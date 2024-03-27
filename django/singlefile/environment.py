import os


class EnvironmentSettings:

    def __init__(self):
        self.source = os.environ

    def get_bool(self, name: str) -> bool:
        """
        Gets a boolean value from the environment
        """
        return self.source.get(name, "").lower() in ["1", "true", "t", "yes"]

    def get(self, name: str, default: str | None = None) -> str | None:
        """
        Gets a string value from the environment
        """
        return self.source.get(name, default)
