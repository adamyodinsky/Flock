import os
import importlib
from flock_models.resources.base import Resource

def __load_plugins(plugin_directory: str, plugin_base_class = Resource) -> dict:
    plugins_map = {}

    for file in os.listdir(plugin_directory):
        if file.endswith(".py") and file != "__init__.py":
            module_name = file[:-3]
            module = importlib.import_module(f"{plugin_directory}.{module_name}")

            for item in dir(module):
                obj = getattr(module, item)

                if isinstance(obj, type) and issubclass(obj, plugin_base_class) and obj != plugin_base_class:
                    plugins_map[module_name] = obj
    return plugins_map


def load_plugins(native_plugins_dir: str = "plugins") -> dict:
        external_plugins_path: str = os.getenv("FLOCK_PLUGINS_PATH")
        if external_plugins_path:
            external_plugins: dict = __load_plugins(external_plugins_path)
        else :
            external_plugins: dict = {}

        native_plugins: dict = __load_plugins(plugin_directory=native_plugins_dir)
        plugins: dict = {**external_plugins, **native_plugins}

        return plugins