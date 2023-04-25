"""Load plugins from plugins directory."""

import importlib
import os


def __load_plugins(plugin_directory: str) -> dict:
    plugins_map = {}

    # if plugin_directory not exist return empty dict
    if not os.path.isdir(plugin_directory):
        return plugins_map

    for file in os.listdir(plugin_directory):
        if file.endswith(".py") and file != "__init__.py":
            module_name = file[:-3]
            module = importlib.import_module(f"{plugin_directory}.{module_name}")

            for key, value in module.export.items():
                plugins_map[key] = value
    return plugins_map


def load_plugins(native_plugins_dir: str = "plugins") -> dict:
    """Load plugins from plugins directory."""

    external_plugins_path: str = os.getenv("FLOCK_PLUGINS_PATH", "")
    if external_plugins_path:
        external_plugins: dict = __load_plugins(external_plugins_path)
    else:
        external_plugins: dict = {}

    native_plugins: dict = __load_plugins(plugin_directory=native_plugins_dir)
    plugins: dict = {**external_plugins, **native_plugins}

    return plugins
