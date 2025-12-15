import pygame
import sys
import clases
import random
import colores
import os



def main():
    pygame.init()
    screen = SetScreen()
    background, ancho_fondo, x_fondo = SetBackground()
    clock = SetClock()

    velocidad_base = 4
    puntos = 0
    intervalo_dificultad = 500
    fuente = pygame.font.SysFont("Press Start 2P Regular", 14)

    #los estados manejan las pantallas: inicio, jugando, game over.  
    estado_juego = "inicio"  

    gallina = clases.GallinaPoderosa()
    _lista_sprite = pygame.sprite.Group()
    _lista_sprite.add(gallina)

    obstaculos = pygame.sprite.Group()
    timer_obstaculo = 500
    ultimo_spawn = pygame.time.get_ticks()

    out = False
    while not out:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                out = True

            if estado_juego == "inicio":
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    estado_juego = "jugando"
                    gallina = clases.GallinaPoderosa()
                    _lista_sprite = pygame.sprite.Group(gallina)
                    obstaculos.empty()
                    puntos = 0
                    velocidad_base = 4

            elif estado_juego == "jugando":
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE or evento.key == pygame.K_UP:
                        gallina.saltar()
                    if evento.key == pygame.K_DOWN:
                        gallina.agacharse()
                    if evento.key == pygame.K_9:
                        gallina.morir()
                if evento.type == pygame.KEYUP:
                    if evento.key == pygame.K_DOWN:
                        gallina.reanudar_correr()

            elif estado_juego == "game_over":
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                    estado_juego = "inicio"
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_e:
                    out=True
    

        if estado_juego == "inicio":
            screen.blit(background, (0, -550))
            mensaje = fuente.render("Presiona ESPACIO para comenzar", True, colores.NEGRO)
            screen.blit(mensaje, (30, 100))
        elif estado_juego == "jugando":
            puntos += 0.5
            y_fondo = -550
            x_fondo -= velocidad_base
            screen.blit(background, (x_fondo, y_fondo))
            screen.blit(background, (x_fondo + ancho_fondo, y_fondo))
      
            if x_fondo <= -ancho_fondo:
                x_fondo = 0

            ahora = pygame.time.get_ticks()

            if ahora - ultimo_spawn > timer_obstaculo:
                tipo = random.choice(["roca1", "ave", "roca2"])
                if tipo == "roca1":
                    nuevo = clases.Roca1(velocidad_base)
                elif tipo == "ave":
                    nuevo = clases.Ave(velocidad_base)
                elif tipo == "roca2":
                    nuevo = clases.Roca2(velocidad_base)
                obstaculos.add(nuevo)
                ultimo_spawn = ahora

            _lista_sprite.update()
            _lista_sprite.draw(screen)

            for obstaculo in obstaculos:
                if gallina.hitbox.colliderect(obstaculo.hitbox):
                    gallina.morir()
                    estado_juego = "game_over"

            obstaculos.update()
            obstaculos.draw(screen)

            if puntos % intervalo_dificultad == 0:
                velocidad_base += 0.5

            texto_puntos = fuente.render(f"Puntos: {int(puntos)}", True, colores.NEGRO)
            screen.blit(texto_puntos, (10, 10))

        elif estado_juego == "game_over":
            screen.blit(background, (0, -550))
            mensaje = fuente.render("Game Over - R para reiniciar", True, colores.ROJO)
            puntos_totales = fuente.render(f"Puntaje: {int(puntos)}", True, colores.NEGRO)
            mensaje_salir=fuente.render("Presiona E para salir", True, colores.NEGRO)
            screen.blit(mensaje, (50, 50))
            screen.blit(puntos_totales, (170, 100))
            screen.blit(mensaje_salir, (100, 140))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

def SetScreen():
    screen = pygame.display.set_mode((500, 250))
    pygame.display.flip()
    return screen

def SetBackground():
    ruta = os.path.join("sprites", "background.png")
    background = pygame.image.load(ruta)
    ancho_fondo = background.get_width()
    x_fondo = 0
    return background, ancho_fondo, x_fondo

def SetClock():
    clock = pygame.time.Clock()
    clock.tick(60)
    return clock


if __name__ == "__main__":
    main()
