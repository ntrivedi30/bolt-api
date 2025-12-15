# Helper to map Python types to OpenAPI types
TYPE_MAP = {int: "integer", str: "string", bool: "boolean", float: "number"}


# --- HTML TEMPLATES ---
def get_swagger_ui_html(openapi_url: str, title: str):
    return (
        "<!DOCTYPE html>"
        "<html>"
        "<head>"
        f"<title>{title}</title>"
        '<link rel="stylesheet" '
        'href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">'
        "</head>"
        "<body>"
        '<div id="swagger-ui"></div>'
        '<script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/'
        'swagger-ui-bundle.js"></script>'
        "<script>"
        "window.onload = () => {"
        "    window.ui = SwaggerUIBundle({"
        f"        url: '{openapi_url}',"
        "        dom_id: '#swagger-ui',"
        "    });"
        "};"
        "</script>"
        "</body>"
        "</html>"
    )


def get_redoc_html(openapi_url: str, title: str):
    return (
        "<!DOCTYPE html>"
        "<html>"
        "<head>"
        f"<title>{title}</title>"
        '<meta charset="utf-8"/>'
        '<script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/'
        'redoc.standalone.js"></script>'
        "</head>"
        "<body>"
        f'<redoc spec-url="{openapi_url}"></redoc>'
        "</body>"
        "</html>"
    )
