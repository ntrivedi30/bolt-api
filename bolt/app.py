import inspect
import re
import traceback
from typing import Callable, List, get_type_hints

import msgspec
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.routing import Route

from .background import BackgroundTasks  # <--- NEW IMPORT
from .di import Depends
from .openapi import TYPE_MAP, get_redoc_html, get_swagger_ui_html

# Internal imports
from .response import FastJSONResponse
from .router import Router


class Bolt(Starlette):
    def __init__(self, title="Bolt API", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title

        # 1. Register Exception Handlers
        self.add_exception_handler(HTTPException, self.http_exception_handler)
        self.add_exception_handler(
            msgspec.ValidationError, self.validation_exception_handler
        )
        self.add_exception_handler(Exception, self.server_error_handler)

        # 2. Register Documentation Routes
        self.add_route("/openapi.json", self.openapi_endpoint, methods=["GET"])
        self.add_route("/docs", self.swagger_endpoint, methods=["GET"])
        self.add_route("/redoc", self.redoc_endpoint, methods=["GET"])

    # --- CORS SUPPORT ---
    def enable_cors(self, origins: List[str] = None):
        """
        Enables Cross-Origin Resource Sharing (CORS).
        """
        if origins is None:
            origins = ["*"]

        self.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # --- DOCS HANDLERS ---
    async def openapi_endpoint(self, request):
        return JSONResponse(self.generate_openapi())

    async def swagger_endpoint(self, request):
        return HTMLResponse(get_swagger_ui_html("/openapi.json", self.title))

    async def redoc_endpoint(self, request):
        return HTMLResponse(get_redoc_html("/openapi.json", self.title))

    def generate_openapi(self):
        """Generates the OpenAPI dict by inspecting registered routes."""
        schema = {
            "openapi": "3.0.3",
            "info": {"title": self.title, "version": "1.0.0"},
            "paths": {},
            "components": {"schemas": {}},
        }

        for route in self.routes:
            if not isinstance(route, Route):
                continue
            if route.path in ["/openapi.json", "/docs", "/redoc"]:
                continue

            # Retrieve metadata attached to the wrapper
            handler = route.endpoint
            meta = getattr(handler, "_bolt_meta", None)
            if not meta:
                continue

            path = route.path
            if path not in schema["paths"]:
                schema["paths"][path] = {}

            # Build Operation Object
            method = list(route.methods)[0].lower()

            operation = {
                "summary": meta["name"].replace("_", " ").title(),
                "parameters": [],
                "responses": {"200": {"description": "Successful Response"}},
            }

            # Add Path & Query Parameters
            for name, type_cls in meta["path_params"].items():
                operation["parameters"].append(
                    {
                        "name": name,
                        "in": "path",
                        "required": True,
                        "schema": {"type": TYPE_MAP.get(type_cls, "string")},
                    }
                )

            for name, type_cls in meta["query_params"].items():
                operation["parameters"].append(
                    {
                        "name": name,
                        "in": "query",
                        "required": False,
                        "schema": {"type": TYPE_MAP.get(type_cls, "string")},
                    }
                )

            # Add Request Body
            if meta["body_type"]:
                (js_schema, components) = msgspec.json.schema(meta["body_type"])
                if components:
                    schema["components"]["schemas"].update(components)

                operation["requestBody"] = {
                    "required": True,
                    "content": {"application/json": {"schema": js_schema}},
                }

            schema["paths"][path][method] = operation

        return schema

    # --- EXCEPTION HANDLERS ---
    async def http_exception_handler(self, request, exc: HTTPException):
        return FastJSONResponse({"error": exc.detail}, status_code=exc.status_code)

    async def validation_exception_handler(self, request, exc: msgspec.ValidationError):
        return FastJSONResponse(
            {"error": "Validation Error", "detail": str(exc)}, status_code=422
        )

    async def server_error_handler(self, request, exc: Exception):
        traceback.print_exc()
        return FastJSONResponse({"error": "Internal Server Error"}, status_code=500)

    # --- ROUTING DECORATORS ---
    def get(self, path: str):
        return self._decorator(path, methods=["GET"])

    def post(self, path: str):
        return self._decorator(path, methods=["POST"])

    def put(self, path: str):
        return self._decorator(path, methods=["PUT"])

    def delete(self, path: str):
        return self._decorator(path, methods=["DELETE"])

    def patch(self, path: str):
        return self._decorator(path, methods=["PATCH"])

    def include_router(self, router: Router):
        """
        Takes all routes from a Router and registers them with the main App.
        """
        for route in router.routes:
            path = route["path"]
            method = route["method"]
            handler = route["handler"]
            decorator = self._decorator(path, methods=[method])
            decorator(handler)

    def _decorator(self, path: str, methods: list[str]):
        # OPTIMIZATION: Compile regex once
        path_param_names = set(re.findall(r"{(.*?)}", path))

        def wrapper(func: Callable):
            sig = inspect.signature(func)
            type_hints = get_type_hints(func)

            struct_param = None
            struct_type = None
            dependencies = {}
            path_params_config = {}
            query_params_config = {}

            # Static Analysis (Startup Time)
            for name, param in sig.parameters.items():
                if name == "request":
                    continue

                # Check for Dependency
                if isinstance(param.default, Depends):
                    dependencies[name] = param.default.dependency
                    continue

                # Check for Body
                if name in type_hints and issubclass(type_hints[name], msgspec.Struct):
                    struct_param = name
                    struct_type = type_hints[name]
                    continue

                # Check for Path Param
                if name in path_param_names:
                    path_params_config[name] = type_hints.get(name, str)
                    continue

                # Check for Query Param (Simple types only)
                if name in type_hints and type_hints[name] in (int, str, bool, float):
                    query_params_config[name] = type_hints[name]

            # Runtime Handler (Request Time)
            async def endpoint(request: Request):
                kwargs = {}
                cleanup_generators = []
                background_tasks = None  # Store tasks here

                try:
                    if "request" in sig.parameters:
                        kwargs["request"] = request

                    # 1. Path Params
                    for name, caster in path_params_config.items():
                        try:
                            kwargs[name] = caster(request.path_params.get(name))
                        except ValueError:
                            raise HTTPException(422, f"Invalid path: {name}")

                    # 2. Query Params
                    for name, caster in query_params_config.items():
                        raw = request.query_params.get(name)
                        if raw is None:
                            if sig.parameters[name].default != inspect.Parameter.empty:
                                continue
                            raise HTTPException(400, f"Missing query: {name}")
                        try:
                            if caster is bool:
                                kwargs[name] = raw.lower() == "true"
                            else:
                                kwargs[name] = caster(raw)
                        except ValueError:
                            raise HTTPException(422, f"Invalid query: {name}")

                    # 3. Dependencies
                    for name, dep in dependencies.items():
                        if inspect.isasyncgenfunction(dep):
                            gen = dep()
                            kwargs[name] = await gen.__anext__()
                            cleanup_generators.append(gen)
                        elif inspect.iscoroutinefunction(dep):
                            kwargs[name] = await dep()
                        else:
                            kwargs[name] = dep()

                    # 4. Check for BackgroundTasks Injection
                    # We check the annotation of arguments not yet filled
                    for name, param in sig.parameters.items():
                        if name not in kwargs and param.annotation == BackgroundTasks:
                            background_tasks = BackgroundTasks()
                            kwargs[name] = background_tasks

                    # 5. Body
                    if struct_type:
                        kwargs[struct_param] = msgspec.json.decode(
                            await request.body(), type=struct_type
                        )

                    # 6. Execute User Function
                    res = await func(**kwargs)

                    # Wrap response
                    response = (
                        res if isinstance(res, Response) else FastJSONResponse(res)
                    )

                    # 7. Attach Background Tasks (if any)
                    if background_tasks and background_tasks.tasks:
                        response.background = background_tasks.execute

                    return response

                finally:
                    # 8. CLEANUP (Close DB Sessions)
                    for gen in reversed(cleanup_generators):
                        try:
                            await gen.aclose()
                        except Exception:
                            pass

            # METADATA ATTACHMENT
            endpoint._bolt_meta = {
                "name": func.__name__,
                "path_params": path_params_config,
                "query_params": query_params_config,
                "body_type": struct_type,
            }

            self.add_route(path, endpoint, methods=methods)
            return func

        return wrapper
