import pygame
import configuration
import sys
from player import Player
from enemy import Enemy
from question import question 
import random

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((configuration.WIDTH, configuration.HEIGHT))
        pygame.display.set_caption("Guardianes del saber")
        self.background = pygame.image.load("img/fondo.png")
        self.font=pygame.font.SysFont(None,40),
        self.font_Start_End=pygame.font.Font("Font/Starborn.ttf",size=30)
        self.titulo=pygame.font.Font("Font/Starborn.ttf",size=50)
        self.font_menu=pygame.font.Font("Font/KingRimba.ttf",size=15)
        self.background = pygame.transform.scale(self.background, (configuration.WIDTH, configuration.HEIGHT))
        self.question_active = False
        self.current_question = None
        self.lives = 3
        self.font = pygame.font.SysFont(None, 40)

        self.player = Player(100, 250)
        self.enemies =[
             Enemy(700, 250),
             Enemy(100, 400),
             Enemy(500, 100)]
        self.current_enemy=None

    def text(self, text, x, y, color=configuration.BLACK):
        render = self.font.render(text, True, color)
        self.screen.blit(render, (x, y))

    def inicio(self):
        titulo = self.titulo.render("Guardianes del saber", True, configuration.WHITE)

        while True:
            self.screen.fill(configuration.BLACK)
            self.screen.blit(titulo, (configuration.WIDTH / 2 - titulo.get_width() / 2, 100))

        
            pygame.draw.rect(self.screen, configuration.WHITE, configuration.boton_jugar)
            pygame.draw.rect(self.screen, configuration.RED, configuration.boton_salir)

            texto_btn_jugar = self.font_Start_End.render("Jugar", True, configuration.BLACK)
            texto_btn_salir = self.font_Start_End.render("Salir", True, configuration.WHITE)

            self.screen.blit(texto_btn_jugar, (configuration.boton_jugar.x + 25, configuration.boton_jugar.y + 10))
            self.screen.blit(texto_btn_salir, (configuration.boton_salir.x + 25, configuration.boton_salir.y + 10))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if configuration.boton_jugar.collidepoint(event.pos):
                        return  
                    
                    elif configuration.boton_salir.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()


    def game_over(self):
        font_Start_End=self.titulo.render("¡Game Over!",True, configuration.WHITE)
        font_menu=self.font.render("Presiona cualquier tecla para salir",True,configuration.RED)
        while True: 
            self.screen.fill(configuration.BLACK)
            self.screen.blit(font_Start_End, (configuration.WIDTH / 2 - font_Start_End.get_width() / 2, 100))
            self.screen.blit(font_menu, (configuration.WIDTH / 2 - font_menu.get_width() / 2, 200))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    pygame.quit()
                    sys.exit()


    def reset_game(self):
        self.player = Player(100, 250)
        self.lives = 3
        self.question_active = False
        self.current_question = None
        self.current_enemy = None
        self.opcion_botones = []

   
        self.enemies = [
            Enemy(700, 250),
            Enemy(100, 400),
            Enemy(500, 100)
        ]


    def runGame(self):
        self.inicio()
        clock = pygame.time.Clock()
        while True:
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.question_active:
                    self.handle_question(event)

            if self.question_active:
                self.question()
            else:
                keys = pygame.key.get_pressed()
                self.player.move(keys)
                
                for enemy in self.enemies:
                    if enemy.active:
                        enemy.follow(self.player.rect)
                        if self.player.rect.colliderect(enemy.rect):
                            self.current_enemy = enemy
                            self.prepare_question()
                            break  

                self.player.draw(self.screen)
                for enemy in self.enemies:
                    if enemy.active:
                        enemy.draw(self.screen)

                self.text(f"Vidas: {self.lives}", 10, 10)

                if self.lives <= 0:
                 self.game_over()
            


            pygame.display.flip()
            clock.tick(configuration.FPS)

    def dividir_texto(self, texto, fuente, max_width):
        palabras = texto.split()
        lineas = []
        linea_actual = ""

        for palabra in palabras:
            test_linea = linea_actual + palabra + " "
            if fuente.size(test_linea)[0] <= max_width:
                linea_actual = test_linea
            else:
                lineas.append(linea_actual.strip())
                linea_actual = palabra + " "

        if linea_actual:
            lineas.append(linea_actual.strip())

        return lineas


    def prepare_question(self):
        self.current_question = random.choice(question)
        self.question_active = True

    def question(self):
        q = self.current_question

        question_box=pygame.Rect(100,80,600,300)
        pygame.draw.rect(self.screen, configuration.WHITE, question_box, border_radius=15)
         
        lineas_pregunta = self.dividir_texto(q["question"], self.font, question_box.width - 40)

        for i, linea in enumerate(lineas_pregunta):
            render_linea = self.font.render(linea, True, configuration.BLACK)
            self.screen.blit(render_linea, (question_box.x + 20, question_box.y + 20 + i * 25))

        self.options_button=[]
        for i, opcion in enumerate(q["options"]):
            boton = pygame.Rect(question_box.x + 50, question_box.y + 80 + i * 60, 500, 40)
            pygame.draw.rect(self.screen, configuration.GREEN, boton, border_radius=5)
            texto_opcion = self.font.render(f"{chr(65 + i)}. {opcion}", True, configuration.BLACK)
            self.screen.blit(texto_opcion, (boton.x + 10, boton.y + 8))
            self.options_button.append((boton, chr(65 + i)))  
      
    def handle_question(self, event):
       if event.type == pygame.MOUSEBUTTONDOWN:
        for boton, letra in self.options_button:
            if boton.collidepoint(event.pos):
                if letra == self.current_question["answer"]:
                    self.mensaje = "¡Respuesta correcta!"
                    self.current_enemy.active = False  
                else:
                    self.mensaje = "Respuesta incorrecta"
                    self.lives -= 1

                if all(not enemy.active for enemy in self.enemies):
                    self.reset_game()  
                    self.runGame() 
                    return       

                self.question_active = False
                self.current_enemy = None
                self.mensaje_timer = pygame.time.get_ticks()



    def new_enemy(self):
        new_enemy = Enemy(random.randint(100, configuration.WIDTH - 100),
                      random.randint(100, configuration.HEIGHT - 100))
        self.enemies.append(new_enemy)


