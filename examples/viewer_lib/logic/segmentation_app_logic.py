from trame_server import Server

from trame_slicer.core import LayoutManager, SlicerApp

from ..ui import SegmentationAppUI, SegmentEditorUI, ViewerLayoutState, VolumePropertyUI
from .viewer_logic import ViewerLogic


class SegmentationAppLogic(ViewerLogic[ViewerLayoutState]):
    def __init__(self, server: Server, slicer_app: SlicerApp):
        super().__init__(server, slicer_app, ViewerLayoutState)

    def set_ui(self, ui: SegmentationAppUI):
        self._segment_editor_logic.set_ui(ui.tool_registry[SegmentEditorUI])
        self._volume_properties_logic.set_ui(ui.tool_registry[VolumePropertyUI])
        self._layout_button_logic.set_ui(ui.layout_button)
        self._load_files_logic.set_ui(ui.load_volume_items_buttons)
        self._mpr_logic.set_ui(ui.mpr_interaction_button)

    def _on_volume_changed(self, *_args):
        self.data.is_drawer_visible = True
        self.data.active_tool = SegmentEditorUI.__name__
        super()._on_volume_changed(*_args)
