from functools import partial
from logic.fichier import action_nouveau, action_ouvrir, action_quitter

def setup_menus(window) -> None:
    """
    Branche les menus de window.topBar/topMenu sur la logique.
    Ne mettre AUCUNE logique ici, juste le câblage.
    """
    window.actions = window.topBar.topMenu.init_file_menu(
        on_new  = partial(action_nouveau, window),
        on_open = partial(action_ouvrir, window),
        on_quit = action_quitter
    )
