import time
from adafruit_servokit import ServoKit

# Indices para arreglos
HORIZONTAL = 0
VERTICAL = 1
KNEE = 2
RIGHT_FRONT = 0
RIGHT_MID = 1
RIGHT_BACK = 2
LEFT_FRONT = 3
LEFT_MID = 4
LEFT_BACK = 5

# Grados a levantar pata
VERTICAL_RIGHT_RISE = 35
VERTICAL_LEFT_RISE = -35
VERTICAL_RETURN_TO_BASE = 0

# Grados a girar pata
HORIZONTAL_TURN_CLOCKWISE = 30
HORIZONTAL_TURN_COUNTERCW = -30
HORIZONTAL_RIGHT_FORWARD = 12
HORIZONTAL_LEFT_FORWARD = -12
HORIZONTAL_RETURN_TO_BASE = 0

# Grados para rodillas
KNEE_BASE = 90
KNEE_LEFT_EXTENSION = 30
KNEE_RIGHT_EXTENSION = -30

	# Las patas izquierdas y derechas estan reflejadas
	# por lo que muchas constantes son opuestas

# Tiempos de espera (segundos)
DELAY_TURN = 0.1
DELAY_FORWARD = 0.2

# EXPERIMENTAL
# Indices para arreglos
COMPENSATE_VERT_FORWARD = 0
COMPENSATE_VERT_BACKWARD = 1
COMPENSATE_KNEE_FORWARD = 2
COMPENSATE_KNEE_BACKWARD = 3

# Conectar a hats
# El hat sin soldadura es 0x40
# El hat con soldadura es 0x42
leftHat = ServoKit(channels=16, address=0x42)
rightHat = ServoKit(channels=16, address=0x40)

# Pines a los cuales estan conectados cada pata
legs = [[8, 9, 10], [4, 5, 6], [0, 1, 2], [8, 9, 10], [4, 5, 6], [0, 1, 2]]
	# right front / right mid / right back / left front / left mid / left back
	# horizontal / vertical / knee

# Angulos base para motores que controlan movimiento horizontal
horizontalBase = [90, 90, 90, 90, 90, 90]
	
	# Angulos viejos previo a ajuste
	# Valores base
	# 85 = 90-5			95 = 90+5
	# 90 				90
	# 110 = 90+20 		70 = 90-20
	# Los valores que se le suman o restan eran ajustes por patas torcidas
#horizontalBase = [85+20, 90+5, 110+5, 95+10, 90+15, 70+5]

# Angulos base para motores que controlan movimiento vertical
verticalBase = [50, 50, 50, 130, 130, 130]

	# Angulos viejos previo a ajuste
	# Derecha 		50 = 90-40
	# Izquierda 	130 = 90+40
	# Los valores que se le suman o restan eran ajustes por patas torcidas
#verticalBase = [50-5, 50-12, 50-10, 130-4, 130+8, 130+5]

# Valores para doblar patas y guardar hexapod
verticalStore = [165, 165, 165, 15, 15, 15]
kneeStore = [165, 165, 165, 15, 15, 15]

# EXPERIMENTAL
# Angulos para compensar movimiento y reducir estres que sufren los motores
compensations = [[2, 0, -2, 0], [0, 0, 0, 0], [0, 2, 0,-4], [-2, 0, 2, 0], [0, 0, 0, 0], [0, -2, 0, 4]]
	# right front / right mid / right back / left front / left mid / left back
	# vertical forward / vertical backward / knee forward / knee backward
	# horizontal no necesita compensacion
	# horizontal es quien hace que la compensacion sea necesaria!



# Variable para saber si el hexapod tiene sus patas dobladas
stored = false



# Rodillas en posicion neutra
def neutralKnees():
	for i in range(0,2):
		leftHat.servo[ legs[i+3][KNEE] ].angle = KNEE_BASE
		rightHat.servo[ legs[i+0][KNEE] ].angle = KNEE_BASE

# Rodillas estiradas
def extendKnees():
	for i in range(0,2):
		leftHat.servo[ legs[i+3][KNEE] ].angle = KNEE_BASE + KNEE_LEFT_EXTENSION
		rightHat.servo[ legs[i+0][KNEE] ].angle = KNEE_BASE + KNEE_RIGHT_EXTENSION



