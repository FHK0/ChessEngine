

#Açıklama ekle

import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15

IMAGES = {}


def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE,SQ_SIZE))




def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gameState = ChessEngine.GameState()
    validMoves = gameState.getValidMoves()
    moveMade = False #Hareketin yapılıp yapılmadığını saptayan flag


    loadImages() #while döngüsünden önce bir kerelik yükleme yapılır.

    running = True
    sqSelected = () #oyuncunun hangi kareyi seçtiğinin takibi
    playerClicks = [] #oyuncunun tıklamalarının takibi


    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col): #eğer oyuncu tıkladığı kareye bir daha tıklarsa seçili karele seçilmemiş hale geçer.
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gameState.board)
                    print(move.getChessNotation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gameState.makeMove(validMoves[i])
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # Z tuşuna basınca geri al
                    gameState.undoMove()
                    moveMade = True


        if moveMade:
            validMoves = gameState.getValidMoves()
            moveMade = False

        drawGameState(screen, gameState)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gameState):
    drawBoard(screen)
    drawPieces(screen, gameState.board)

"""
Oyun Tahtasını çizer.
"""
def drawBoard(screen):
    colors = [p.Color(235, 235, 208), p.Color(119, 148, 85)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c* SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

"""
Oyun Taşlarını çizer.
"""
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))



if __name__ == "__main__":
    main()
