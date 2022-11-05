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
    board: Board = None

    def __init__(self) -> None:
        self.board = Board()

    def getBoard(self) -> Board:
        return self.board

    def newBoard(self) -> None:
        self.board = Board()
        return self.board


board = UseBoard()


@app.get("/")
def read_root():
    return board.getBoard().getJSON()


@app.post("/")
def set_box(box: Box):
    b = board.getBoard()
    b.setBox(box.x, box.y, box.value)
    return b.getJSON()


@app.get("/fill")
def read_root(dif="easy"):
    b = board.getBoard()
    try:
        b.fill(dif)
    except AlreadyInitializedError as e:
        return e.args[0]

    return b.getJSON()


@app.get("/reset")
def read_root():
    b = board.newBoard()
    return b.getJSON()


@app.get("/resolve")
def read_root():
    b = board.getBoard()
    try:
        resolved = b.resolve()
        b.setBoard(b.boardToMatrix(resolved))
        b.setResolved(True)
    except (AlreadyResolvedError, NotInitializedError) as e:
        return e.args[0]

    return b.getJSON()


@app.get("/verify")
def verify():
    b = board.getBoard()
    return b.verify()


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)
