# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    "name": "text to Strips",
    "author": "Tintwotin",
    "version": (0, 2),
    "blender": (2, 80, 0),
    "location": "Text Editor Edit Menu",
    "description": "Converts lines or full text to one or more Text strips",
    "warning": "",
    "wiki_url": "",
    "category": "Text Editor",
}


import bpy
import re
from bpy.types import Operator
from bpy.props import (
    BoolProperty,
    EnumProperty,
)


def find_completely_empty_channel():
    if not bpy.context.scene.sequence_editor:
        bpy.context.scene.sequence_editor_create()
    sequences = bpy.context.sequences
    if not sequences:
        addSceneChannel = 1
    else:
        channels = [s.channel for s in sequences]
        channels = sorted(list(set(channels)))
        empty_channel = channels[-1] + 1
        addSceneChannel = empty_channel
    return addSceneChannel


class TEXT_OT_text_to_strip(Operator):
    """Converts lines or full text to text strips"""

    bl_idname = "text.text_to_strip"
    bl_label = "Text to Strip"
    bl_options = {"REGISTER", "UNDO"}

    type: EnumProperty(
        name="Text to Strip",
        description="Sends line or full text to text strip",
        options={"ENUM_FLAG"},
        items=(
            ("FULL_TEXT", "One Strip", "Full text to one Text strip"),
            ("LINES", "One Strip per Line", "Text lines to Text strips"),
        ),
        default={"LINES"},
    )

    @classmethod
    def poll(cls, context):
        return context.area.type == "TEXT_EDITOR" and context.space_data.text

    def execute(self, context):
        st = context.space_data
        text = st.text.as_string()
        name = st.text.name
        old_line = bpy.context.space_data.text.current_line_index
        trimmed = ""
        instance = 0
        lines = str(text).splitlines()
        chan = find_completely_empty_channel()

        scn = bpy.context.scene
        cf = scn.frame_current
        context = bpy.context

        if self.type == {"FULL_TEXT"}:
            text_strip = bpy.context.scene.sequence_editor.sequences.new_effect(
                name="Text Edit",
                type="TEXT",
                frame_start=cf,
                frame_end=cf + 100,
                channel=chan,
            )
            text_strip.text = text
            text_strip.location[1] = 0.5
            text_strip.location[0] = 0.2
            text_strip.align_y = "CENTER"
            text_strip.align_x = "LEFT"
            text_strip.wrap_width = 0.68
            text_strip.font_size = 40
        if self.type == {"LINES"}:
            pos = 0
            for i in range(len(lines)):
                text_strip = bpy.context.scene.sequence_editor.sequences.new_effect(
                    name="Text Edit",
                    type="TEXT",
                    frame_start=pos,
                    frame_end=pos + 100,
                    channel=chan,
                )
                text_strip.text = lines[i].replace("  ", "")
                text_strip.location[1] = 0.1
                text_strip.location[0] = 0.2
                text_strip.align_y = "BOTTOM"
                text_strip.align_x = "LEFT"
                text_strip.wrap_width = 0.68
                text_strip.font_size = 40
                pos += 100
        return {"FINISHED"}


def menu_text_to_strip(self, context):
    self.layout.operator_menu_enum("text.text_to_strip", "type")


def register():
    bpy.utils.register_class(TEXT_OT_text_to_strip)
    bpy.types.TEXT_MT_edit.append(menu_text_to_strip)


def unregister():
    bpy.utils.unregister_class(TEXT_OT_text_to_strip)
    bpy.types.TEXT_MT_edit.remove(menu_text_to_strip)


if __name__ == "__main__":
    register()
