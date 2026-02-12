from trame_server import Server

from trame_slicer.core import SlicerApp

from ..ui import MedicalViewerUI, SegmentEditorUI, ViewerLayoutState, VolumePropertyUI
from .viewer_logic import ViewerLogic
from .markups_button_logic import MarkupsButtonLogic
from .segmentation import SegmentEditorLogic
from .slab_logic import SlabLogic


class MedicalViewerLogic(ViewerLogic[ViewerLayoutState]):
    def __init__(self, server: Server, slicer_app: SlicerApp):
        super().__init__(server, slicer_app, ViewerLayoutState)

        # Create the application logic
        self._segment_editor_logic = SegmentEditorLogic(server, slicer_app)
        self._markups_logic = MarkupsButtonLogic(server, slicer_app)
        self._slab_logic = SlabLogic(server, slicer_app)

    def set_ui(self, ui: MedicalViewerUI):
        self._segment_editor_logic.set_ui(ui.tool_registry[SegmentEditorUI])
        self._volume_properties_logic.set_ui(ui.tool_registry[VolumePropertyUI])
        self._layout_button_logic.set_ui(ui.layout_button)
        self._markups_logic.set_ui(ui.markups_button)
        self._load_files_logic.set_ui(ui.load_volume_items_buttons)
        self._slab_logic.set_ui(ui.slab_button)
        self._mpr_logic.set_ui(ui.mpr_interaction_button)