########## FUNCIONES BASE PARA MOVIMIENTO ##########
################### NO MODIFICAR ###################

	# Movimiento vertical

# Los motores deben moverse de tres en tres
# Siempre deben haber al menos tres patas en contacto con el suelo para dar estabilidad

# Mover a tres angulos distintos
# Nunca se llama directamente
# Se prefiere usar las otras funciones porque movimientos deben ser simetricos
def moveVerticalLRL(front, mid, back):
	leftHat.servo[ legs[LEFT_FRONT][VERTICAL] ].angle = verticalBase[LEFT_FRONT] + front 
	rightHat.servo[ legs[RIGHT_MID][VERTICAL] ].angle = verticalBase[RIGHT_MID] + mid 
	leftHat.servo[ legs[LEFT_BACK][VERTICAL] ].angle = verticalBase[LEFT_BACK] + back

# Mover a dos angulos distintos
# Usado para levantar patas
def moveVerticalLRL2(left, right):
	moveVerticalLRL(left, right, left)

# Mover al mismo angulo
# Usado para regresar patas a tierra
def moveVerticalLRL1(delta):
	moveVerticalLRL(delta, delta, delta)

# Las siguientes tres funciones son reflejo de las tres anteriores
# pero para el trio opuesto de patas

# Mover a tres angulos distintos
# Nunca se llama directamente
# Se prefiere usar las otras funciones porque movimientos deben ser simetricos
def moveVerticalRLR(front, mid, back):
	rightHat.servo[ legs[RIGHT_FRONT][VERTICAL] ].angle = verticalBase[RIGHT_FRONT] + front 
	leftHat.servo[ legs[LEFT_MID][VERTICAL] ].angle = verticalBase[LEFT_MID] + mid 
	rightHat.servo[ legs[RIGHT_FRONT][VERTICAL] ].angle = verticalBase[RIGHT_BACK] + back 

# Mover a dos angulos distintos
# Usado para levantar patas
def moveVerticalRLR2(left, right):
	moveVerticalRLR(right, left, right)

# Mover al mismo angulo
# Usado para regresar patas a tierra
def moveVerticalRLR1(delta):
	moveVerticalRLR(delta, delta, delta)



	# Movimiento horizontal

# Usado para caminar
def moveHorizontalLRL(left, right):
	leftHat.servo[ legs[LEFT_FRONT][HORIZONTAL] ].angle = horizontalBase[LEFT_FRONT] + left 
	rightHat.servo[ legs[RIGHT_MID][HORIZONTAL] ].angle = horizontalBase[RIGHT_MID] + right 
	leftHat.servo[ legs[LEFT_BACK][HORIZONTAL] ].angle = horizontalBase[LEFT_BACK] + left

# Usado para girar o regresar patas a posicion base
def moveHorizontalLRL1(delta):
	moveHorizontalLRL(delta, delta)

# Usado para caminar
def moveHorizontalRLR(left, right):
	rightHat.servo[ legs[RIGHT_FRONT][HORIZONTAL] ].angle = horizontalBase[RIGHT_FRONT] + right 
	leftHat.servo[ legs[LEFT_MID][HORIZONTAL] ].angle = horizontalBase[LEFT_MID] + left 
	rightHat.servo[ legs[RIGHT_BACK][HORIZONTAL] ].angle = horizontalBase[RIGHT_BACK] + right

# Usado para girar o regresar patas a posicion base
def moveHorizontalRLR1(delta):
	moveHorizontalRLR(delta, delta)

########## FIN DE FUNCIONES BASE PARA MOVIMIENTO ##########
###################### NO MODIFICAR #######################



# Calibracion
# Usado para llevar las patas a una posicion base
# para poder ajustar el hardware
def callibrate(rise):
	moveHorizontalRLR1(HORIZONTAL_RETURN_TO_BASE)
	moveHorizontalLRL1(HORIZONTAL_RETURN_TO_BASE)
	time.sleep(1)

	leftHat.servo[ legs[LEFT_FRONT][VERTICAL] ].angle = verticalBase[LEFT_FRONT] - rise 
	leftHat.servo[ legs[LEFT_MID][VERTICAL] ].angle = verticalBase[LEFT_MID] - rise 
	leftHat.servo[ legs[LEFT_BACK][VERTICAL] ].angle = verticalBase[LEFT_BACK] - rise
	rightHat.servo[ legs[RIGHT_FRONT][VERTICAL] ].angle = verticalBase[RIGHT_FRONT] + rise
	rightHat.servo[ legs[RIGHT_MID][VERTICAL] ].angle = verticalBase[RIGHT_MID] + rise
	rightHat.servo[ legs[RIGHT_BACK][VERTICAL] ].angle = verticalBase[RIGHT_BACK] + rise
	time.sleep(1)

