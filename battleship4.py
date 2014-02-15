from random import randint
import time

####### PARAMETROS

turns = 100 # Maximum number of turns
rango = 7
NUM = ["0","1","2","3","4","5","6","7","8","9"]
ABC = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
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
        return num in NUM

def esletra (letra):
	return letra.upper() in ABC

def coord(hor, ver, codesallowed): #Recibe los cheats y las coordenadas
	global reveal
	entendido = False
	code = ""
	guess_x = 0
	guess_y = 0
	while entendido == False:
		entendido = True
		input = raw_input("Coordenadas:")
		#CHEATS
		if input == "revealall" and codesallowed:
			reveal = not reveal
		elif (input in codes) and codesallowed:
			code = input
			break
		# Entendiendo la INPUT
		if len(input) < 2:
			print "No te he entendido. Intentalo de nuevo."
			entendido = False
		elif esnumero(input[0]) and esletra(input[1]):
			guess_y = int(input[0])
			guess_x = ABC.index(input[1].upper())
		elif esnumero(input[1]) and esletra(input[0]):
			guess_y = int(input[1])
			guess_x = ABC.index(input[0].upper())
		else:
			print "No te he entendido. Intentalo de nuevo."
			entendido = False
		if guess_y+ver > rango or guess_x+hor > rango:
			print "Fuera del tablero. Intentalo de nuevo."
			entendido = False
	
	return [guess_x, guess_y, code]

####### TABLERO

class Board (object):
	
	def __init__(self, fleet, name):
		self.fleet = fleet
		fleet.board = self
		self.name = name
		self.grid = []
		for x in range(rango):
			self.grid.append([nada] * rango)

	def clear(self): #Vacia el tablero
		self.grid = []
		for x in range(rango):
			self.grid.append([nada] * rango)

	def show(self): #Muestra el tablero
		print "%%%", self.name, "%%%"
		print ""
		a = "#"
		global reveal
		for i in range(len(self.grid)):
			a += " " + ABC[i]
		print a
		for i in range(len(self.grid)):
			a = str(i)
			for j in range(len(self.grid[0])):
				if self.grid[i][j] == barco and reveal == False and self.fleet == cmpfleet:
					b = nada
				else:
					b = self.grid[i][j]
				a += " " + b
			print a,"        ",
			#muestro la flota tambien
			hueco = (rango-len(self.fleet.ships))/2
			if i-hueco < len(self.fleet.ships) and i-hueco >= 0:
				self.fleet.ships[i-hueco].describe()
			else:
				print

	def estaLibre(self, startX, startY, Ax, Ay):
		libre = True
		for j in range(Ay):
				for i in range(Ax):
					if self.grid[startY+j][startX+i] == barco:
						libre = False
						break
				if libre == False:
					break
		return libre


##### FLEET
	
class Fleet (object):

	def __init__(self, ships):
		self.ships = ships
		self.board = []
		for ship in ships:
			ship.fleet = self

	def describe(self):
		for i in self.ships:
			i.describe()
	
	def find(self, m, n):
		for ship in self.ships:
			if ship.x<=m and ship.x+ship.hor>m and ship.y<=n and ship.y+ship.ver>n:
				return ship

	def hit(self, m, n):
		ship = self.find(m, n)
		ship.hit(max(m-ship.x, n-ship.y))
		
	def randomdeploy(self):
		for ship in self.ships:
			ship.randomdeploy()

	def deploy(self):
		for ship in self.ships:
			self.board.show()
			clear()
			ship.deploy()
			print ""
		clear()
		print "Flota colocada!"
		print ""
		self.board.show()


####### SHIPS

