class BasePlugin:

    def execute(self, prompt: str) -> str:
        raise "NotImplementedError" 