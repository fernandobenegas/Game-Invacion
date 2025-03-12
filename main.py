
# Modulos
import math
import pygame
import random
import pygame
from pygame import mixer #Modulo de musica
pygame.init()


# Creamos la pantalla
pantalla = pygame.display.set_mode((800,600))

#titulo del cono
pygame.display.set_caption("Mi Primer Juego")
icono = pygame.image.load('ovni.png')  # Asegúrate de usar la ruta correcta a tu imagen
fondo = pygame.image.load('background.jpg')# Agregamos el fondo
puntaje = 0
fuente= pygame.font.Font('freesansbold.ttf',32)
texto_x = 10
texto_y = 10
final_juego = pygame.font.Font('freesansbold.ttf',40) 


mixer.music.load('MusicaFondo.mp3')
mixer.music.play(-1)
#------------------Variables-----------------------------------------

#creamos el jugador y sus variables
img_jugador = pygame.image.load("cohete.png")
jugadorX = 368
jugadorY = 500
jugador_x_cambio = 0 
puntaje = 0

#creamos el enemigo y sus variables
img_enemigo = []
enemigoX = []
enemigoY = []
enemigo_x_cambio = [] # esto es la tasa de cambio o movimiento
enemigo_y_cambio = []
cantidad_enemigos = 5

# Creamos 8 enemigos con el loop for
for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("enemigo.png"))
    enemigoX.append(random.randint(0,736))
    enemigoY.append(random.randint(50,200))
    enemigo_x_cambio.append(0.1) # esto es la tasa de cambio o movimiento
    enemigo_y_cambio.append(50)

#Variables de disparo 
img_disparos =pygame.image.load('bala.png')#Agregamos la bala
disparosX = 0
disparosY = 500 #La bala se posiciona a la altura donde esta la nave
disparo_x_cambio = 0
disparo_y_cambio = 0.8 
disparo_visible = False

#----------------Funciones-Start---------------------------------------------
#Funcion jugador
def jugador(x,y):
    pantalla.blit(img_jugador,(x,y))#Arrojamos los datos a la pantalla

#Funcion enemigo
def enemigo(x,y,n):
    pantalla.blit(img_enemigo[n],(x,y))#Arrojamos los datos a la pantalla

def disparos_bala(X,Y):
    global disparo_visible
    disparo_visible = True
    pantalla.blit(img_disparos,(X + 16  , Y + 10 )) 

# Funcion que detecta coliciones
def detectarColicion(x_1,y_1,x_2,y_2):
    distancia = math.sqrt(math.pow(x_1-x_2 , 2) + math.pow(y_1 - y_2, 2))
    if distancia < 27:
        return True
    else:
        False

def mostraPuntaje(x,y):
    texto = fuente.render(f"Puntaje {puntaje}",True, (255,255,255,255))
    pantalla.blit(texto,(x,y))

def texto_final():
    final = final_juego.render(f"Game Over" , True , (255,255,255))
    pantalla.blit(final,(100,250)) 
    

# Configuramos el ícono de la ventana
pygame.display.set_icon(icono)

#----------------Funciones-End--------------------------------------------



#----------------Bucles-Start---------------------------------------------

# Bucle principal del juego
corriendo = True
while corriendo:

    # Cargamos la imagen de fondo
    #pantalla.fill((205, 144, 228))# esto carga la imagen rgb el metodo fill()
    pantalla.blit(fondo,(0,0))
    
    #Iteramos los eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: # si ocuure el evento quit osea precionamos la X cerramos la ventana
            corriendo = False
        #Evento precionar tecla
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.2 #movimientos a la izquierda
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.2#movimientos a la derecha
            #Evento de la tecla espaciadora
            if evento.key == pygame.K_SPACE:
                sonido_disparo = mixer.Sound('disparo.mp3')
                sonido_disparo.play()
                if disparo_visible == False:
                    disparosX = jugadorX
                    disparos_bala(disparosX,disparosY)
               
        if evento.type == pygame.KEYUP:# ESTE EVENTO SE DISPARA CUANDO SACAMOS EL DEDO DE LA TECLA
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0 #sin movimientos

    #Modifica la accion del jugador
    jugadorX += jugador_x_cambio # le pasamos los movimientos
  
    #Mantener dentro de los bordes al jugador 
    if jugadorX <= 0:
        jugadorX = 0
    elif jugadorX >= 736:
        jugadorX = 736 #Se calcula 800 - 64 que es el tamaño en pixel de nuestra nave  

    #Mantener dentro de los bordes al enemigo

    for e in range(cantidad_enemigos):    
        #Fin del juego
        if enemigoY[e] >= 490:
            for k in range(cantidad_enemigos):
                enemigoY[k] = 1000
            texto_final()
            break

        enemigoX[e] += enemigo_x_cambio[e] # le damos el movimiento al enemigo
        if enemigoX[e] <= 0:
            enemigo_x_cambio[e] = 0.2 # Movimientos en el eje X
            enemigoY[e] += enemigo_y_cambio[e] #Movimientos en el eje Y
        elif enemigoX[e] >= 736:
            enemigo_x_cambio[e] = -0.2   # Movimientos en el eje X
            enemigoY[e] += enemigo_y_cambio[e] #Movimientos en el eje Y
        #Verificamos si ahi colicion
        colicion = detectarColicion(enemigoX[e],enemigoY[e],disparosX,disparosY)
        if colicion ==  True:
            sonido_choque = mixer.Sound('Golpe.mp3')
            sonido_choque.play()
            disparosY = 500
            disparo_visible = False
            puntaje += 1 
            enemigoX[e] = random.randint(0,736)
            enemigoY[e] = random.randint(50,200)
        enemigo(enemigoX[e],enemigoY[e],e)

    #Movimientos de los disparos
    if disparosY <= -64:# si pasa los borde superiores y es menor a los pixeles de nuestra nave
        disparosY = 500#vuelve a su estado original
        disparo_visible = False#se recetea

    if disparo_visible == True:
        disparos_bala(disparosX,disparosY)
        disparosY -= disparo_y_cambio
 #----------------Bucles-End--------------------------------------------- 

 #----------------LLamado a Funciones------------------------------------

    jugador(jugadorX,jugadorY)
    mostraPuntaje(texto_x,texto_y)
  #----------------Fin llamado Funciones---------------------------------


  # ---------------Actualizaciones---------------------------------------
    # Actualizamos la pantalla
    pygame.display.update()

pygame.quit()