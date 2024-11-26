import os


def enshure_dir(path: str) -> None:
    if not os.path.exists(path):
        try:
            os.makedirs(path, exist_ok=True)
        except (IOError, OSError) as e:
            print(e)
