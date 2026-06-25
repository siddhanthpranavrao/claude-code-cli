import os


class MissingSecretError(RuntimeError):
    pass


def require_secret(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise MissingSecretError(f"Missing required secret: {name}")
    return value

