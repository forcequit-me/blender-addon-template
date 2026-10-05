"""Smoke test: the add-on enables, every operator registers, disable and re-enable work,
an update loads every file fresh, and bl_info matches blender_manifest.toml.

Run headless:
    blender --background --factory-startup --python tests/test_blender_smoke.py

--factory-startup keeps an installed copy of this add-on from shadowing the repo copy.
"""

import sys
import tomllib
from pathlib import Path

import addon_utils
import bpy

MODULE = 'addon_name'
OPERATORS = [
    'wm.addon_name_example',
    'wm.addon_name_open_link',
]

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def check_manifest(info):
    manifest = tomllib.loads((REPO / MODULE / "blender_manifest.toml").read_text(encoding="utf-8"))
    pairs = [
        ("name", info["name"], manifest["name"]),
        ("version", ".".join(map(str, info["version"])), manifest["version"]),
        ("blender", ".".join(map(str, info["blender"])), manifest["blender_version_min"]),
    ]
    for key, from_info, from_manifest in pairs:
        assert from_info == from_manifest, f"bl_info {key} {from_info!r} != manifest {from_manifest!r}"


def check_update_loads_new_files(mod):
    """Installing an update over a loaded copy reloads only __init__.py. The add-on's
    other files must load fresh too, or a class the new __init__ asks for is missing.
    Leaves the add-on disabled."""
    import os
    import addon_utils
    old = {n: m for n, m in sys.modules.items() if n.startswith(mod.__name__ + ".")}
    addon_utils.disable(mod.__name__, default_set=False)
    stamp = os.path.getmtime(mod.__file__)
    os.utime(mod.__file__, (stamp + 1, stamp + 1))  # an update changes __init__.py on disk
    try:
        assert addon_utils.enable(mod.__name__, default_set=True) is not None, "enable after an update failed"
        addon_utils.disable(mod.__name__, default_set=False)
    finally:
        os.utime(mod.__file__, (stamp, stamp))
    stale = sorted(n for n, m in old.items() if sys.modules.get(n) is m)
    assert not stale, f"still the old version after an update: {stale}"


def run():
    addon_utils.disable(MODULE, default_set=False)
    mod = addon_utils.enable(MODULE, default_set=True)  # same path as the prefs checkbox
    assert mod is not None, f"{MODULE} failed to enable"
    check_manifest(mod.bl_info)
    try:
        for op in OPERATORS:
            category, name = op.split(".")
            getattr(getattr(bpy.ops, category), name).get_rna_type()  # raises if not registered
    finally:
        addon_utils.disable(MODULE, default_set=False)
    check_update_loads_new_files(mod)
    # A second enable must work too (script reload, toggling in prefs).
    assert addon_utils.enable(MODULE, default_set=True) is not None
    addon_utils.disable(MODULE, default_set=False)
    print(f"SMOKE OK: {MODULE} ({len(OPERATORS)} operators)")


if __name__ == "__main__":
    run()
