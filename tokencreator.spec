# tokencreator.spec
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules

root = Path.cwd()

# Collecte des QSS où qu’ils soient (styles/ ou app/styles/)
datas = []
for d in (root / "styles", root / "app" / "styles"):
    if d.exists():
        for p in d.glob("*.qss"):
            datas.append((str(p), "styles"))

icons_dir = root / "icons"
if icons_dir.exists():
    for p in icons_dir.glob("*.ico"):
        datas.append((str(p), "icons"))

a = Analysis(
    ['app/__main__.py'],
    pathex=[str(root)],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'qframelesswindow',
        'qframelesswindow.windows',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=['qframelesswindow.mac', 'qframelesswindow.linux'],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)
exe = EXE(
    pyz,
    a.scripts,
    name='TokenCreator',
    icon=str((root / 'icons' / 'app.ico')) if (root / 'icons' / 'app.ico').exists() else None,
    console=False,
)
coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, name='TokenCreator')
