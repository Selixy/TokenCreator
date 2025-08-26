# .vscode/script/build.py
import shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "tokencreator.spec"
OUT = ROOT / "build"

def run(cmd):
    print("+", " ".join(map(str, cmd)))
    subprocess.check_call(cmd)

def main():
    if OUT.exists():
        shutil.rmtree(OUT)

    distpath = OUT / "dist"
    workpath = OUT / "work"

    run([
        sys.executable, "-m", "PyInstaller",
        str(SPEC),
        "--distpath", str(distpath),
        "--workpath", str(workpath),
        "--clean",
        "--noconfirm"
    ])

    print(f"\n Build terminé -> {distpath/'TokenCreator'}")

if __name__ == "__main__":
    main()
