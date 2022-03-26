import importlib

class ModuleInterface:
    @staticmethod
    def register() -> None:
        pass

def import_module(name: str) -> ModuleInterface:
    return importlib.import_module(name)

def load_plugins(plugins: list)->None:
    for plugin_file in plugins:
        plugin = import_module(f"common.plugins.{plugin_file}")
        plugin.register()