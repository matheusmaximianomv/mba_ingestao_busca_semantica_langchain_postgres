import os

def validate_env(envs: list[str]):
    for keys in envs:
        if not os.getenv(keys):
            raise ValueError(f"Environment variable {keys} is not set")