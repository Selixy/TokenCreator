# app/ui/apply_theme.py
import re
import sys
from pathlib import Path

def apply_theme(app, theme: str = "dark") -> None:
    candidates: list[Path] = []

    # PyInstaller
    if getattr(sys, "frozen", False):
        meipass = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
        candidates += [meipass / "styles", Path(sys.executable).parent / "styles"]

    # Développement
    here = Path(__file__).resolve().parent
    candidates += [here.parent / "styles", here / "styles"]

    # Trouver le premier dossier contenant base.qss
    base_dir = next((c for c in candidates if (c / "base.qss").exists()), None)
    if base_dir is None:
        sys.stderr.write("[WARN] Aucun fichier QSS trouvé, thème non appliqué\n")
        return

    base_qss = (base_dir / "base.qss").read_text(encoding="utf-8")
    theme_path = base_dir / f"{theme}.colors.qss"

    if not theme_path.exists():
        sys.stderr.write(f"[WARN] {theme_path.name} manquant, seul base.qss appliqué\n")
        app.setStyleSheet(base_qss)
        return

    mapping: dict[str, str] = {}
    for line in theme_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith(("/*", "//", "#")):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            mapping[k.strip()] = v.strip().rstrip(";")

    # Vérifier les clés nécessaires
    needed = set(re.findall(r"\{\{[^}]+}}", base_qss))
    missing = needed - set(mapping.keys())
    if missing:
        sys.stderr.write(f"[WARN] Placeholders manquants dans {theme_path.name}: {sorted(missing)}\n")

    # Remplacer
    resolved = base_qss
    for k, v in mapping.items():
        resolved = resolved.replace(k, v)

    app.setStyleSheet(resolved)
