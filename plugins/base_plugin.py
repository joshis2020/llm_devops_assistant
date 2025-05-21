class BasePlugin:

    def match(self, prompt: str) -> bool:
        raise "NotImplementedError"

    def execute(self, prompt: str) -> str:
        raise "NotImplementedError" 