# type: ignore

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from board.board import Board
from board.exceptions import AlreadyInitializedError, AlreadyResolvedError, NotInitializedError


class Box(BaseModel):
    x: int
    y: int
    value: int


app = FastAPI()


class UseBoard:
    board: Board

    def __init__(self) -> None:
        self.board = Board()

    def getBoard(self) -> Board:
        return self.board

    def newBoard(self) -> Board:
        self.board = Board()
        return self.board


board = UseBoard()


@app.get("/")
def get_board() -> str:
    return board.getBoard().getJSON()


@app.post("/")
def set_box(box: Box) -> str:
    b = board.getBoard()
    b.setBox(box.x, box.y, box.value)
    return b.getJSON()


@app.get("/fill")
def get_fill(dif: str = "easy") -> str:
    b = board.getBoard()
    try:
        b.fill(dif)
    except AlreadyInitializedError as e:
        msg: str = e.args[0]
        return msg

    return b.getJSON()


@app.get("/reset")
def get_reset() -> str:
    b = board.newBoard()
    return b.getJSON()


@app.get("/resolve")
def get_resolve() -> str:
    b = board.getBoard()
    try:
        resolved = b.resolve()
        b.setBoard(b.boardToMatrix(resolved))
        b.setResolved(True)
    except (AlreadyResolvedError, NotInitializedError) as e:
        msg: str = e.args[0]
        return msg

    return b.getJSON()


@app.get("/verify")
def get_verify() -> bool:
    b = board.getBoard()
    return b.verify()


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)
