import pygame
import time
import random
#def new_func(Ventana):
    
    

#----INICIALIZANDO-----
pygame.init()
pygame.mixer.init()
pygame.font.init()
#-----------------------

#-----CONFIGURACIONES-----
#LETRA
TipoLetra = pygame.font.SysFont('System', 60)
#SONIDO
Sonidoraqueta = pygame.mixer.Sound("Sounds/clipload2.wav")
SonidoPunto = pygame.mixer.Sound("Sounds/gol.wav")
SonidoRebote = pygame.mixer.Sound("Sounds/clipload2.wav")

#VENTANA
Tamano = (800, 600)
PlayerAncho = 15
PlayerAlto = 90
Ventana = pygame.display.set_mode(Tamano)
clock = pygame.time.Clock()
#-----------------------------------------------

# ----COLORES----
Negro = (0, 0, 0)
Blanco = (255, 255, 255)
#-------------------------

#----CLASES---------------
class Player:
    def __init__(self, x, y) -> None:
        self.x = x 
        self.y = y  
        self.speed_x = 0
        self.speed_y = 0
        self.puntos_player = 0
        self.score = 0
    def movimiento(self):
        self.y += self.speed_y
        self.x += self.speed_x
    def powerUp(self):
        pass  
class Ball:
    def __init__(self) -> None:
        self.x = 400
        self.y = 300
        self.speed_x = 3
        self.speed_y = 3
    def movimiento(self):
        self.y += self.speed_y
        self.x += self.speed_x  
class Menu:
    def __init__(self) -> None:
        pass
#--------------------------------------

#----FUNCIONES----------
def lado(bola,n):
    if bola.speed_x > 0 and bola.speed_y > 0:
        bola.speed_x = n
        bola.speed_y = n
    elif bola.speed_x > 0 and bola.speed_y < 0:
        bola.speed_x = n
        bola.speed_y = -n
    #izquierda
    elif bola.speed_x < 0 and bola.speed_y < 0:
        bola.speed_x = -n 
        bola.speed_y = -n
    elif bola.speed_x < 0 and bola.speed_y > 0:
        bola.speed_x = -n
        bola.speed_y = n


#----INICIALIZANDO PLAYER----
player1 = Player(50,300-45)
player2 = Player(750-PlayerAncho,300-45)
#----------------------------------------

#----INICIALIZANDO BOLA----
bola = Ball()
#----------------------------------------

game_over = False
contador_bloqueo = 0

spawn_power_up_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_power_up_event, 5000)  # 2000 milisegundos = 2 segundos

power_up = pygame.Rect(0, 0, 20, 20)
power_up_active = False
# Lista para almacenar las coordenadas de los puntos


