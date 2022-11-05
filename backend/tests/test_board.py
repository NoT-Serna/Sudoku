import pytest

from board.board import Board
from board.exceptions import AlreadyResolvedError


@pytest.fixture(scope="class")
def board() -> Board:
    return Board()


@pytest.mark.usefixtures("board")
class TestBoard:

    def test_init(self, board: Board) -> None:
        assert (len(board.board) == 9 and len(board.board[0]) == 9
                and 0 in board.board[0])

    def test_set_box(self, board: Board) -> None:
        board.setBox(0, 0, 1)
        board.setBox(8, 0, 2)
        board.setBox(0, 8, 3)
        board.setBox(8, 8, 4)

        assert board.board[0][0] == 1
        assert board.board[0][8] == 2
        assert board.board[8][0] == 3
        assert board.board[8][8] == 4

        # revisar el tipo de error
        with pytest.raises(IndexError):
            board.setBox(9, 0, 0)

        with pytest.raises(IndexError):
            board.setBox(0, 9, 0)

        with pytest.raises(ValueError):
            board.setBox(0, 0, 10)

        with pytest.raises(ValueError):
            board.setBox(0, 0, -1)

    def test_get_json(self, board: Board) -> None:
        board.fill("easy")
        dict = board.getJSON()

        assert (dict["board"] == board.board and dict["original"] == board.original  # type: ignore
                and dict["difficulty"] == "easy")  # type: ignore

    @pytest.mark.xfail(reason="El test esta mal hecho")
    def test_verify(self, board: Board) -> None:
        # esta mal porque toca construir tambien board.original y revisar que
        # el verify se salte el error de NotInitializedError
        wrong_board = []
        # un tablero lleno de ceros es incorrecto
        zeros = [[0 for j in range(9)] for i in range(9)]
        wrong_board.append(zeros)

        correct_board = [
            # ejemplo de un tablero lleno y correcto
            [[9, 6, 3, 1, 7, 4, 2, 5, 8],
             [1, 7, 8, 3, 2, 5, 6, 4, 9],
             [2, 5, 4, 6, 8, 9, 7, 3, 1],
             [8, 2, 1, 4, 3, 7, 5, 9, 6],
             [4, 9, 6, 8, 5, 2, 3, 1, 7],
             [7, 3, 5, 9, 6, 1, 8, 2, 4],
             [5, 8, 9, 7, 1, 3, 4, 6, 2],
             [3, 1, 7, 2, 4, 6, 9, 8, 5],
             [6, 4, 2, 5, 9, 8, 1, 7, 3]],
        ]

        # se modifica el tablero correcto para que ya no lo sea
        failing = correct_board[0]
        failing[8][4] = 1
        failing[8][6] = 9

        failing[0][4] = 3
        failing[0][2] = 7
        wrong_board.append(failing)

        for b in wrong_board:
            board.board = b
            assert not board.verify()

        for b in correct_board:
            board.board = b
            assert board.verify()

    @pytest.mark.xfail(reason="No esta implementado")
    def test_partialVerify(self, board: Board) -> None:

        correct_partial_board = [
            # ejemplo de un tablero casi lleno y correcto
            [[9, 6, 3, 1, 7, 4, 2, 5, 8],
             [1, 0, 8, 3, 2, 5, 6, 4, 9],
             [2, 5, 4, 6, 8, 9, 7, 0, 1],
             [8, 2, 1, 4, 3, 7, 5, 9, 6],
             [4, 9, 6, 8, 5, 2, 3, 1, 7],
             [7, 3, 5, 0, 6, 1, 8, 2, 4],
             [5, 8, 9, 7, 1, 3, 4, 6, 2],
             [3, 0, 7, 2, 4, 6, 0, 8, 5],
             [6, 4, 2, 5, 9, 8, 1, 7, 3]],
            # ejemplo de un tablero casi vacio y correcto
            [[1, 2, 3, 4, 5, 6, 7, 8, 9],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        ]

        incorrect_partial_board = [
            # ejemplo de un tablero casi lleno e incorrecto
            [[9, 4, 3, 1, 7, 4, 2, 5, 8],
             [1, 4, 8, 3, 2, 5, 6, 4, 9],
             [2, 5, 4, 6, 8, 0, 7, 3, 1],
             [8, 2, 1, 4, 3, 7, 5, 9, 6],
             [4, 9, 6, 8, 5, 2, 3, 1, 7],
             [7, 3, 0, 2, 6, 1, 8, 2, 4],
             [5, 8, 9, 7, 1, 3, 4, 1, 2],
             [3, 2, 7, 2, 4, 6, 2, 0, 5],
             [6, 4, 0, 5, 9, 8, 1, 7, 3]],
            # ejemplo de un tablero casi vacio e incorrecto
            [[1, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0, 0, 0, 0]],
        ]
        zeros = [[0 for j in range(9)] for i in range(9)]
        correct_partial_board.append(zeros)

        for b in correct_partial_board:
            board.board = b
            assert board.partialVerify()

        for b in incorrect_partial_board:
            board.board = b
            assert not board.partialVerify()

    @pytest.mark.xfail(reason="No esta implementado")
    def test_hint(self, board: Board) -> None:
        with pytest.raises(AlreadyResolvedError):
            # ejemplo de tablero lleno
            board.board = [[9, 6, 3, 1, 7, 4, 2, 5, 8],
                           [1, 7, 8, 3, 2, 5, 6, 4, 9],
                           [2, 5, 4, 6, 8, 9, 7, 3, 1],
                           [8, 2, 1, 4, 3, 7, 5, 9, 6],
                           [4, 9, 6, 8, 5, 2, 3, 1, 7],
                           [7, 3, 5, 9, 6, 1, 8, 2, 4],
                           [5, 8, 9, 7, 1, 3, 4, 6, 2],
                           [3, 1, 7, 2, 4, 6, 9, 8, 5],
                           [6, 4, 2, 5, 9, 8, 1, 7, 3]]
            board.hint()

        # ejemplo de tablero medio lleno y correcto
        board.board = [[1, 2, 3, 6, 8, 0, 0, 0, 0],
                       [4, 5, 6, 7, 0, 0, 0, 0, 0],
                       [7, 8, 9, 0, 0, 0, 0, 0, 0],
                       [2, 3, 0, 0, 0, 0, 0, 0, 0],
                       [9, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0], ]

        box = board.hint()
        board.setBox(*box)

        assert board.partialVerify()

    @pytest.mark.xfail(reason="mientras usemos el API no se puede probar")
    def test_resolve(self, board: Board) -> None:
        board.fill("easy")
        board.resolve()
        assert board.verify()

    @pytest.mark.skip(reason="mientras usemos el API no se puede probar")
    def test_fill(self, board: Board) -> None:
        # toca probar si se le manda mal la dificultad
        pass
