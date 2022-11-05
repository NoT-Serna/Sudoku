import http.client
from typing import List, Tuple, Literal, Dict
import json

from .exceptions import NotInitializedError, AlreadyInitializedError, AlreadyResolvedError


class Board():
    board: List[List[int]] = []
    original: List[List[int]] = []
    difficulty: Literal["easy", "medium", "hard"] = "easy"
    filled = False
    resolved = False

    def __init__(self) -> None:
        self.board = [[0 for j in range(9)] for i in range(9)]
        self.original = [[0 for j in range(9)] for i in range(9)]

    def matrixToBoard(self) -> str:
        result = ""
        for row in self.original:
            for box in row:
                result += str(box) if box != 0 else "."

        return result

    def boardToMatrix(self, board: str) -> List[List[int]]:
        result = [[0 for j in range(9)] for i in range(9)]
        cont = 0
        for i in range(9):
            for j in range(9):
                result[i][j] = int(board[cont]) if board[cont] != "." else 0
                cont += 1

        return result

    def fill(self, dif: str) -> None:
        if not self.filled:
            if dif not in ["easy", "medium", "hard"]:
                raise ValueError
            else:
                conn = http.client.HTTPSConnection("sudoku-generator1.p.rapidapi.com")

                headers = {
                    'X-RapidAPI-Key': "eefc2721f6mshceeb0e5cf49acf9p1c83d2jsn8c93826ed3e4",
                    'X-RapidAPI-Host': "sudoku-generator1.p.rapidapi.com"
                }

                conn.request("GET", f"/sudoku/generate?difficulty={dif}", headers=headers)
                print(f"/sudoku/generate/?difficulty={dif}")
                res = conn.getresponse()
                data = res.read()

                puzzle: str = json.loads(data)["puzzle"]  # type: ignore
                cont = 0
                for i in range(9):
                    for j in range(9):
                        self.original[i][j] = int(puzzle[cont]) if puzzle[cont] != "." else 0
                        self.board[i][j] = int(puzzle[cont]) if puzzle[cont] != "." else 0
                        cont += 1

                self.filled = True

        else:
            raise AlreadyInitializedError

    def setBox(self, x: int, y: int, v: int) -> None:
        if v >= 0 and v <= 9:
            self.board[y][x] = v
        else:
            raise ValueError

    def setBoard(self, board: List[List[int]]) -> None:
        self.board = board

    def setResolved(self, bool: bool) -> None:
        self.resolved = bool

    def getJSON(self) -> str:
        json = {"difficulty": self.difficulty, "board": self.board, "original": self.original}
        return str(json)

    def hint(self) -> Tuple[int, int, int]:
        # da una pista, devuelve el numero y su posicion, no lo coloca
        pass

    def resolve(self) -> str:
        if not self.resolved and self.filled:
            conn = http.client.HTTPSConnection("sudoku-generator1.p.rapidapi.com")

            headers = {
                'X-RapidAPI-Key': "eefc2721f6mshceeb0e5cf49acf9p1c83d2jsn8c93826ed3e4",
                'X-RapidAPI-Host': "sudoku-generator1.p.rapidapi.com"
            }

            conn.request("GET", f"/sudoku/solve?puzzle={self.matrixToBoard()}", headers=headers)

            print(self.matrixToBoard())
            res = conn.getresponse()
            data = res.read()

            return str(json.loads(data)["solution"])  # type: ignore

        elif self.resolved:
            raise AlreadyResolvedError
        else:
            raise NotInitializedError

    def verify(self) -> bool:
        # retorna true si el tablero esta completo y es correcto
        solution_str = self.resolve()
        solution = self.boardToMatrix(solution_str)

        return solution == self.board

    def partialVerify(self) -> bool:
        # retorna true si en lo que va completado del tablero
        # no hay ningun error
        pass
