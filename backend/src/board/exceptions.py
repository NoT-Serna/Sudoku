class NotInitializedError(Exception):
    """"No se ha inicializado el tablero, aun no se pueden realizar cambios"""

    def __init__(self, *args: object) -> None:
        super().__init__("El tablero no ha sido inicializado")


class AlreadyInitializedError(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__("El tablero ya fue inicializado")


class AlreadyResolvedError(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__("El tablero ya fue resuelto")
