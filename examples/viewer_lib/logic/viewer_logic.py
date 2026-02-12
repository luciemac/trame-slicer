from pathlib import Path
from typing import TypeVar

from .base_logic import BaseLogic
from .layout_button_logic import LayoutButtonLogic
from .load_volume_logic import LoadVolumeLogic
from .mpr_interaction_button_logic import MprInteractionButtonLogic
from .segmentation import SegmentEditorLogic
from .volume_property_logic import VolumePropertyLogic

from trame_server import Server
from trame_slicer.core import LayoutManager, SlicerApp
from trame_slicer.rca_view import register_rca_factories


T = TypeVar("T")

class ViewerLogic(BaseLogic[T]):
    def __init__(self, server: Server, slicer_app: SlicerApp, state_type: type[T] | None):
        super().__init__(server, slicer_app, state_type)

        # Load JS module
        self.load_js_module(server)

        # Register the RCA view creation
        register_rca_factories(self._slicer_app.view_manager, self._server)

        # Create application logic
        self._layout_button_logic = LayoutButtonLogic(server, slicer_app)
        self._load_files_logic = LoadVolumeLogic(server, slicer_app)
        self._mpr_logic = MprInteractionButtonLogic(server, slicer_app)
        self._segment_editor_logic = SegmentEditorLogic(server, slicer_app)
        self._volume_properties_logic = VolumePropertyLogic(server, slicer_app)

        # Connect signals
        self._load_files_logic.volume_loaded.connect(self._on_volume_changed)
        self._load_files_logic.volume_loaded.connect(self._volume_properties_logic.on_volume_changed)
        self._load_files_logic.volume_loaded.connect(self._segment_editor_logic.on_volume_changed)

        # Initialize the state defaults
        self.server.state["trame__title"] = "trame Slicer"
        self.server.state["trame__favicon"] = (
            "https://raw.githubusercontent.com/Slicer/Slicer/main/Applications/SlicerApp/Resources/Icons/Medium/Slicer-DesktopIcon.png"
        )

    @property
    def layout_manager(self) -> LayoutManager:
        return self._layout_button_logic.layout_manager

    def load_js_module(self, server: Server) -> None:
        js_file = Path(__file__).parent.parent.parent / "js/utils.js"
        server.enable_module(
            dict(
                serve={"file_loading": str(js_file.parent)},
                scripts=[f"file_loading/{js_file.name}"],
            )
        )

    def _on_volume_changed(self, *_args):
        self.data.is_volume_loaded = True
