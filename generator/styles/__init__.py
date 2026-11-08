"""Every module in this folder with a render(days) function is a style.

The style's name is the module name with dashes, so tree_growth.py is "tree-growth".
"""
import importlib
import pkgutil

STYLES = {}
for _mod in sorted(pkgutil.iter_modules(__path__), key=lambda m: m.name):
    if _mod.name == "catalog":
        continue
    _module = importlib.import_module(f".{_mod.name}", __name__)
    if hasattr(_module, "render"):
        STYLES[_mod.name.replace("_", "-")] = _module.render
