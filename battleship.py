from random import randint

####### Function definitions

def clear():
    for i in range(15):
        print ""

def blank_board(board):
    for x in range(rango):
        board.append(["O"] * rango)
    
def print_board(board):
    a = "#"
    global reveal
    for i in range(len(board)):
        a += " " + ABC[i]
    print a
    for i in range(len(board)):
        a = str(i)
        for j in range(len(board[0])):
            if board[i][j] == "=" and reveal == False:
                b = "O"
            else:
                b = board[i][j]
            a += " " + b
        print a

def deploy_ship(board, lon_y, lon_x):
    ship_y = randint(0, len(board) - lon_y)
    ship_x = randint(0, len(board[0]) - lon_x)
    vacio = False
    n = 0
    while vacio == False:
        n += 1
        vacio = True
        for y in range(lon_y):
            for x in range(lon_x):
                if board[ship_y+y][ship_x+x] == "=":
                    vacio = False
        if vacio == True:
            for y in range(lon_y):
                for x in range(lon_x):
                    board[ship_y+y][ship_x+x] = "="
        if n >= 100:
            global finish
            finish = False
            print "Can't deploy" + str(lon_y) + str(lon_x)
            break
            
def esnumero (num):
    es = False
    for i in NUM:
        if num == i:
            es = True
    return es

def esletra (letra):
    es = False
    for i in ABC:
        if letra.upper() == i:
            es = True
    return es
                
###### Preparando el tablero y deploying los ships

rango = 9
NUM = ["0","1","2","3","4","5","6","7","8","9"]
ABC = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
board = []
finish = False
reveal = False

while finish == False:
    board = []
    finish = True
    blank_board(board)
    deploy_ship(board,1,5)
    deploy_ship(board,4,1)
    deploy_ship(board,1,4)
    deploy_ship(board,1,3)
    deploy_ship(board,2,1)
    deploy_ship(board,1,3)

########## Game starts!!

turns = 100 # Maximum number of turns

clear()
clear()
print "########### HUNDIR LA FLOTA 1.0 ###########"
print ""
raw_input("Pulsa intro para jugar")
clear()
print_board(board)

## Empiezan los turnos
for turn in range(turns):
    
    clear()
    print "### Turno " + str(turn+1) + " ###"
    
    ## Entendiendo la INPUT
    entendido = False
    while entendido == False:
        entendido = True
    	guess = raw_input("Dispara:")
    	#CHEATS
        if guess == "revealall":
            reveal = not reveal
        elif guess == "quit":
            break
        # Entendiendo            
        if len(guess) < 2:
            print "No te he entendido. Intentalo de nuevo."
            entendido = False
        elif esnumero(guess[0]) and esletra(guess[1]):
        	guess_row = int(guess[0])
        	guess_col = ABC.index(guess[1].upper())
    	elif esnumero(guess[1]) and esletra(guess[0]):
        	guess_row = int(guess[1])
        	guess_col = ABC.index(guess[0].upper())
    	else:
       		print "No te he entendido. Intentalo de nuevo."
        	entendido = False
            
    ## SALIR
    if guess == "quit":
        break
        
    ## FUERA
    if guess_row < 0 or guess_row >= rango or guess_col < 0 or guess_col >= rango:
        print "Fuera del tablero."

    ## TOCADO
    elif board[guess_row][guess_col] == "=":
        print "Tocado!"
        board[guess_row][guess_col] = "X"
        
    ## REPETIDO
    elif board[guess_row][guess_col] == "." or board[guess_row][guess_col] == "X":
        print "Ya habías disparado aquí."
        
    ## AGUA
    else:
        print "Agua!"
        board[guess_row][guess_col] = "."
    
    ## Dibujamos el tablero y si es el ultimo turno GAME OVER
    print ""
    print_board(board)
    
    if turn == turns-1:
        print ""
        print ""
        print "GAME OVER"