class Ship (object):

	def __init__(self, name, hor, ver):
		self.name = name
		self.hor = hor
		self.ver = ver
		self.fleet = []
		self.board = []
		self.estado = []
		for i in range(max(hor, ver)):
			self.estado.append(barco)

	def randomdeploy(self):
		vacio = False
		n = 0
		
		for i in range(100):
			
			self.y = randint(0, len(self.fleet.board.grid) - self.ver) #elijo un sitio al azar
			self.x = randint(0, len(self.fleet.board.grid[0]) - self.hor)
			
			# Margenes de barco
			marg_izq = min(1,self.x)
			marg_dcha = min(1, rango - self.x - self.hor)
			marg_arr = min(1,self.y)
			marg_ab = min(1, rango - self.y - self.ver)

			# Miro si la posicion esta libre
			vacio = self.fleet.board.estaLibre(self.x-marg_izq, self.y-marg_arr, self.hor+marg_izq+marg_dcha, self.ver+marg_arr+marg_ab)
			if vacio: break
			
		else:
			global deployed
			deployed = False
			vacio = False
			print "ERROR: Can't deploy", self.name, self.hor, self.ver, "in", self.x, ABC[self.y]

		if vacio: #si esta vacio pongo el barco
			for j in range(self.ver):
				for i in range(self.hor):
					self.fleet.board.grid[self.y+j][self.x+i] = barco
	def deploy(self):

		deployed = False

		while deployed == False:
			# Donde lo pongo?
			print "Donde quieres colocar el", self.name, "?"
			[self.x, self.y, codes] = coord(self.hor, self.ver, False)
				
			# Margenes de barco
			marg_izq = min(1,self.x)
			marg_dcha = min(1, rango - self.x - self.hor)
			marg_arr = min(1,self.y)
			marg_ab = min(1, rango - self.y - self.ver)

			# Miro si la posicion esta libre
			vacio = self.fleet.board.estaLibre(self.x-marg_izq, self.y-marg_arr, self.hor+marg_izq+marg_dcha, self.ver+marg_arr+marg_ab)
			
			if vacio == True: #si esta vacio pongo el barco
					deployed = True
					for j in range(self.ver):
						for i in range(self.hor):
							self.fleet.board.grid[self.y+j][self.x+i] = barco
					print self.name+" deployed!"
					clear()
			else:
				print "Posicion no valida"

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
			self.hundir()
	
	def hundir(self):
		for i in range(len(self.estado)): #Hundimos en el estado del barco
			self.estado[i] = hundido
		for j in range(self.ver): #Hundimos en el tablero
			for i in range(self.hor):
				self.fleet.board.grid[self.y+j][self.x+i] = hundido
	
	def estaHundido(self):
		return self.estado[0] == hundido

###### PREPARING BOARDS

## DEPLOYING COMPUTER SHIPS

cmpship1 = Ship("PortaavionesCMP",1,5)
cmpship2 = Ship("YateCMP",3,1)
cmpship3 = Ship("PesqueroCMP",1,3)
cmpship4 = Ship("BarquicaCMP",1,2)
cmpship5 = Ship("Barca hinchableCMP",1,1)

cmpfleet = Fleet([cmpship1, cmpship2, cmpship3, cmpship4, cmpship5])

while deployed == False:
	deployed = True
	cmpboard = Board(cmpfleet, "Tablero enemigo")
	cmpfleet.randomdeploy()

## USER SHIPS

usrship1 = Ship("PortaavionesUSR",1,5)
usrship2 = Ship("YateUSR",3,1)
usrship3 = Ship("PesqueroUSR",1,3)
usrship4 = Ship("BarquicaUSR",1,2)
usrship5 = Ship("Barca hinchableUSR",1,1)

usrfleet = Fleet([usrship1, usrship2, usrship3, usrship4, usrship5])

usrboard = Board(usrfleet, "Mi tablero")

boards = [usrboard, cmpboard]

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

def jugada (guess_col, guess_row, board, write):

	## FUERA
	if guess_row < 0 or guess_row >= rango or guess_col < 0 or guess_col >= rango:
		if write: print "Fuera del tablero."

	## TOCADO
	elif board.grid[guess_row][guess_col] == barco:
		board.fleet.hit(guess_col, guess_row)
		if board.fleet.find(guess_col, guess_row).estaHundido():
			if write: print "Tocado y hundido!"
		else:
			if write: print "Tocado!"
			board.grid[guess_row][guess_col] = tocado

	## REPETIDO
	elif board.grid[guess_row][guess_col] in [agua, tocado, hundido]:
		if write: print "Ya habias disparado aqui."

	## AGUA
	else:
		if write: print "Agua!"
		board.grid[guess_row][guess_col] = agua

