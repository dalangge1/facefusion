from typing import List, Optional

import gradio

from facefusion import state_manager, wording
from facefusion.processors.frame import choices as frame_processors_choices
from facefusion.processors.frame.typing import FaceDebuggerItem
from facefusion.uis.core import get_ui_component, register_ui_component

FACE_DEBUGGER_ITEMS_CHECKBOX_GROUP : Optional[gradio.CheckboxGroup] = None


def render() -> None:
	global FACE_DEBUGGER_ITEMS_CHECKBOX_GROUP

	FACE_DEBUGGER_ITEMS_CHECKBOX_GROUP = gradio.CheckboxGroup(
		label = wording.get('uis.face_debugger_items_checkbox_group'),
		choices = frame_processors_choices.face_debugger_items,
		value = state_manager.get_item('face_debugger_items'),
		visible = 'face_debugger' in state_manager.get_item('frame_processors')
	)
	register_ui_component('face_debugger_items_checkbox_group', FACE_DEBUGGER_ITEMS_CHECKBOX_GROUP)


def listen() -> None:
	FACE_DEBUGGER_ITEMS_CHECKBOX_GROUP.change(update_face_debugger_items, inputs = FACE_DEBUGGER_ITEMS_CHECKBOX_GROUP)

	frame_processors_checkbox_group = get_ui_component('frame_processors_checkbox_group')
	if frame_processors_checkbox_group:
		frame_processors_checkbox_group.change(update_frame_processors, inputs = frame_processors_checkbox_group, outputs = FACE_DEBUGGER_ITEMS_CHECKBOX_GROUP)


def update_frame_processors(frame_processors : List[str]) -> gradio.CheckboxGroup:
	has_face_debugger = 'face_debugger' in frame_processors
	return gradio.CheckboxGroup(visible = has_face_debugger)


def update_face_debugger_items(face_debugger_items : List[FaceDebuggerItem]) -> None:
	state_manager.set_item('face_debugger_items', face_debugger_items)