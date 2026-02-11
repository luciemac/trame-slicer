from pathlib import Path
from trame.app import get_server, TrameApp
from trame.app.testing import enable_testing
from trame_server import Server

try:
    from viewer_lib import MedicalViewerLogic, MedicalViewerUI
except ModuleNotFoundError:
    from .viewer_lib import MedicalViewerLogic, MedicalViewerUI

from trame_slicer.core import SlicerApp


class MedicalViewerApp:
    def __init__(self, server: Server | None=None) -> None:
        self._server = get_server(server, client_type="vue3")
        self._slicer_app = SlicerApp()

        self._logic = MedicalViewerLogic(self._server, self._slicer_app)
        self._ui = MedicalViewerUI(self._server, self._logic.layout_manager)
        self._logic.set_ui(self._ui)

    @property
    def server(self):
        return self._server


def load_js_module(server: Server) -> None:
    js_file = Path(__file__).parent / "js/utils.js"
    server.enable_module(
        dict(
            serve={"file_loading": str(js_file.parent)},
            scripts=[f"file_loading/{js_file.name}"],
        )
    )

def main(server=None, **kwargs):
    app = MedicalViewerApp(server)
    enable_testing(app.server)
    load_js_module(app.server)
    app.server.start(**kwargs)


if __name__ == "__main__":
    main()