# Doblar patas para guardar el hexapod
def store():
	global stored
	stored = true

	moveHorizontalRLR1(HORIZONTAL_RETURN_TO_BASE)
	moveHorizontalLRL1(HORIZONTAL_RETURN_TO_BASE)
	time.sleep(1)

	# Dobla cada pata
	# Tiempo de espera entre cada pata por seguridad
	# y para hacerlo mas vistoso :P
	leftHat.servo[ legs[LEFT_FRONT][VERTICAL] ].angle = verticalStore[LEFT_FRONT]
	time.sleep(0.5)
	leftHat.servo[ legs[LEFT_MID][VERTICAL] ].angle = verticalStore[LEFT_MID]
	time.sleep(0.5)
	leftHat.servo[ legs[LEFT_BACK][VERTICAL] ].angle = verticalStore[LEFT_BACK]
	time.sleep(0.5)
	rightHat.servo[ legs[RIGHT_FRONT][VERTICAL] ].angle = verticalStore[RIGHT_FRONT]
	time.sleep(0.5)
	rightHat.servo[ legs[RIGHT_MID][VERTICAL] ].angle = verticalStore[RIGHT_MID]
	time.sleep(0.5)
	rightHat.servo[ legs[RIGHT_BACK][VERTICAL] ].angle = verticalStore[RIGHT_BACK]
	time.sleep(0.5)

	# Dobla todas las rodillas a la vez
	for i in range(0,2):
		leftHat.servo[ legs[i+3][KNEE] ].angle = kneeStore[i+3]
		rightHat.servo[ legs[i+0][KNEE] ].angle = kneeStore[i+0]
	time.sleep(1)

# Parar el hexapod
# Se puede usar para extender las patas despues de haberlas doblado
def standStill():
	global stored
	stored = false

	moveHorizontalLRL1(HORIZONTAL_RETURN_TO_BASE)
	moveHorizontalRLR1(HORIZONTAL_RETURN_TO_BASE)
	time.sleep(1)

	moveVerticalLRL1(VERTICAL_RETURN_TO_BASE)
	moveVerticalRLR1(VERTICAL_RETURN_TO_BASE)
	time.sleep(1)

	extendKnees()
	time.sleep(1)

# Caminar hacia adelante
def forward():
	if stored:
		standStill()

	for i in range(0, 6):
		# Se asegura de colocar tres patas en el suelo
		moveVerticalLRL1(VERTICAL_RETURN_TO_BASE)
		# Levanta las otras tres patas
		moveVerticalRLR2(VERTICAL_LEFT_RISE, VERTICAL_RIGHT_RISE)
		time.sleep(DELAY_FORWARD)
		# Gira patas que levanto hacia adelante
		moveHorizontalRLR(HORIZONTAL_LEFT_FORWARD, HORIZONTAL_RIGHT_FORWARD)
		# Gira patas del suelo hacia atras
		moveHorizontalLRL(-HORIZONTAL_LEFT_FORWARD, -HORIZONTAL_RIGHT_FORWARD)
		time.sleep(DELAY_FORWARD)

		# Repite el proceso con las tres patas opuestas
		moveVerticalRLR1(VERTICAL_RETURN_TO_BASE)
		moveVerticalLRL2(VERTICAL_LEFT_RISE, VERTICAL_RIGHT_RISE)
		time.sleep(DELAY_FORWARD)
		moveHorizontalLRL(HORIZONTAL_LEFT_FORWARD, HORIZONTAL_RIGHT_FORWARD)
		moveHorizontalRLR(-HORIZONTAL_LEFT_FORWARD, -HORIZONTAL_RIGHT_FORWARD)
		time.sleep(DELAY_FORWARD)

	# Llamada a standStill() para garantizar
	# que patas regresen a posicion base
	standStill()

