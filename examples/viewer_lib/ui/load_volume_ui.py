from dataclasses import dataclass, field

from trame.decorators import trigger
from trame.widgets import client
from trame_server.utils.typed_state import TypedState
from trame_vuetify.widgets.vuetify3 import VFileInput, VProgressCircular, VTooltip
from undo_stack import Signal

from .flex_container import FlexContainer


@dataclass
class LoadVolumeItemsState:
    loading_busy: bool = False
    button_tooltip: bool = False


@dataclass
class LoadVolumeState:
    file_button: LoadVolumeItemsState = field(default_factory=LoadVolumeItemsState)
    dir_button: LoadVolumeItemsState = field(default_factory=LoadVolumeItemsState)


class LoadVolumeUI(FlexContainer):
    on_load_volume = Signal(list[dict], str)

    def __init__(self, **kwargs):
        super().__init__(row=True, **kwargs)

        typed_state = TypedState(self.state, LoadVolumeState)

        with self:
            client.Style(".v-input__prepend .v-icon { opacity: 1.0; }")  # Overwrite vuetify's opacity
            self.load_volume_files_button = LoadVolumeButton(
                name="Open Files",
                load_directory=False,
                icon="mdi-file-upload",
                typed_state=typed_state.get_sub_state(typed_state.name.file_button),
            )
            self.load_volume_dir_button = LoadVolumeButton(
                name="Open Directory",
                load_directory=True,
                icon="mdi-folder-upload",
                typed_state=typed_state.get_sub_state(typed_state.name.dir_button),
            )

        self.load_volume_files_button.on_load_volume.connect(self.on_load_volume)
        self.load_volume_dir_button.on_load_volume.connect(self.on_load_volume)


class LoadVolumeButton(FlexContainer):
    on_load_volume = Signal(list[dict], str)

    def __init__(self, name: str, load_directory: bool, icon: str, typed_state: TypedState[LoadVolumeItemsState]):
        super().__init__(justify="center", row=True, style="width: 50px; height: 50px;")

        self._files = []
        self._typed_state = typed_state

        with self:
            VTooltip(
                v_model=(typed_state.name.button_tooltip,),
                text=name,
                activator="parent",
                transition="slide-y-transition",
                location="bottom start",
            )
            VFileInput(
                v_if=(f"!{typed_state.name.loading_busy}",),
                change=f"""
                    utils.file_loading.actions.send_chunk(
                        $event.target.files,
                        '{self.server.trigger_name(self.upload_chunk)}'
                    )
                """,
                prepend_icon=icon,
                multiple=not load_directory,
                hide_input=True,
                raw_attrs=["webkitdirectory"] if load_directory else [],
            )
            VProgressCircular(v_else=True, indeterminate=True, size=24)

    async def upload_chunk(self, files_list: list[dict]) -> None:
        self._typed_state.data.loading_busy = True
        self._typed_state.data.button_tooltip = False

        if not files_list:
            await self.on_load_volume.async_emit(self._files, self._typed_state.name.loading_busy)
            self._files = []

        else:
            self._files.extend(files_list)
