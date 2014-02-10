from random import randint

####### PARAMETROS

turns = 100 # Maximum number of turns
rango = 9
NUM = ["0","1","2","3","4","5","6","7","8","9"]
ABC = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
board = []
deployed = False
reveal = False
nada = "."
agua = "o"
barco = "="
tocado = "+"
hundido = "X"
codes = ["quit", "diagonal", "bombanuclear", "random"]


####### FUNCIONES GENERALES

def clear():
	for i in range(9):
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

def coord(sepermitencodes): #Recibe los cheats y las coordenadas
	global reveal
	entendido = False
	code = ""
	guess_row = 0
	guess_col = 0
	## Recibiendo la INPUT
	while entendido == False:
		entendido = True
		input = raw_input("Coordenadas:")
		#CHEATS
		if input == "revealall" and sepermitencodes:
			reveal = not reveal
		elif (input in codes) and sepermitencodes:
			code = input
			break
		# Entendiendo la INPUT
		if len(input) < 2:
			print "No te he entendido. Intentalo de nuevo."
			entendido = False
		elif esnumero(input[0]) and esletra(input[1]):
			guess_row = int(input[0])
			guess_col = ABC.index(input[1].upper())
		elif esnumero(input[1]) and esletra(input[0]):
			guess_row = int(input[1])
			guess_col = ABC.index(input[0].upper())
		else:
			print "No te he entendido. Intentalo de nuevo."
			entendido = False
	
	return [guess_col, guess_row, code]

####### TABLERO

def blank_board(board): #Crea un tablero en blanco
	for x in range(rango):
		board.append([nada] * rango)

def print_board(board): #Muestra el tablero
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

	def deploy(self, board):
		vacio = False
		n = 0
		
		while vacio == False:
			
			n += 1
			
			self.y = randint(0, len(board) - self.ver) #elijo un sitio al azar
			self.x = randint(0, len(board[0]) - self.hor)
			
			# Margenes de barco por defecto
			marg_izq = 1
			marg_dcha = 1
			marg_arr = 1
			marg_ab = 1
			# Margenes de barco para los extremos
			if self.x == 0:
				marg_izq = 0
			if self.x + self.hor == rango:
				marg_dcha = 0
			if self.y == 0:
				marg_arr = 0
			if self.y + self.ver == rango:
				marg_ab = 0
			
			vacio = True
			
			for j in range(self.ver+marg_arr+marg_ab): #miro si esta vacio
				for i in range(self.hor+marg_izq+marg_dcha):
					if board[self.y+j-marg_arr][self.x+i-marg_izq] == barco:
						vacio = False
			if vacio == True: #si esta vacio pongo el barco
				for j in range(self.ver):
					for i in range(self.hor):
						board[self.y+j][self.x+i] = barco
			
			if n >= 100: #si tarda mas de 100 --> no se puede
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
			if i == barco:
				break
		else:
			self.hundir(board)
	
	def hundir(self, board):
		for i in range(len(self.estado)): #Hundimos en el estado del barco
			self.estado[i] = hundido
		for j in range(self.ver): #Hundimos en el tablero
			for i in range(self.hor):
				board[self.y+j][self.x+i] = hundido
	
	def estaHundido(self):
		return self.estado[0] == hundido

class Flota (object):

	def __init__(self,ships):
		self.ships = ships

	def describe(self):
		for i in self.ships:
			i.describe()
	
	def find(self, m, n):
		for ship in self.ships:
			if ship.x<=m and ship.x+ship.hor>m and ship.y<=n and ship.y+ship.ver>n:
				return ship
	
	def findHitPoint(self, m, n):
		for ship in self.ships:
			if ship.x<=m and ship.x+ship.hor>m and ship.y<=n and ship.y+ship.ver>n:
				return max(m-ship.x, n-ship.y)
	
	def hit(self, m, n):
		self.find(m, n).hit(self.findHitPoint(m, n))
		return self.find(m, n)

