import time
from pygame.locals import *
from sprites import Sprites
from modele import Generation
import math
import threading as th
import utils
import pygame


class Vue():
    def __init__(self, t):

        # Taille du tableau de jeu
        self.longueur = 16
        self.largeur = 16

        self.nb_mines = 40

        self.niveau = 1

        self.menuHeight = 20
        self.hauteur = 50 + self.menuHeight
        self.bordure = 12

        self.screen_width = self.largeur*16 + 2*self.bordure
        self.screen_height = self.longueur * 16 + self.hauteur + self.bordure

        self.background = (192, 192, 192)
        self.colorWhite = (255, 255, 255)
        self.colorGrey = (128, 128, 128)

        self.left = 1
        self.middle = 2
        self.right = 3

        self.digit_x = 13
        self.digit_y = 23

        self.smiley = 25

        self.seconds = 0
        self.demineur = 0
        self.nb_bombes = 0
        self.arrayHide = []

        self.win = False
        self.lose = False

        self.genere = True
        self.run = True
        self.t = t

        self.utils = utils.Utils()
        self.t.start()
        self.t.pause()
        pygame.init()
        pygame.font.init()  # you have to call this at the start,
        # if you want to use this module.
        self.my_font = pygame.font.SysFont('Arial', 12)
        self.initStart()

    def initStart(self):
        self.genere = True
        self.window = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        self.sprite = Sprites()
        self.window.fill(self.background)
        pygame.display.set_caption('Démineur')
        pygame.display.set_icon(pygame.image.load('./icon.png'))
        pygame.display.flip()

        self.affiche_bordure()
        self.grille()

    def fillBlocFull(self):
        for i in range(len(self.arrayHide[0])):
            for j in range(len(self.arrayHide)):
                if self.arrayHide[j][i] == '*':
                    self.window.blit(
                        self.sprite.getbloc_full(), (i*16+self.bordure, j*16+self.hauteur))

    def affiche_bordure(self):
        # print text on the screen at 0,0
        text_surface = self.my_font.render('Niveau', False, (0, 0, 0))
        self.window.blit(text_surface, dest=(
            5, (self.menuHeight-self.my_font.size("Niveau")[1])/2))

        pygame.draw.rect(self.window, self.colorWhite,
                         pygame.Rect(0, self.menuHeight, self.screen_width, 2))

        pygame.draw.rect(self.window, self.colorGrey,
                         pygame.Rect(self.bordure, 10+self.menuHeight, self.screen_width - 2*self.bordure, 2))

        pygame.draw.rect(self.window, self.colorWhite,
                         pygame.Rect(self.bordure-2, self.hauteur-self.bordure, self.screen_width - 2*self.bordure+2, 2))

        pygame.draw.rect(self.window, self.colorGrey,
                         pygame.Rect(self.bordure, self.hauteur-2, self.screen_width - 2*self.bordure, 2))

        pygame.draw.rect(self.window, self.colorWhite,
                         pygame.Rect(10, self.screen_height - self.bordure, self.screen_width - 2 * self.bordure + 4, 2))

        pygame.draw.rect(self.window, self.colorGrey,
                         pygame.Rect(0, self.screen_height - 2, self.screen_width, 2))

        # self.longueur
        pygame.draw.rect(self.window, self.colorWhite,
                         pygame.Rect(0, self.menuHeight, 2, self.screen_height-self.menuHeight))

        pygame.draw.rect(self.window, self.colorGrey,
                         pygame.Rect(10, self.hauteur-2, 2, self.screen_height - self.hauteur - self.bordure + 2))

        pygame.draw.rect(self.window, self.colorWhite,
                         pygame.Rect(self.screen_width - self.bordure, self.hauteur-2,  2, self.screen_height - self.hauteur - self.bordure + 2))

        pygame.draw.rect(self.window, self.colorGrey,
                         pygame.Rect(self.screen_width - 2, self.menuHeight,  2, self.screen_height-self.menuHeight))

        pygame.draw.rect(self.window, self.colorWhite,
                         pygame.Rect(self.screen_width - self.bordure, 10+self.menuHeight,  2, self.hauteur - 2*self.bordure + 4-self.menuHeight))

        pygame.draw.rect(self.window, self.colorGrey,
                         pygame.Rect(10, 10+self.menuHeight,  2, self.hauteur - 2*self.bordure + 2-self.menuHeight))

    def lose_and_show(self):
        for i in range(len(self.arrayHide[0])):
            for y in range(len(self.arrayHide)):
                if self.arrayHide[y][i] != '*':
                    # Si on perd
                    if self.arrayHide[y][i] == 'B':
                        for g in range(len(self.demineur.array[0])):
                            for w in range(len(self.demineur.array)):
                                if self.arrayHide[w][g] == 'F' and self.demineur.array[w][g] != 'b':
                                    self.window.blit(
                                        self.sprite.getbloc_mine_wrong(), (g*16+self.bordure, w*16+self.hauteur))
                                elif self.arrayHide[w][g] == 'F' and self.demineur.array[w][g] == 'b':
                                    self.window.blit(
                                        self.sprite.getbloc_flag(), (g*16+self.bordure, w*16+self.hauteur))
                                elif self.arrayHide[w][g] != 'F' and self.demineur.array[w][g] == 'b':
                                    self.window.blit(
                                        self.sprite.getbloc_mine(), (g*16+self.bordure, w*16+self.hauteur))
                        self.window.blit(
                            self.sprite.getbloc_mine_explode(), (i*16+self.bordure, y*16+self.hauteur))
                        self.window.blit(self.sprite.getsmiley_lose(), ((
                            self.screen_width/2) - self.smiley/2, (self.hauteur-self.menuHeight)/2 - self.smiley/2+self.menuHeight))
                        self.lose = True
                        self.t.pause()
                    # affiche les autres numéro qui sont pas une bombes
                    else:
                        self.window.blit(
                            eval(self.sprite.returnSprite(self.arrayHide[y][i])), (i*16+self.bordure, y*16+self.hauteur))

    def victoire(self):
        # Victoire
        if self.demineur.getWin() == self.nb_mines:
            self.win = True
            self.t.pause()
            self.window.blit(self.sprite.getsmiley_win(), ((self.screen_width/2) -
                                                           self.smiley/2, (self.hauteur-self.menuHeight)/2 - self.smiley/2 + self.menuHeight))

    def grille(self):
        # On affiche le tableau
        for i in range(self.largeur):
            for y in range(self.longueur):
                self.window.blit(self.sprite.getbloc_full(),
                                 (16*i+self.bordure, 16*y+self.hauteur))

        self.window.blit(self.sprite.getsmiley_happy(), ((self.screen_width/2) -
                                                         self.smiley/2, (self.hauteur-self.menuHeight)/2 + self.menuHeight - self.smiley/2))

        for i in range(3):
            self.window.blit(self.sprite.getdigit_0(),
                             (self.screen_width - (i * self.digit_x) - self.digit_x - self.bordure, (self.hauteur-self.menuHeight)/2 - self.digit_y/2 + self.menuHeight))

        # Calcul le nombre de bombes restantes
        self.nb_bombes = list(str(self.nb_mines))
        for i in range(3-len(self.nb_bombes)):
            self.nb_bombes.insert(0, '0')
        # Affiche le nombre de bombes restantes
        for i in range(len(self.nb_bombes)):
            self.window.blit(
                self.sprite.printNumber(i, self.nb_bombes), (i*self.digit_x + self.bordure, (self.hauteur - self.menuHeight)/2 - self.digit_y/2 + self.menuHeight))

        while self.run:
            # event during game
            if not self.genere and self.lose == False and self.win == False and self.t.cpt != self.seconds:
                self.seconds = self.t.cpt
                nb_sec = list(str(self.seconds))
                lst = []
                for i in range(3-len(nb_sec)):
                    nb_sec.insert(0, '0')
                for i in nb_sec:
                    lst.insert(0, i)
                for i in range(len(lst)):
                    self.window.blit(self.sprite.printNumber(i, lst),
                                     (self.screen_width - (i * self.digit_x) - self.digit_x - self.bordure, (self.hauteur-self.menuHeight)/2 - self.digit_y/2+self.menuHeight))

            for event in pygame.event.get():
                # timer tout les secondes
                if event.type == pygame.QUIT:
                    self.run = False
                    self.t.stop()
                    pygame.quit()
                    exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == self.left:
                    x, y = event.pos
                    y -= self.hauteur
                    x -= self.bordure
                    # affiche le shock si on est dans le jeux
                    if self.lose == False and self.win == False:
                        if y >= 0 and x >= 0 and x < self.screen_width - self.bordure*2 and y < self.screen_height - self.bordure - self.hauteur:
                            self.window.blit(self.sprite.getsmiley_shock(), ((self.screen_width/2) -
                                                                             self.smiley/2, (self.hauteur-self.menuHeight)/2 - self.smiley/2 + self.menuHeight))
                        # si on est dans le menu affiche le btnclick si on click dessus
                        elif x + self.bordure < (self.screen_width/2) + self.smiley/2 and x + self.bordure > (self.screen_width/2) - self.smiley/2 and y + self.hauteur < ((self.hauteur-self.menuHeight)/2) + self.smiley/2+self.menuHeight and y + self.hauteur > ((self.hauteur-self.menuHeight)/2) - self.smiley/2+self.menuHeight:
                            self.window.blit(self.sprite.getsmiley_happy_click(), ((self.screen_width/2) -
                                                                                   self.smiley/2, (self.hauteur-self.menuHeight)/2 - self.smiley/2+self.menuHeight))
                    elif self.win == False:
                        self.window.blit(self.sprite.getsmiley_lose(), ((self.screen_width/2) -
                                                                        self.smiley/2, (self.hauteur-self.menuHeight)/2 - self.smiley/2 + self.menuHeight))

                elif event.type == pygame.MOUSEBUTTONUP and event.button == self.left:
                    # Set the x, y postions of the mouse click
                    x, y = event.pos

                    # si on est dans le menu
                    if x > 0 and x < self.my_font.size("Niveau")[0] + 10 and y > 0 and y < self.menuHeight:
                        self.niveau = ((self.niveau) + 1) % 3
                        if self.niveau == 0:
                            self.longueur = 8
                            self.largeur = 7
                            self.nb_mines = 10
                        elif self.niveau == 1:
                            self.longueur = 16
                            self.largeur = 16
                            self.nb_mines = 40
                        elif self.niveau == 2:
                            self.longueur = 16
                            self.largeur = 31
                            self.nb_mines = 99
                        self.screen_width = self.largeur*16 + 2*self.bordure
                        self.screen_height = self.longueur * 16 + self.hauteur + self.bordure
                        self.initStart()

                    y -= self.hauteur
                    x -= self.bordure
                    pos_x, pos_y = int(x / 16), int(y / 16)

                    # si on est dans le jeu
                    if y >= 0 and x >= 0 and x < self.screen_width - self.bordure*2 and y < self.screen_height - self.bordure - self.hauteur:

                        while self.genere:
                            self.t.resume()
                            self.demineur = Generation(
                                self.longueur, self.largeur, self.nb_mines, pos_x, pos_y)
                            self.genere = False
                            # self.t.start()
                        if self.lose == False and self.win == False:
                            self.arrayHide = self.demineur.deleteCase(
                                pos_x, pos_y)

                        self.victoire()

                        self.lose_and_show()

                    elif x + self.bordure < (self.screen_width/2) + self.smiley/2 and x + self.bordure > (self.screen_width/2) - self.smiley/2 and y + self.hauteur < ((self.hauteur - self.menuHeight)/2 + self.smiley/2 + self.menuHeight) and y + self.hauteur > ((self.hauteur-self.menuHeight)/2 - self.smiley/2+self.menuHeight):
                        self.genere = True
                        self.t.pause()
                        self.lose = False
                        self.win = False
                        # Affiche un tableau de bloc plein
                        for i in range(self.largeur):
                            for y in range(self.longueur):
                                self.window.blit(self.sprite.getbloc_full(),
                                                 (16*i+self.bordure, 16*y+self.hauteur))
                        # Calcul le nombre de bombes restantes
                        self.nb_bombes = list(str(self.nb_mines))
                        for i in range(3-len(self.nb_bombes)):
                            self.nb_bombes.insert(0, '0')
                        # Affiche le nombre de bombes restantes
                        for i in range(len(self.nb_bombes)):
                            self.window.blit(
                                self.sprite.printNumber(i, self.nb_bombes), (i*self.digit_x + self.bordure, (self.hauteur-self.menuHeight)/2 - self.digit_y/2+self.menuHeight))

                    # Réaffiche le bon self.smiley
                    if self.lose == False and self.win == False:
                        self.window.blit(self.sprite.getsmiley_happy(), ((self.screen_width/2) -
                                                                         self.smiley/2, (self.hauteur-self.menuHeight)/2 - self.smiley/2+self.menuHeight))

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == self.right and self.lose == False and self.win == False:
                    # Set the x, y postions of the mouse click
                    x, y = event.pos
                    y -= self.hauteur
                    x -= self.bordure
                    pos_x, pos_y = int(x / 16), int(y / 16)
                    if not self.genere and y >= 0 and x >= 0 and x < self.screen_width - self.bordure*2 and y < self.screen_height - self.bordure - self.hauteur:
                        self.arrayHide = self.demineur.setFlagorInt(
                            pos_x, pos_y, self.nb_mines)

                        for i in range(len(self.arrayHide[0])):
                            for y in range(len(self.arrayHide)):
                                if self.arrayHide[y][i] == 'F':
                                    self.window.blit(
                                        self.sprite.getbloc_flag(), (int(i*16)+self.bordure, int(y*16)+self.hauteur))
                                if self.arrayHide[y][i] == 'I':
                                    self.window.blit(
                                        self.sprite.getbloc_interrogation(), (int(i*16)+self.bordure, int(y*16)+self.hauteur))
                                if self.arrayHide[y][i] == '*':
                                    self.window.blit(
                                        self.sprite.getbloc_full(), (int(i*16)+self.bordure, int(y*16)+self.hauteur))

                        # Calcul le nombre de bombes restantes
                        nb_bombe = self.nb_mines - self.demineur.getNb_Bombe()
                        self.nb_bombes = list(str(nb_bombe))
                        for i in range(3-len(self.nb_bombes)):
                            self.nb_bombes.insert(0, '0')
                 # Affiche le nombre de bombes restantes
                    for i in range(len(self.nb_bombes)):
                        self.window.blit(
                            self.sprite.printNumber(i, self.nb_bombes), (i*self.digit_x + self.bordure, (self.hauteur-self.menuHeight)/2 - self.digit_y/2+self.menuHeight))

                elif event.type == pygame.MOUSEBUTTONUP and event.button == self.middle and self.lose == False and self.win == False:
                    self.fillBlocFull()
                    self.victoire()

                # click middle
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == self.middle and self.lose == False and self.win == False:
                    x, y = event.pos
                    y -= self.hauteur
                    x -= self.bordure
                    pos_x, pos_y = int(x / 16), int(y / 16)
                    arthur = self.demineur.clickmiddle(pos_x, pos_y)
                    for i in range(len(arthur)):
                        self.demineur.deleteCase(arthur[i][0], arthur[i][1])

                    self.lose_and_show()

                # Pour actualiser le click long
                if not self.genere and self.lose == False and self.win == False:
                    click = pygame.mouse.get_pressed()
                    if click[1] == True:
                        cur = pygame.mouse.get_pos()
                        y = cur[1]-self.hauteur
                        x = cur[0]-self.bordure
                        if y >= 0 and x >= 0 and x < self.screen_width - self.bordure*2 and y < self.screen_height - self.bordure - self.hauteur:
                            dispfull = self.utils.tryMiddleClick(
                                self.arrayHide, int(x / 16), int((y / 16)), self.largeur, self.longueur)
                            self.fillBlocFull()
                            for i in range(len(dispfull)):
                                self.window.blit(
                                    self.sprite.getbloc_empty(), (dispfull[i][0]*16+self.bordure, dispfull[i][1]*16+self.hauteur))

                    if click[0] == True:
                        cur = pygame.mouse.get_pos()
                        y = cur[1]-self.hauteur
                        x = cur[0]-self.bordure
                        if y >= 0 and x >= 0 and x < self.screen_width - self.bordure*2 and y < self.screen_height - self.bordure - self.hauteur:
                            if self.arrayHide[int(y / 16)][int((x / 16))] == '*':
                                self.fillBlocFull()
                                self.window.blit(
                                    self.sprite.getbloc_empty(), (int(x / 16)*16+self.bordure, math.floor(y/16)*16+self.hauteur))
                            else:
                                self.fillBlocFull()

                # click gauche menu
                click = pygame.mouse.get_pressed()
                cur = pygame.mouse.get_pos()
                # si on est dans le menu
                if cur[0] > 0 and cur[0] < self.my_font.size("Niveau")[0] + 10 and cur[1] > 0 and cur[1] < self.menuHeight:
                    pygame.draw.rect(self.window, self.colorWhite,
                                     pygame.Rect(0, 0, self.my_font.size("Niveau")[0]+10, 1))
                    pygame.draw.rect(self.window, self.colorGrey,
                                     pygame.Rect(0, self.menuHeight-1, self.my_font.size("Niveau")[0]+10, 1))
                    pygame.draw.rect(self.window, self.colorWhite,
                                     pygame.Rect(0, 0, 1, self.menuHeight))
                    pygame.draw.rect(self.window, self.colorGrey,
                                     pygame.Rect(self.my_font.size("Niveau")[0]+10, 0, 1, self.menuHeight))
                else:
                    pygame.draw.rect(self.window, self.background,
                                     pygame.Rect(0, 0, self.my_font.size("Niveau")[0]+10, 1))
                    pygame.draw.rect(self.window, self.background,
                                     pygame.Rect(0, self.menuHeight-1, self.my_font.size("Niveau")[0]+10, 1))
                    pygame.draw.rect(self.window, self.background,
                                     pygame.Rect(0, 0, 1, self.menuHeight))
                    pygame.draw.rect(self.window, self.background,
                                     pygame.Rect(self.my_font.size("Niveau")[0]+10, 0, 1, self.menuHeight))
                if click[0] == True:
                    cur = pygame.mouse.get_pos()
                    # si on est dans le menu
                    if cur[0] > 0 and cur[0] < self.my_font.size("Niveau")[0] + 10 and cur[1] > 0 and cur[1] < self.menuHeight:
                        pygame.draw.rect(self.window, self.colorGrey,
                                         pygame.Rect(0, 0, self.my_font.size("Niveau")[0]+10, 1))
                        pygame.draw.rect(self.window, self.colorWhite,
                                         pygame.Rect(0, self.menuHeight-1, self.my_font.size("Niveau")[0]+10, 1))
                        pygame.draw.rect(self.window, self.colorGrey,
                                         pygame.Rect(0, 0, 1, self.menuHeight))
                        pygame.draw.rect(self.window, self.colorWhite,
                                         pygame.Rect(self.my_font.size("Niveau")[0]+10, 0, 1, self.menuHeight))
                        self.t.pause()
                        self.t.resume()

            pygame.display.update()
        return


class appThread(th.Thread):
    def __init__(self, thread) -> None:
        super(appThread, self).__init__()
        self.cnt = 0
        self.thread = thread

    def run(self) -> None:
        while True:
            self.cnt = self.thread(self.cnt)


class TimerTh(th.Thread):

    def __init__(self, *args, **kwargs):
        super(TimerTh, self).__init__(*args, **kwargs)
        self.cpt = 0
        self.__flag = th.Event()  # The flag used to pause the thread
        self.__flag.set()  # Set to True
        self.__running = th.Event()  # Used to stop the thread identification
        self.__running.set()  # Set running to True

    def run(self):
        while self.__running.is_set():
            # return immediately when it is True, block until the internal flag is True when it is False
            self.__flag.wait()
            if (self.cpt < 999):
                time.sleep(1)
                self.cpt += 1

    def pause(self):
        self.__flag.clear()  # Set to False to block the thread
        self.cpt = 0

    def resume(self):
        self.__flag.set()  # Set to True, let the thread stop blocking

    def stop(self):
        self.__flag.set()  # Resume the thread from the suspended state, if it is already suspended
        self.__running.clear()  # Set to False


t = TimerTh()
Vue(t)
