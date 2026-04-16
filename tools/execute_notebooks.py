from pathlib import Path
import os
from contextlib import contextmanager

import nbformat
from nbclient import NotebookClient
import jupyter_core.paths as jupyter_paths
import jupyter_client.connect as jupyter_connect


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT / ".jupyter_runtime"
NOTEBOOKS = [
    ROOT / "Prac_04" / "homework" / "Homework.ipynb",
    ROOT / "Prac_05" / "homework" / "Homework.ipynb",
    ROOT / "Prac_06" / "Prac 06.1" / "homework" / "Homework.ipynb",
    ROOT / "Prac_07" / "Prac 07.2" / "homework" / "Homework.ipynb",
    ROOT / "Prac_08" / "Prac 08.1" / "homework" / "Homework.ipynb",
    ROOT / "Prac_08" / "Prac 08.2" / "homework" / "Homework.ipynb",
    ROOT / "Prac_09" / "Poisson_Blending_Comparison.ipynb",
]


@contextmanager
def insecure_write(path, binary=False):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    mode = "wb" if binary else "w"
    with open(path, mode) as f:
        yield f


jupyter_paths.secure_write = insecure_write
jupyter_connect.secure_write = insecure_write


def execute_notebook(path: Path):
    RUNTIME_DIR.mkdir(exist_ok=True)
    os.environ["JUPYTER_RUNTIME_DIR"] = str(RUNTIME_DIR)
    with path.open("r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
    client = NotebookClient(nb, timeout=1800, kernel_name="python3")
    client.execute(cwd=str(path.parent))
    with path.open("w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print(f"Executed: {path}")


def main():
    for path in NOTEBOOKS:
        execute_notebook(path)


if __name__ == "__main__":
    main()