# Girar en sentido antihorario
def turnCounterClockwise():
	if stored:
		standStill()

	# Gira todas las patas en el suelo
	moveHorizontalLRL1(HORIZONTAL_TURN_COUNTERCW)
	moveHorizontalRLR1(HORIZONTAL_TURN_COUNTERCW)
	time.sleep(DELAY_TURN)
	
	# Levanta tres patas
	moveVerticalLRL2(VERTICAL_LEFT_RISE, VERTICAL_RIGHT_RISE)
	time.sleep(DELAY_TURN)
	# Gira patas que levanto a posicion neutra
	moveHorizontalLRL1(HORIZONTAL_RETURN_TO_BASE)
	time.sleep(DELAY_TURN)
	# Regresa patas al suelo
	moveVerticalLRL1(VERTICAL_RETURN_TO_BASE)
	time.sleep(DELAY_TURN)

	# Repite proceso con el otro trio de patas
	moveVerticalRLR2(VERTICAL_LEFT_RISE, VERTICAL_RIGHT_RISE)
	time.sleep(DELAY_TURN)
	moveHorizontalRLR1(HORIZONTAL_RETURN_TO_BASE)
	time.sleep(DELAY_TURN)
	moveVerticalRLR1(VERTICAL_RETURN_TO_BASE)
	time.sleep(DELAY_TURN)
	
	# Por seguridad
	time.sleep(DELAY_TURN)

# Girar en sentido horario
def turnClockwise():
	if stored:
		standStill()

	# Mismos movimientos que turnCounterClockwise
	# pero en sentido opuesto

	moveHorizontalRLR1(HORIZONTAL_TURN_CLOCKWISE)
	moveHorizontalLRL1(HORIZONTAL_TURN_CLOCKWISE)
	time.sleep(DELAY_TURN)

	moveVerticalRLR2(VERTICAL_LEFT_RISE, VERTICAL_RIGHT_RISE)
	time.sleep(DELAY_TURN)
	moveHorizontalRLR1(HORIZONTAL_RETURN_TO_BASE)
	time.sleep(DELAY_TURN)
	moveVerticalRLR1(VERTICAL_RETURN_TO_BASE)
	time.sleep(DELAY_TURN)

	moveVerticalLRL2(VERTICAL_LEFT_RISE, VERTICAL_RIGHT_RISE)
	time.sleep(DELAY_TURN)
	moveHorizontalLRL1(HORIZONTAL_RETURN_TO_BASE)
	time.sleep(DELAY_TURN)
	moveVerticalLRL1(VERTICAL_RETURN_TO_BASE)
	time.sleep(DELAY_TURN)
	
	# Por seguridad
	time.sleep(DELAY_TURN)



# Menu sencillo que lee comandos del usuario
while (True):
    read = input("comando: ")
    
    if read == 's':					# s - salir
        break
    elif read == 'g':				# g - guardar patas
        store()
    elif read == 'p':				# p - pararse
        standStill()
    elif read == 'c':				# c - caminar	
        forward()
    elif read == 'i':				# i - girar a la izquierda (antihorario)
        turnCounterClockwise()		# Se llama tres veces para hacerlo vistoso
        turnCounterClockwise()
        turnCounterClockwise()
    elif read == 'd':				# d - girar a la derecha (horario)
        turnClockwise()				# SE llama tres veces para hacerlo vistoso
        turnClockwise()
        turnClockwise()



# Para crear una rutina de movimiento solo se deberia llamar a
#	store()
# 	standStill()
#	forward()
#	turnClockwise()
#	turnCounterClockwise()

# Para calibrar el hexapod solo deberia llamarse
# 	callibrate(anguloDePrueba)
# Esta funcion solo deberia llamarse con el hexapod colocado sobre
# una base para evitar que patas se fuercen

# Las demas funciones no deberian ser llamadas directamente

# Cada rutina nueva deberia probarse con el hexapod sobre una base
# La base puede ser una caja común, de material que soporte unas 3 o 4 libras de peso
# Tamano recomendado:
#	Altura - 14 cm o mas
# 	Ancho - entre 8 y 10 cm
#	Largo - entre 10 y 15 cm

# Siempre que se mande a llamar store() se deberia tener el hexapod
# ya sobre la base, o sostenido con la mano