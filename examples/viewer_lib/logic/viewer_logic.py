from pathlib import Path
from typing import TypeVar

from .base_logic import BaseLogic

from trame_server import Server

from trame_slicer.core import SlicerApp

T = TypeVar("T")

class ViewerLogic(BaseLogic[T]):
    def __init__(self, server: Server, slicer_app: SlicerApp, state_type: type[T] | None):
        super().__init__(server, slicer_app, state_type)
        self.load_js_module(server)

    def load_js_module(self, server: Server) -> None:
        js_file = Path(__file__).parent.parent.parent / "js/utils.js"
        server.enable_module(
            dict(
                serve={"file_loading": str(js_file.parent)},
                scripts=[f"file_loading/{js_file.name}"],
            )
        )
