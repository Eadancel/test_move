""" 
 Cómo poner un temporizador en la pantalla.
  
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
"""
  
import pygame
  
# Definimos algunos colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
  
pygame.init()
   
   
# Establecemos la altura y largo de la pantalla
dimensiones = [700, 500]
pantalla = pygame.display.set_mode(dimensiones)
  
pygame.display.set_caption("Mi Juego")
  
#Iteramos hasta que el usuario haga click sobre el botón de cerrar
hecho = False
  
# Usado para gestionar cuán rápido se actualiza la pantalla
reloj = pygame.time.Clock()
 
# Esta es la fuente que usaremos para el textoo que aparecerá en pantalla (tamaño 25)
fuente = pygame.font.Font(None, 25)
 
numero_de_fotogramas = 0
tasa_fotogramas = 20
instante_de_partida = 90
 
# -------- Bucle Principal del Programa -----------
while not hecho:    
    for evento in pygame.event.get():  # El usuario hizo algo
        if evento.type == pygame.QUIT: # Si el usuario hace click sobre cerrar
            hecho = True               # Marca que ya lo hemos hecho, de forma que abandonamos el bucle
  
    # Limpia la pantalla y establece su color de fondo
    pantalla.fill(BLANCO)
  
    # TODO EL CÓDIGO DE DIBUJO DEBERÍA IR DEBAJO DE ESTE COMENTARIO
     
    # --- El temporizador avanza ---
    # Calculamos los segundos totales
    segundos_totales = numero_de_fotogramas // tasa_fotogramas
     
    # Dividimos por 60 para obtener los minutos totales
    minutos = segundos_totales // 60
     
    # Usamos el módulo (resto) para obtener los segundos
    segundos = segundos_totales % 60
     
    # Usamos el formato de cadenas de texto para formatear los ceros del principio
    texto_de_salida = "Time: {0:02}:{1:02}".format(minutos, segundos)
     
    # Volcamos en pantalla
    texto = fuente.render(texto_de_salida, True, NEGRO)
    pantalla.blit(texto, [250, 250])
     
 
    # --- El temporizador retrocede ---
    # --- El temporizador avanza ---
    # Calculamos los segundos totales 
    segundos_totales = instante_de_partida - (numero_de_fotogramas // tasa_fotogramas)
    if segundos_totales < 0:
        segundos_totales = 0
     
    # Dividimos por 60 para obtener los minutos totales
    minutos = segundos_totales // 60
     
    # Usamos el módulo (resto) para obtener los segundos
    segundos = segundos_totales % 60
     
    # Usamos el formato de cadenas de texto para formatear los ceros del principio
    texto_de_salida = "Time left: {0:02}:{1:02}".format(minutos, segundos)
     
    # Volcamos en pantalla
    texto = fuente.render(texto_de_salida, True, NEGRO)
     
    pantalla.blit(texto, [250, 280])
     
    # TODO EL CÓDIGO DE DIBUJO DEBERÍA IR ENCIMA DE ESTE COMENTARIO
    numero_de_fotogramas += 1
     
    # Limitamos a 20 fotogramas por segundo
    reloj.tick(20)
  
    # Avancemos y actualicemos la pantalla con lo que hemos dibujado.
    pygame.display.flip()
      
# Pórtate bien con el IDLE. Si nos olvidamos de esta línea, el programa se 'colgará'
# en la salida.
pygame.quit()