from typing import List, Tuple, Literal


class Board():
    board: List[List[int]] = []
    original: List[List[int]] = []
    difficulty: Literal["easy", "medium", "hard"] = "easy"
    filled = False

    def __init__(self) -> None:
        self.board = [[0 for j in range(9)] for i in range(9)]
        self.original = [[0 for j in range(9)] for i in range(9)]

    def fill(self, dif: Literal["easy", "medium", "hard"]) -> None:
        pass

    def setBox(self, x: int, y: int, v: int) -> None:
        pass

    def getJSON(self) -> str:
        pass

    def hint(self) -> Tuple[int, int, int]:
        # da una pista, devuelve el numero y su posicion, no lo coloca
        pass

    def resolve(self) -> None:
        # resuelve todo el tablero
        pass

    def verify(self) -> bool:
        # retorna true si el tablero esta completo y es correcto
        pass

    def partialVerify(self) -> bool:
        # retorna true si en lo que va completado del tablero
        # no hay ningun error
        pass
