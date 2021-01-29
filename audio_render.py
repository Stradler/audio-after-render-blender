import bpy
from bpy.app.handlers import persistent
from bpy.props import *
from bpy.types import Operator, AddonPreferences
import requests
import re
import os
import aud


bl_info = {
    "name": "Render Audio",
    "blender": (2, 83, 0),
    "category": "Object",
}


path = "D:\Blender\Render.mp3"
snd = aud.Sound(path)
dev = aud.Device()

@persistent
def finish_render(scene):
    dev.play(snd)

class RenderAudio(bpy.types.Operator):
    """Stop Audio"""
    bl_idname = "object.render_audio"
    bl_label = "Stop Audio"
    bl_options = {'REGISTER', 'UNDO'}
    total: bpy.props.IntProperty(name="Steps", default=2, min=1, max=100)
    
    def __init__():
      print('lel')

    def execute(self, context):
        
        dev = aud.Device()
        dev.stopAll()
        print(path)

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(RenderAudio.bl_idname)

# store keymaps here to access after registration
addon_keymaps = []


@persistent
def load_handler_for_startup(_):
    bpy.app.handlers.render_complete.clear()
    bpy.app.handlers.render_complete.append(finish_render)


def register():
    bpy.utils.register_class(RenderAudio)
    bpy.types.VIEW3D_MT_object.append(menu_func)

    bpy.app.handlers.load_factory_startup_post.append(load_handler_for_startup)
    bpy.app.handlers.render_complete.clear()
    bpy.app.handlers.render_complete.append(finish_render)

    # handle the keymap
    wm = bpy.context.window_manager
    # Note that in background mode (no GUI available), keyconfigs are not available either,
    # so we have to check this to avoid nasty errors in background case.
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new(RenderAudio.bl_idname, 'T', 'PRESS', ctrl=True, shift=True)
        kmi.properties.total = 4
        addon_keymaps.append((km, kmi))

def unregister():
    # Note: when unregistering, it's usually good practice to do it in reverse order you registered.
    # Can avoid strange issues like keymap still referring to operators already unregistered...
    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.app.handlers.render_complete.clear()
    bpy.utils.unregister_class(RenderAudio)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.app.handlers.load_factory_startup_post.remove(load_handler_for_startup)


if __name__ == "__main__":
    bpy.app.handlers.render_complete.clear()
    bpy.app.handlers.render_complete.append(finish_render)
    register()