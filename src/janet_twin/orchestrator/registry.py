class PluginRegistry:
    def __init__(self):
        self.plugins = {}

    def register(self, name: str, plugin):
        self.plugins[name] = plugin

    def get(self, name: str):
        return self.plugins.get(name)

    def all(self):
        return self.plugins
