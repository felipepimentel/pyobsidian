import importlib
import os

class PluginSystem:
    def __init__(self, plugin_dir):
        self.plugin_dir = plugin_dir
        self.plugins = {}

    def load_plugins(self):
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename[:-3]
                spec = importlib.util.spec_from_file_location(module_name, os.path.join(self.plugin_dir, filename))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'register_plugin'):
                    self.plugins[module_name] = module.register_plugin()

    def execute_plugin(self, plugin_name, *args, **kwargs):
        if plugin_name in self.plugins:
            return self.plugins[plugin_name].execute(*args, **kwargs)
        else:
            raise ValueError(f"Plugin {plugin_name} not found")

    def list_plugins(self):
        return list(self.plugins.keys())