###### Preparando el tablero y deploying los ships

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

####### RANKING

def anotar_ranking(turnos, nombre):
        ranking = open("ranking.txt","a")
        ranking.write("\n"+str(turnos)+" "+nombre)
        ranking.close()

def mostrar_ranking ():
        #leemos el ranking guardado
        ranking = open("ranking.txt","r")
        rank = []
        for line, data in enumerate(ranking):
                rank.append(data.split())
        ranking.close()
        #ordenamos el ranking
        for n, data in enumerate(rank):
                rank[n][0] = int(rank[n][0])
        rank.sort()
        #mostramos el ranking
        clear()
        
        print "RANKING"
        print ""
        print "#   TURNOS   NOMBRE"
        for n, item in enumerate(rank):
                print str(n) + "   "+str(rank[n][0])+"       "+rank[n][1]

####### JUGADA

def jugada (guess_col, guess_row, write):

	## FUERA
	if guess_row < 0 or guess_row >= rango or guess_col < 0 or guess_col >= rango:
		if write: print "Fuera del tablero."

	## TOCADO
	elif board[guess_row][guess_col] == barco:
		flota.hit(guess_col, guess_row)
		if flota.find(guess_col, guess_row).estaHundido():
			if write: print "Tocado y hundido!"
		else:
			if write: print "Tocado!"
			board[guess_row][guess_col] = tocado

	## REPETIDO
	elif board[guess_row][guess_col] == agua or board[guess_row][guess_col] == tocado or board[guess_row][guess_col] == hundido:
		if write: print "Ya habias disparado aqui."

	## AGUA
	else:
		if write: print "Agua!"
		board[guess_row][guess_col] = agua

###### OTRAS JUGADAS

def bomba (r):
	print "Donde?"
	[x, y, code] = coord(False)
	centro = [x,y]
	for i in range(r):
		for j in range(r):
			if not [i,j] == [0,0] and not [i,j] == [r-1,r-1] and not [i,j] == [r-1,0] and not [i,j] == [0,r-1]:
				jugada(centro[0]-(r-1)/2+i, centro[1]-(r-1)/2+j, False)
	print "Bomba va!"
				
def diagonal ():
	for i in range(rango):
		jugada(i,i,False)
	print "Diagonal!"

def bombrandom ():
        for i in range(10):
                jugada(randint(0, len(board)),randint(0, len(board)),False)
        print "Bombardeo!"

########## EMPIEZA EL JUEGO

clear()
clear()
clear()
clear()
print "########### HUNDIR LA FLOTA 3.0 ###########"
print ""
modo = raw_input("Pulse intro para jugar ")

##### MODO JUGAR
if modo == "":
        
        clear()
        print_board(board)
        print ""
        flota.describe()

        ## Empiezan los turnos
        for turn in range(turns):

                clear()
                print "### Turno " + str(turn+1) + " ###"
                
                [guess_col, guess_row, code] = coord(True)
                
                ## SALIR
                if code == "quit":
                        break
                
                ## JUGADA
                if code == "diagonal":
                        diagonal()
                elif code == "bombanuclear":
                        bomba(5)
                elif code == "random":
                        bombrandom()
                else:
                        jugada(guess_col, guess_row, True)
                        
                ## Dibujar
                print ""
                print_board(board)
                print ""
                flota.describe()
                        
                ## FIN DEL JUEGO
                for ship in flota.ships:
                        if not ship.estaHundido():
                                if turn == turns-1:
                                        print ""
                                        print ""
                                        print "GAME OVER"
                                        raw_input()
                                break
                else:
                        print ""
                        print ""
                        print "HAS GANADO!!!"
                        clear()
                        nombre = raw_input("Introduce tu nombre:")
                        anotar_ranking(turn, nombre)
                        mostrar_ranking()
                        break

##### MODO RANKING
elif modo == "r":
        mostrar_ranking()


                
