from pathlib import Path
import tomllib

def load_config(path: Path) -> dict:
    # Lee archivos TOML defensivamente devolviendo dict vacío si no existe.
    if not path.exists():
        return {}
    with path.open("rb") as fh:
        return tomllib.load(fh)
