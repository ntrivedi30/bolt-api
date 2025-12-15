from typing import Any

import msgspec
from starlette.responses import Response


class FastJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        # The msgspec magic
        return msgspec.json.encode(content)
