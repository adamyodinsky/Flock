"""Singleton class for storing configuration values"""


class FlockConfig:
    """Singleton class for storing configuration values"""

    __instance = None

    class _FlockConfig:
        """Inner class for storing configuration values"""

        def __init__(self):
            self.configuration = {}

        def update_config(self, key, value):
            self.configuration[key] = value

        def get_config(self, key):
            return self.configuration.get(key, None)

    def __new__(cls):
        if not FlockConfig.__instance:
            FlockConfig.__instance = FlockConfig._FlockConfig()
        return FlockConfig.__instance

    def __getattr__(self, name):
        return getattr(self.__instance, name)

    def __setattr__(self, name, value):
        return setattr(self.__instance, name, value)
