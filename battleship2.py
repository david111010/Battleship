from random import randint

####### FUNCIONES GENERALES

def clear():
    for i in range(10):
        print ""

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

####### TABLERO

def blank_board(board):
	for x in range(rango):
		board.append([nada] * rango)

def print_board(board):
	a = "#"
	global reveal
	for i in range(len(board)):
		a += " " + ABC[i]
	print a
	for i in range(len(board)):
		a = str(i)
		for j in range(len(board[0])):
			if board[i][j] == barco and reveal == False:
				b = nada
			else:
				b = board[i][j]
			a += " " + b
		print a

####### BARCOS

class Ship (object):

	x = 0
	y = 0

	def __init__(self, name, hor, ver):
		self.name = name
		self.hor = hor
		self.ver = ver
		self.estado = []
		for i in range(max(hor, ver)):
			self.estado.append(barco)
		print self.estado

	def deploy(self, board):
		self.y = randint(0, len(board) - self.ver)
		self.x = randint(0, len(board[0]) - self.hor)
		vacio = False
		n = 0
		while vacio == False:
			n += 1
			vacio = True
			for j in range(self.ver):
				for i in range(self.hor):
					if board[self.y+j][self.x+i] == barco:
						vacio = False
			if vacio == True:
				for j in range(self.ver):
					for i in range(self.hor):
						board[self.y+j][self.x+i] = barco
			if n >= 100:
				global deployed
				deployed = False
				print "Can't deploy", self.name, self.hor, self.ver, "in", self.x, ABC[self.y]
				break

	def describe(self):
		print self.name," / ", "Hor:", self.hor, "Ver:", self.ver, " / ",
		if reveal == True or self.estaHundido():
			print " ".join(self.estado)
		else:
			for i in range(max(self.hor,self.ver)):
				if i < self.estado.count(tocado):
					print tocado,
				else:
					print barco,
			print

	def hit(self, m):
		self.estado[m] = tocado
		for i in self.estado:
			if i == barco: #Si queda algo de barco sin tocar salimos
				return False 
				break
		else: #Si todo esta tocado, hundimos
			self.hundir(board)
			return True # TRUE si TOCADO Y HUNDIDO    FALSE si TOCADO
	
	def hundir(self, board):
		for i in range(len(self.estado)): #Hundimos en el estado del barco
			self.estado[i] = hundido
		for j in range(self.ver): #Hundimos en el tablero
			for i in range(self.hor):
				board[self.y+j][self.x+i] = hundido
	
	def estaHundido(self):
		return self.estado[0]==hundido

class Flota (object):

	def __init__(self,ships):
		self.ships = ships

	def describe(self):
		for i in self.ships:
			i.describe()
	
	def find(self, m, n):
		for ship in self.ships:
			if ship.x<=m and ship.x+ship.hor>=m and ship.y<=n and ship.y+ship.ver>=n:
				return ship
	
	def findHitPoint(self, m, n):
		for ship in self.ships:
			if ship.x<=m and ship.x+ship.hor>=m and ship.y<=n and ship.y+ship.ver>=n:
				return max(m-ship.x, n-ship.y)
	
	def hit(self, m, n):
		self.find(m, n).hit(self.findHitPoint(m, n))
		return self.find(m, n)

###### Preparando el tablero y deploying los ships

rango = 9
NUM = ["0","1","2","3","4","5","6","7","8","9"]
ABC = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
board = []
deployed = False
reveal = False
nada = "O"
agua = "."
barco = "="
tocado = "+"
hundido = "X"

## Deploying Barcos

ship1 = Ship("Portaaviones",1,5)
ship2 = Ship("Yate",3,1)
ship3 = Ship("Pesquero",1,3)
ship4 = Ship("Barquica",1,2)
ship5 = Ship("Barca hinchable",1,1)

flota = Flota([ship1, ship2, ship3, ship4, ship5])

while deployed == False:
	board = []
	deployed = True
	blank_board(board)
	ship1.deploy(board)
	ship2.deploy(board)
	ship3.deploy(board)
	ship4.deploy(board)
	ship5.deploy(board)

########## Game starts!!

turns = 10 # Maximum number of turns

clear()
clear()
print "########### HUNDIR LA FLOTA 2.0 ###########"
print ""
raw_input("Pulsa intro para jugar")
clear()
print_board(board)
print ""
flota.describe()

## Empiezan los turnos
for turn in range(turns):

	clear()
	print "### Turno " + str(turn+1) + " ###"

	## Recibiendo la INPUT
	entendido = False
	while entendido == False:
		entendido = True
		guess = raw_input("Dispara:")
		#CHEATS
		if guess == "revealall":
			reveal = not reveal
		elif guess == "quit":
			break
		# Entendiendo la INPUT
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
	elif board[guess_row][guess_col] == barco:
		flota.hit(guess_col, guess_row)
		if flota.find(guess_col, guess_row).estaHundido():
			print "Tocado y hundido!"
		else:
			print "Tocado!"
			board[guess_row][guess_col] = tocado

	## REPETIDO
	elif board[guess_row][guess_col] == agua or board[guess_row][guess_col] == tocado:
		print "Ya habias disparado aqui."

	## AGUA
	else:
		print "Agua!"
		board[guess_row][guess_col] = agua

	## Dibujamos el tablero y si es el ultimo turno GAME OVER
	print ""
	print_board(board)
	print ""
	flota.describe()

	if turn == turns-1:
		print ""
		print ""
		print "GAME OVER"