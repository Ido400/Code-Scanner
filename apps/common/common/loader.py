import importlib

from common.errors.plugin_not_found import PluginNotFoundError

class ModuleInterface:
    @staticmethod
    def register() -> None:
        pass

def import_module(name: str) -> ModuleInterface:
    """
    This method will import the module 
    """
    try:
        return importlib.import_module(name)
    except ImportError:
        raise PluginNotFoundError("The plugin not found") 

def load_plugins(plugins: list)->None:
    """
    This method will import the plugins 

    Args:
    -----
        plugins(list): The list of engines that will be imported
    """
    try:
        for plugin_file in plugins:
            plugin = import_module(f"common.plugins.{plugin_file}")
            plugin.register()
    except PluginNotFoundError:
        raise PluginNotFoundError("The plugin not found")