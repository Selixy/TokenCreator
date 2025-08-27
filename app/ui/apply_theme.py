import re
import sys
from pathlib import Path
from PySide6.QtGui import QPalette, QColor

_PLACEHOLDER_RX = re.compile(r"\{\{[^}]+}}")

def _normalize_key(k: str) -> str:
    k = k.strip()
    if not k:
        return k
    # accepte "FILEBTN_TEXT" ou "{{FILEBTN_TEXT}}"
    inner = k.strip("{} \t")
    return f"{{{{{inner}}}}}"

def apply_theme(app, theme: str = "dark") -> None:
    candidates: list[Path] = []

    # PyInstaller
    if getattr(sys, "frozen", False):
        meipass = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
        candidates += [meipass / "styles", Path(sys.executable).parent / "styles"]

    # Développement
    here = Path(__file__).resolve().parent
    candidates += [here.parent / "styles", here / "styles"]

    # Trouver un dossier contenant base.qss
    base_dir = next((c for c in candidates if (c / "base.qss").exists()), None)
    if base_dir is None:
        sys.stderr.write("[WARN] Aucun fichier QSS trouvé, thème non appliqué\n")
        return

    base_qss_path = base_dir / "base.qss"
    base_qss = base_qss_path.read_text(encoding="utf-8")

    theme_path = base_dir / f"{theme}.colors.qss"
    mapping: dict[str, str] = {}

    if theme_path.exists():
        for line in theme_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith(("/*", "//", "#")):
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                mapping[_normalize_key(k)] = v.strip().rstrip(";")
    else:
        sys.stderr.write(f"[WARN] {theme_path.name} manquant, seul base.qss appliqué\n")

    # Vérifier les placeholders attendus par base.qss
    needed = set(_PLACEHOLDER_RX.findall(base_qss))
    missing = [ph for ph in needed if ph not in mapping]
    if missing:
        sys.stderr.write(f"[WARN] Placeholders manquants dans {theme_path.name if theme_path.exists() else '(absent)'}: {sorted(missing)}\n")

    # Remplacement (uniquement placeholders connus)
    def repl(m):
        ph = m.group(0)
        return mapping.get(ph, ph)  # laisse tel quel si manquant
    resolved = _PLACEHOLDER_RX.sub(repl, base_qss)

    # Appliquer le QSS global
    app.setStyleSheet(resolved)

    # set le font de l'app (notament la bar de titre)
    pal = app.palette()
    if theme.lower() == "dark":
        bg = QColor("#1f1f1f")
    else:
        bg = QColor("#f0f0f0")

    pal.setColor(QPalette.Window, bg)
    pal.setColor(QPalette.Base, bg)
    pal.setColor(QPalette.Button, bg)
    app.setPalette(pal)