###### OTRAS JUGADAS

def bomba (r):
	print "Donde?"
	[x, y, code] = coord(1,1,False)
	centro = [x,y]
	for i in range(r):
		for j in range(r):
			if not [i,j] in [[0,0],[r-1,r-1],[r-1,0],[0,r-1]]:
				jugada(centro[0]-(r-1)/2+i, centro[1]-(r-1)/2+j, cmpboard, False)
	print "Bomba va!"
				
def diagonal ():
	for i in range(rango):
		jugada(i,i,cmpboard, False)
	print "Diagonal!"

def bombrandom ():
	for i in range(10):
		jugada(randint(0, rango), randint(0, rango), cmpboard, False)
	print "Bombardeo!"

####### ARTIFICIAL INTELLIGENCE
def artif_int():
        for j in range(rango):
                for i in range(rango):
                        if usrboard.grid[j][i] == tocado:
                                for Aj in range(6):
                                        if j+1+Aj<=rango:
                                                if usrboard.grid[j+1+Aj][i] in [nada, barco]:
                                                        return [i, j+1+Aj]
                                                elif usrboard.grid[j+1+Aj][i] == agua:
                                                        if j-1>=0:
                                                                if usrboard.grid[j-1][i] != agua:
                                                                        return [i, j-1]
                                                        else:
                                                                break

                                for Ai in range(6):
                                        if i+1+Ai<=rango:
                                                if usrboard.grid[j][i+1+Ai] in [nada, barco]:
                                                        return [i+1+Ai, j]
                                                elif usrboard.grid[j][i+1+Ai] == agua:
                                                        if i-1>=0:
                                                                if usrboard.grid[j][i-1] != agua:
                                                                        return [i-1, j]
                                                        else:
                                                                break
        else:
                valido = False
                while not valido:
                        x = randint(0,rango-1)
                        y = randint(0,rango-1)
                        if usrboard.grid[y][x] in [nada, barco]:
                                valido = True
                                if x > 0:
                                        if hundido == usrboard.grid[y][x-1]:
                                                valido = False
                                if x < rango-1:
                                        if hundido == usrboard.grid[y][x+1]:
                                                valido = False
                                if y > 0:
                                        if hundido == usrboard.grid[y-1][x]:
                                                valido = False
                                if y < rango-1:
                                        if hundido == usrboard.grid[y+1][x]:
                                                valido = False
                else:
                        return [x,y]
	
########## EMPIEZA EL JUEGO

clear()
clear()
clear()
clear()
print "########### HUNDIR LA FLOTA 4.0 ###########"
print ""
modo = raw_input("Pulse intro para jugar ")

##### MODO JUGAR
if modo == "":

	#Deploying user ships
	clear()
	print "Donde quieres poner los barcos?"
	clear()
	reveal = True
	usrfleet.deploy()
	reveal = False

	#Comienza la guerra
	print ""
	raw_input("Comienza la guerra!")
	print ""
	cmpboard.show()
	print ""

	## Empiezan los turnos
	for turn in range(turns):

		print ""
		#### USER TURN
		print "### Turno " + str(turn+1) + " USER ###"
		print "Dispara!"
		[guess_col, guess_row, code] = coord(1,1,True)
		
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
			jugada(guess_col, guess_row, cmpboard, True)

		print ""
		time.sleep(0.01)
		print "### Turno " + str(turn+1) + " COMP ###"

		##### COMP TURN
		time.sleep(0.01)
		[x, y] = artif_int()
		print ABC[x],y
		time.sleep(0.01)
		jugada(x , y, usrboard, True)
		print ""
		time.sleep(0.01)

		## Dibujar
		usrboard.show()
		print ""
		cmpboard.show()
			
		## FIN DEL JUEGO
		for ship in cmpfleet.ships:
			if not ship.estaHundido():
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


		
