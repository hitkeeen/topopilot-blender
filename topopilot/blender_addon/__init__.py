"""TopoPilot Blender add-on skeleton.

The bpy import is intentionally guarded so the package can be inspected and
the CLI can run on machines without Blender.
"""

bl_info = {
    "name": "TopoPilot",
    "author": "TopoPilot contributors",
    "version": (0, 1, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > TopoPilot",
    "description": "Local-first mesh diagnosis for selected assets",
    "category": "3D View",
}

try:
    import bpy
except ImportError:  # Keep the core importable outside Blender.
    bpy = None


def _classes():
    if bpy is None:
        return ()

    class TOPOPILOT_OT_diagnose(bpy.types.Operator):
        bl_idname = "topopilot.diagnose_active_mesh"
        bl_label = "Diagnose Active Mesh"
        bl_options = {"REGISTER"}

        def execute(self, context):
            from topopilot.diagnosis import diagnose_mesh

            obj = context.active_object
            if obj is None or obj.type != "MESH":
                self.report({"WARNING"}, "Select a mesh object first")
                return {"CANCELLED"}
            mesh = obj.data
            data = {"vertices": [list(vertex.co) for vertex in mesh.vertices], "faces": [list(poly.vertices) for poly in mesh.polygons]}
            report = diagnose_mesh(data, name=obj.name)
            self.report({"INFO"}, "{}: {} warning(s)".format(obj.name, len(report["warnings"])))
            return {"FINISHED"}

    class TOPOPILOT_PT_panel(bpy.types.Panel):
        bl_label = "TopoPilot"
        bl_idname = "TOPOPILOT_PT_panel"
        bl_space_type = "VIEW_3D"
        bl_region_type = "UI"
        bl_category = "TopoPilot"

        def draw(self, context):
            layout = self.layout
            layout.label(text="Local mesh diagnosis")
            layout.operator("topopilot.diagnose_active_mesh", icon="VIEWZOOM")

    return (TOPOPILOT_OT_diagnose, TOPOPILOT_PT_panel)


def register():
    if bpy is None:
        return
    for cls in _classes():
        bpy.utils.register_class(cls)


def unregister():
    if bpy is None:
        return
    for cls in reversed(_classes()):
        bpy.utils.unregister_class(cls)