while not game_over:
    tiempo = pygame.time.get_ticks()//1000
    #pygame.mixer.Sound.play(fondoSound)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == spawn_power_up_event:
            power_up.x = random.randint(0, 800 - power_up.width)
            power_up.y = random.randint(0, 600 - power_up.height)
            power_up_active = True
        if event.type == pygame.KEYDOWN:
            # ----Jugador 1----
            if event.key == pygame.K_w:
                player1.speed_y = -4
            if event.key == pygame.K_s:
                player1.speed_y = 4
            if event.key == pygame.K_a:  
                player1.speed_x = -4
            if event.key == pygame.K_d:  
                player1.speed_x = 4
            # ----Jugador 2----
            if event.key == pygame.K_UP:
                player2.speed_y = -4
            if event.key == pygame.K_DOWN:
                player2.speed_y = 4
            if event.key == pygame.K_LEFT: 
                player2.speed_x = -4
            if event.key == pygame.K_RIGHT: 
                player2.speed_x = 4

        if event.type == pygame.KEYUP:
            # Jugador 1
            if event.key == pygame.K_w:
                player1.speed_y = 0
            if event.key == pygame.K_s:
                player1.speed_y = 0
            if event.key == pygame.K_a:
                player1.speed_x = 0
            if event.key == pygame.K_d:
                player1.speed_x = 0
            # Jugador 2
            if event.key == pygame.K_UP:
                player2.speed_y = 0
            if event.key == pygame.K_DOWN:
                player2.speed_y = 0
            if event.key == pygame.K_LEFT:
                player2.speed_x = 0
            if event.key == pygame.K_RIGHT:
                player2.speed_x = 0

    #-----COLISIONES CON PAREDES------
    if bola.y > 590 or bola.y < 10:
        bola.speed_y *= -1
        pygame.mixer.Sound.play(SonidoRebote)
        
              
    #--------------------------------------

    #------PUNTO JUGADOR 1---------
    if bola.x > 800:
        bola.x = 400
        bola.y = 300
        bola.speed_x *= -1
        bola.speed_y *= -1
        pygame.mixer.Sound.play(SonidoPunto)
        player1.puntos_player += 1
    #-----------------------------------------
    #-----PUNTO JUGADOR 2-----------
    
    if bola.x < 0:
        bola.x = 400
        bola.y = 300
        bola.speed_x *= -1
        bola.speed_y *= -1
        pygame.mixer.Sound.play(SonidoPunto)
        player2.puntos_player += 1
    #--------------------------------------------------






    #----powerUP----
    #jugador1
    mostrar_bloqueo1 = None
    mostrar_bloqueo2 = None
    
    if player1.puntos_player == 2 and player2.puntos_player == 0 and contador_bloqueo == 0:
        if bola.x <= 398 and contador_bloqueo == 0:
            player2.speed_x = 0
            player2.speed_y = 0
            mostrar_bloqueo1 = True
        if bola.x > 400 and contador_bloqueo ==0:
            mostrar_bloqueo1 = None
            contador_bloqueo = 1
    #jugador2
    if player2.puntos_player == 2 and player1.puntos_player == 0 and contador_bloqueo == 0:
        
        if bola.x >= 398:
            player1.speed_x = 0
            player1.speed_y = 0
            mostrar_bloqueo2 = True
        if bola.x < 396:
            mostrar_bloqueo2 = None
            contador_bloqueo = 1

    #----------------------------------------------


    #----Dificultad-----
    if tiempo == 10:
        n = 4
        lado(bola,n)
    if tiempo == 20:
        n = 5
        lado(bola,n)
    if tiempo == 35:
        n = 5
        lado(bola,n)
    if tiempo == 50:
        n = 6
        lado(bola,n)
    if tiempo == 60:
        n = 7
        lado(bola,n)
    if tiempo == 70:
        n = 8
        lado(bola,n)
    if tiempo == 80:
        n = 9
        lado(bola,n)
    #-----------------------
    
    



    
    #----MOVIMIENTO JUGADORES----
    player1.movimiento()
    player2.movimiento()
    #---------------------------

    #----MOVIMIENTO PELOTA----
    bola.movimiento()
    #-------------------------

    
  
    #----GRAFICAR--------
    fondo = pygame.image.load("images/fondo.jpg")
    fondo = pygame.transform.scale(fondo,(800,600))
    Ventana.blit(fondo, (0,0))

    imagen_jugador1 = pygame.image.load("images/jugador1.png")
    imagen_jugador2 = pygame.image.load("images/jugador2.png")
    imagen_jugador1 = pygame.transform.scale(imagen_jugador1, (90, 110))
    imagen_jugador2 = pygame.transform.scale(imagen_jugador2, (90, 110))

    jugador1 = imagen_jugador1.get_rect()
    jugador2 = imagen_jugador2.get_rect()
    jugador1.topright = (player1.x+90,player1.y) 
    jugador2.topleft = (player2.x, player2.y)   
    
    Ventana.blit(imagen_jugador1, (player1.x, player1.y))
    Ventana.blit(imagen_jugador2, (player2.x, player2.y))

    imagen_pelota = pygame.image.load("images/ball.png")
    imagen_pelota = pygame.transform.scale(imagen_pelota, (60, 60))
    pelota = imagen_pelota.get_rect()
    pelota.topleft = (bola.x,bola.y)
    # pelota = pygame.draw.circle(Ventana, Blanco, (bola.x, bola.y), 10)
    Ventana.blit(imagen_pelota, (bola.x, bola.y))

    LineaMitad = pygame.draw.rect(Ventana, Blanco, (398, 40, 4, 600)) 
    
    LineaIzq = pygame.draw.rect(Ventana, Blanco, (0, 0, 4, 600))
    LineaDer = pygame.draw.rect(Ventana, Blanco, (796, 0, 4, 600))
    LineaSup = pygame.draw.rect(Ventana, (255, 255, 255), (0, 0, 800, 4))
    LineaInf = pygame.draw.rect(Ventana, (255, 255, 255), (0, 596, 800, 4))


    
    if power_up_active and jugador1.colliderect(power_up):
        player1.score += 1
        if player1.score > 3 and player1.score <= 5 :
            lado(player1,8)
        power_up_active = False  

    if power_up_active and jugador2.colliderect(power_up):
        player2.score += 1
        if player2.score > 3 and player2.score <= 5 :
            lado(player2,8)
        power_up_active = False  

    if power_up_active:
        pygame.draw.ellipse(Ventana, Blanco, power_up)
    


    #------------------------------------------------------------------------------------------------------
    #----PUNTAJE------
    if player1.puntos_player >= 5 or player2.puntos_player >= 5:
        game_over = True
    #-----------------------------------------------------------

    #textos borrables
    if mostrar_bloqueo1 is not None:
        bloqueado = f"CONGELADO"
        texto = TipoLetra.render(bloqueado, True, (255, 255, 255))
        Ventana.blit(texto,(450,70))
    if mostrar_bloqueo2 is not None:
        bloqueado = f"CONGELADO"
        texto = TipoLetra.render(bloqueado, True, (255, 255, 255))
        Ventana.blit(texto,(50,70))
        
         


    #----Colisiones----
    if pelota.colliderect(jugador1) or pelota.colliderect(jugador2):
        bola.speed_x *= -1
        #pygame.mixer.Sound.play(Sonidoraqueta)
    if jugador1.colliderect(LineaMitad):
        player1.x -= 5
    if jugador2.colliderect(LineaMitad):
        player2.x += 5
    #----------------------------------------------------------------------
    

    

    #----TIEMPO-------
    
    tiempo_texto = f"{tiempo} seg"
    texto = TipoLetra.render(tiempo_texto, True, (255, 255, 255))
    Ventana.blit(texto,(360,0))
    #-----------------------------------------------------------

    #----PUNTAJE---------
    TextoPlayer1 = TipoLetra.render(str(player1.puntos_player), False, Blanco)
    TextoPlayer2 = TipoLetra.render(str(player2.puntos_player), False, Blanco)  
    Ventana.blit(TextoPlayer1, (100, 0))
    Ventana.blit(TextoPlayer2, (700, 0))
    #----------------------------------------------------------------------------

    pygame.display.flip()
    clock.tick(60)
pygame.quit()