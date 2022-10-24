class Board():
    board = []
    
    def __init__(self):
        for i in range(9):
            row = []
            for j in range(9):
                row.append(0)
            self.board.append(row)
            
    def fill(self, dif):
        pass
    
    def setBox(self, x, y, v):
        pass
    
    def getJSON(self):
        pass
    
    def hint(self):
        pass
    
    def resolve(self):
        pass
    
    def verify(self):
        pass
            
    
