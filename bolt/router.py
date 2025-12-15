from typing import Callable

# We need to replicate the decorator logic,
# but we can't fully reuse the code from App because App is an ASGI application
# and Router is just a container.


class Router:
    def __init__(self, prefix: str = ""):
        self.prefix = prefix
        self.routes = []  # Stores tuples: (path, method, handler)

    def get(self, path: str):
        return self._register(path, "GET")

    def post(self, path: str):
        return self._register(path, "POST")

    def put(self, path: str):
        return self._register(path, "PUT")

    def delete(self, path: str):
        return self._register(path, "DELETE")

    def patch(self, path: str):
        return self._register(path, "PATCH")

    def _register(self, path: str, method: str):
        def wrapper(func: Callable):
            # We just store the function and path.
            # The Main App will apply the 'Magic Decorator' later.
            full_path = self.prefix + path
            self.routes.append({"path": full_path, "method": method, "handler": func})
            return func

        return wrapper
