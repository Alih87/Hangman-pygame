# Importing required modules
import pygame
import random

# Initializing pygame and game window features
pygame.init()
pygame.display.set_caption("Hangman")
background = pygame.image.load("background.png")
gallows = pygame.image.load("megacropped.png")
icon = pygame.image.load("hangman30.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((800, 600))

# Open the words folder to randomly select from
with open("words.txt", "r") as f:
    sel = f.read()
    sel = sel.split()


# Chooses a letter from a given list of letters (a word)
def chooseletter(List):
    rand = random.choice(List)
    return rand


# Displays the string passed to it on the screen
def message(Str, width=0, length=0):
    font = pygame.font.Font("freesansbold.ttf", 32)
    text = font.render(Str, True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (420 + width, 146 + length)
    screen.blit(text, textRect)


# Facial Expression type 1
def expression():
    Pi = 3.14
    head = pygame.Rect(255, 137, 20, 20)
    pygame.draw.line(screen, (0, 0, 0), [256, 135], [256, 137], 3)
    pygame.draw.line(screen, (0, 0, 0), [273, 135], [273, 137], 3)
    pygame.draw.arc(screen, (0, 0, 0), head, Pi - Pi / 210, 0, 2)


# Facial Expression type 2
def expression2():
    pygame.draw.line(screen, (0, 0, 0), [256, 135], [256, 137], 3)
    pygame.draw.line(screen, (0, 0, 0), [273, 135], [273, 137], 3)
    pygame.draw.line(screen, (0, 0, 0), [256, 147], [273, 147], 3)


# Facial Expression type 3
def expression3():
    Pi = 3.14
    head = pygame.Rect(255, 143, 20, 20)
    pygame.draw.line(screen, (0, 0, 0), [256, 135], [256, 137], 3)
    pygame.draw.line(screen, (0, 0, 0), [273, 135], [273, 137], 3)
    pygame.draw.arc(screen, (0, 0, 0), head, 0, Pi - Pi / 210, 2)


def Head():
    head = pygame.Rect(240, 115, 50, 50)
    pygame.draw.ellipse(screen, (0, 0, 0), head, 5)


def Torso():
    pygame.draw.line(screen, (0, 0, 0), [263, 165], [263, 255], 3)


def Hands():
    pygame.draw.line(screen, (0, 0, 0), [263, 195], [223, 225], 3)
    pygame.draw.line(screen, (0, 0, 0), [263, 195], [303, 225], 3)


def Legs():
    pygame.draw.line(screen, (0, 0, 0), [263, 255], [223, 285], 3)
    pygame.draw.line(screen, (0, 0, 0), [263, 255], [303, 285], 3)


# Displays some part of the character with each strike
def StrikeCounter(Strike):
    if Strike == 1:
        Head()
        expression()
    elif Strike == 2:
        Head()
        Torso()
        expression2()
    elif Strike == 3:
        Head()
        Torso()
        Hands()
        expression3()
    elif Strike == 4:
        Head()
        Torso()
        Hands()
        Legs()
        expression3()


class Hangman:
    # Class constructor used to initialize important variables and lists inside the class scope
    def __init__(self, txt=None, y=None, ltxt=None, ntxt=None, index=None, space=0, strike=0, font=None,
                 text=None,
                 textRect=None, text1=None, textRect1=None, running=None):
        if index is None:
            index = list()
        if ntxt is None:
            ntxt = list()
        if ltxt is None:
            ltxt = list()
        self.running = running
        self.txt = txt
        self.ltxt = ltxt
        self.ntxt = ntxt
        self.index = index
        self.font = font
        self.text = text
        self.textRect = textRect
        self.text1 = text1
        self.textRect1 = textRect1
        self.space = space
        self.strike = strike
        self.y = y

    # Displays the word on screen which is blanked at random indices by the "blanks()" method
    def displayblanks(self, List):
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        for alph in List:
            self.space += 30
            self.text = self.font.render(alph, True, (0, 0, 0))
            self.textRect = self.text.get_rect()
            self.textRect.center = (400 + self.space, 197)
            screen.blit(self.text, self.textRect)

    # Blanks the given word at random indices
    def blanks(self):
        chose = random.choice(sel)
        self.txt = chose
        self.ltxt = list()
        self.txt = self.txt.upper()
        self.ltxt[:0] = self.txt
        self.index = list()
        self.ntxt = self.ltxt.copy()
        i = 0
        while i <= (len(self.ltxt)) // 3:
            rand = chooseletter(self.ltxt)
            self.index.append(self.ltxt.index(rand))
            self.ntxt[self.index[-1]] = "_"
            i += 1

    # Takes the user input (letter) and compares it to the letter present in the word at the index in question
    # If the letter matches, the blank is replaced by the correctly guessed letter
    # If the letter doesn't match, the blank stays and the player is penalised with a strike
    def guess(self):
        text = self.font.render("Guess:", True, (0, 0, 0))
        textrect = text.get_rect()
        textrect.center = (470, 120)
        screen.blit(text, textrect)
        if (self.y is not None) and (self.y != ""):
            x = self.y
            x = x.upper()
            check = x in self.ltxt
            if check:
                check1 = self.ntxt[self.ltxt.index(x)] == "_"
                if check1:
                    self.ntxt[self.ltxt.index(x)] = x
                    self.y = ""
                    return
                else:
                    self.strike += 1
                    self.y = ""
                    return
            else:
                self.strike += 1
                self.y = ""
                return
        else:
            return

    # This is the main function with the while loop for the game events
    # This function is recursive, and initiates itself again if the user wants to "Play again"
    def Main(self):
        self.strike = 0
        threshold = 230
        z = ""
        self.blanks()
        self.running = True
        while self.running:          # Game's main while loop
            while self.strike < 4:   # This loop ends as soon as strikes count hit 4
                self.space = 0
                for self.events in pygame.event.get():
                    self.font = pygame.font.Font("freesansbold.ttf", 32)
                    if self.events.type == pygame.QUIT:
                        self.running = False
                    if self.events.type == pygame.KEYDOWN:
                        if self.events.unicode.isalpha():
                            z += self.events.unicode
                        elif self.events.key == pygame.K_BACKSPACE:
                            z = z[:-1]
                        elif self.events.key == pygame.K_RETURN:
                            self.y = z
                            z = ""
                    elif self.events.type == pygame.QUIT:
                        return
                screen.blit(background, (0, 0))
                screen.blit(gallows, (70, 52))
                StrikeCounter(self.strike)
                for x in range(gallows.get_width()):            # In order for the screen to display the black gallows
                    for y in range(gallows.get_height()):       # animation only we use these for loops to find and light
                        color = gallows.get_at((x, y))          # color above the codes of (230, 230, 230) and replace with the actual background
                        if color.r > threshold and color.g > threshold and color.g > threshold:
                            gallows.set_at((x, y), (0, 0, 0, 0))
                text = self.font.render(z, True, (0, 0, 0))
                textrect = text.get_rect()
                textrect.center = (560, 120)
                screen.blit(text, textrect)
                self.guess()
                self.displayblanks(self.ntxt)
                pygame.display.update()
                if self.ntxt == self.ltxt:
                    screen.blit(background, (0, 0))
                    message("Well Done!")
                    message("Play again? (Y/N)", 0, 52)
                    for self.events in pygame.event.get():
                        if self.events.type == pygame.KEYDOWN:
                            if self.events.key == pygame.K_y:
                                self.Main()
                                return
                            elif self.events.key == pygame.K_n:
                                self.running = False
                                return
                    pygame.display.update()
                elif self.strike == 4:
                    Legs()                       # This and the next two lines are written to to make sure
                    pygame.display.update()      # that the legs of the character are displayed before the
            pygame.time.wait(500)                # display is updated
            screen.blit(background, (0, 0))
            message("The word was: " + self.txt)
            message("Play again? (Y/N)", 0, 52)
            for self.events in pygame.event.get():
                if self.events.type == pygame.KEYDOWN:
                    if self.events.key == pygame.K_y:
                        self.Main()
                        return
                    elif self.events.key == pygame.K_n:
                        self.running = False
                        return
                if self.events.type == pygame.QUIT:
                    self.running = False
            pygame.display.update()


if __name__ == '__main__':
    word = Hangman()
    word.blanks()
    word.Main()
