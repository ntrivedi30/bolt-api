from typing import Any, Callable


class Depends:
    def __init__(self, dependency: Callable[..., Any]):
        self.dependency = dependency
