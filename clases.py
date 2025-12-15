import pygame
import os

#clase gallina (el gran protagonista)
class GallinaPoderosa(pygame.sprite.Sprite):
    def __init__(self):

        super().__init__()

        #atributos relacionads a animacion
        self._vel_animacion = 50
        self._ultimo_update = pygame.time.get_ticks()
        self._pos_animacion = 0

        #atributos relacionados al salto
        self.vel_y = 0
        self.gravedad = 0.7
        self.en_suelo = True

        #carga de animaciones
        self._animacion_correr = self.cargar_animacion("ChickenWalking.png", 4)
        self._animacion_salto = self.cargar_animacion("ChickenJumping-Sheet.png", 6)
        self._animacion_agacharse = self.cargar_frame("ChickenPeck-Sheet.png",5,27,21)
        self._animacion_morir = self.cargar_animacion("ChickenDie-Sheet.png", 4)
        self.muerta = False

        self.animacion_actual = self._animacion_correr
        self.image = self.animacion_actual[self._pos_animacion]
        
        #atributos de rect
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = 150

        #atributos de hitbox
        self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.6, self.rect.height * 0.6)
        self.hitbox.center = self.rect.center


    def cargar_animacion(self, archivo, cantidad_frames):
        ruta = os.path.join("sprites", archivo)
        sheet = pygame.image.load(ruta).convert_alpha()
        frames = []
        for i in range(cantidad_frames):
            frame = sheet.subsurface(pygame.Rect(i * 20, 0, 20, 21))
            frames.append(frame)
        return frames


    def cargar_frame(self, archivo, indice, ancho, alto):
        ruta = os.path.join("sprites", archivo)
        sheet = pygame.image.load(ruta).convert_alpha()
        frame = sheet.subsurface(pygame.Rect(indice * ancho, 0, ancho, alto))
        return frame

    def reanudar_correr(self):
        self.animacion_actual = self._animacion_correr
        self._pos_animacion = 0
        self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.6, self.rect.height * 0.6)

    def agacharse(self):
        if self.en_suelo:
            self.image = self._animacion_agacharse
            self.animacion_actual = [self._animacion_agacharse]

           #se toma como referencia la hitbox actual
            midbottom = self.hitbox.midbottom

            #se actualiza la hitbox. (cuando la gallina se agacha, la hitbox es mas enana)
            nueva_hitbox = pygame.Rect(0, 0, self.hitbox.width, self.hitbox.height * 0.5)
            nueva_hitbox.midbottom = midbottom

            self.hitbox = nueva_hitbox

    def saltar(self):
        if self.en_suelo:
            self.vel_y = -7
            self.en_suelo = False
            self.animacion_actual = self._animacion_salto
            self._pos_animacion = 0
    
    def morir(self):
        if not self.muerta:
            self.muerta = True
            self.animacion_actual = self._animacion_morir
            self._pos_animacion = 0

    def update(self):
        super().update()
        self.hitbox.center = self.rect.center
        if self.muerta:
            # Solo animar la muerte
            tiempo_actual = pygame.time.get_ticks()
            if self._pos_animacion < len(self.animacion_actual) - 1:
                if tiempo_actual - self._ultimo_update > self._vel_animacion:
                    self._pos_animacion += 1
                    self.image = self.animacion_actual[self._pos_animacion]
                    self._ultimo_update = tiempo_actual
            return  

    # Gravedad y movimiento vertical
        self.vel_y += self.gravedad
        self.rect.y += self.vel_y

        if self.rect.y >= 150:
            self.rect.y = 150
            self.vel_y = 0
            if not self.en_suelo:
                self.animacion_actual = self._animacion_correr
                self._pos_animacion = 0
                self.en_suelo = True

        # Animación frame por frame
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self._ultimo_update > self._vel_animacion:
            self._pos_animacion = (self._pos_animacion + 1) % len(self.animacion_actual)
            self.image = self.animacion_actual[self._pos_animacion]
            self._ultimo_update = tiempo_actual


#clase padre obstaculo
class Obstaculo(pygame.sprite.Sprite): 
    def __init__(self,velocidad):
        super().__init__()
        self.velocidad = velocidad
        
    def update(self):
        self.rect.x -= self.velocidad
        if self.rect.right < 0:
            self.kill()


#clase hija obstaculo terrestre 1
class Roca1(Obstaculo):
    def __init__(self,velocidad):
        super().__init__(velocidad)
        
        ruta = os.path.join("sprites", "sprite_02.png")
        self.image = pygame.image.load(ruta).convert_alpha()
        self.rect = self.image.get_rect()
        
        self.rect.x = 500
        self.rect.y = 115 #altura terrestre para nuestras rocas individuales

        
        self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.1, self.rect.height * 0.1)
        self.hitbox.center = self.rect.center

    def update(self):
        super().update()
        self.hitbox.center = self.rect.center  


#clase hija obstaculo terrestre 2
class Roca2(Obstaculo):
    def __init__(self,velocidad):
        super().__init__(velocidad)
        
        ruta = os.path.join("sprites", "sprite_04.png")
        self.image = pygame.image.load(ruta).convert_alpha()
        self.rect = self.image.get_rect()
        
        self.rect.x = 500
        self.rect.y = 115 #altura terrestre para nuestras rocas individuales

        
        self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.1, self.rect.height * 0.1)
        self.hitbox.center = self.rect.center

    def update(self):
        super().update()
        self.hitbox.center = self.rect.center  


#clase hija obstaculo aéreo
class Ave(Obstaculo):
    def __init__(self,velocidad):
        super().__init__(velocidad)
        self.frames = self.cargar_animacion()
        self._pos_frame = 0
        self._vel_animacion = 100  
        self._ultimo_update = pygame.time.get_ticks()
        
        self.image = self.frames[self._pos_frame]
        self.rect = self.image.get_rect()
        

        self.rect.x = 500
        self.rect.y = 143  #altura aérea para nuestras rocas individuales
        


        self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.8, self.rect.height * 0.8)
        self.hitbox.center = self.rect.center

    def cargar_animacion(self):
        ruta = os.path.join("sprites", "Bird Spritesheet.png")
        sheet = pygame.image.load(ruta).convert_alpha()
        frames = []
        ancho_frame = 16
        alto_frame = 16
        fila = 1  

        for i in range(8):
            frame = sheet.subsurface(pygame.Rect(i * ancho_frame, fila * alto_frame, ancho_frame, alto_frame))
            frames.append(frame)

        return frames

    def update(self):
        super().update()  
        self.hitbox.center = self.rect.center

        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self._ultimo_update > self._vel_animacion:
            self._pos_frame = (self._pos_frame + 1) % len(self.frames)
            self.image = self.frames[self._pos_frame]
            self._ultimo_update = tiempo_actual

