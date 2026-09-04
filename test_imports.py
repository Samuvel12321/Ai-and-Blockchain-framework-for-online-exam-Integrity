import time
import importlib

modules = [
    "object_cheating.components.camera_feed",
    "object_cheating.components.controls",
    "object_cheating.components.treshold",
    "object_cheating.components.stats_panel",
    "object_cheating.components.behavior_panel",
    "object_cheating.components.coordinate_panel",
    "object_cheating.components.table",
    "object_cheating.components.input_panel",
    "object_cheating.components.warning_dialog",
    "object_cheating.components.delete_dialog",
]

for module in modules:
    start = time.time()
    try:
        importlib.import_module(module)
        print(f"{module}: {time.time() - start:.2f} sec")
    except Exception as e:
        print(f"{module}: ERROR -> {e}")