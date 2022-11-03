class NotFilledError(Exception):
    """"No se ha inicializado el tablero, aun no se pueden realizar cambios"""
    pass


class FullBoard(Exception):
    """El tablero esta resuelto, no hay más pistas disponibles"""
    pass
