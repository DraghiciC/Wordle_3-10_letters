import pygame
import random


# load all words from dictionary
def load_words():
    with open('words.txt') as word_file:
        valid_words = set(word_file.read().split())
    return valid_words


# match guess with secret word
def match(text):
    ltext = list(text.strip(" "))
    lsecret = list(secret_word.strip(" "))
    x = [0 for i in range(0, length)]
    for i in range(0, length):
        if ltext[i] == lsecret[i]:  # 2 if the letter is in the correct place
            x[i] = 2
            lsecret[i] = "0"
    for i in range(0, length):
        if x[i] == 0:  # 0 if the letter is not in the secret word
            for j in range(0, length):
                if ltext[i] == lsecret[j]:  # 1 if the letter is in the secret word in the wrong place
                    x[i] = 1
                    lsecret[j] = 0
                    break
    return x


# check if windows was closed
def check_quit(event):
    if event.type == pygame.QUIT:
        return True
    return False


# display title and background color
def display_title():
    screen.fill((50, 50, 50))
    screen.blit(img1, (25, 20))


# display options
def display_options():
    screen.blit(img2, (500 - (img2.get_width() / 2), 140))
    for i in range(0, 4):
        pygame.draw.rect(screen, (100, 100, 100), (20 + 245 * i, 200, 225, 300))
        img = font3.render(str(i + 3), True, (200, 200, 200))
        screen.blit(img, (85 + 245 * i, 250))
    for i in range(0, 3):
        pygame.draw.rect(screen, (100, 100, 100), (20 + 245 * i, 550, 225, 300))
        img = font3.render(str(i + 7), True, (200, 200, 200))
        screen.blit(img, (85 + 245 * i, 600))
    pygame.draw.rect(screen, (100, 100, 100), (20 + 245 * 3, 550, 225, 300))
    img = font3.render(str(10), True, (200, 200, 200))
    screen.blit(img, (15 + 245 * 3, 600))


# pick from the displayed options
def pick_length(event):
    global length, choosing
    if event.type == pygame.MOUSEBUTTONUP:
        pos = pygame.mouse.get_pos()
        if 200 < pos[1] < 500:
            for i in range(0, 4):
                if (20 + 245 * i) < pos[0] < (225 + 245 * i):
                    length = i + 3
                    choosing = False
        if 550 < pos[1] < 850:
            for i in range(0, 4):
                if (20 + 245 * i) < pos[0] < (225 + 245 * i):
                    length = i + 7
                    choosing = False


# filter words by length and choose secret word
def pick_word():
    global words, secret_word, setup
    for word in english_words:
        if len(word) == length:
            words.append(word)
    secret_word = random.choice(words)
    print("found " + str(len(words)) + " " + str(length) + "-letter words")
    print(secret_word)
    setup = False


# display message if correct word and "press enter to play again"
def display_win_message():
    img = font3.render("You win!", True, (200, 200, 200))
    screen.blit(img, (500 - img.get_width() / 2, 300))
    img = font6.render("Press enter to play again", True, (200, 200, 200))
    screen.blit(img, (500 - img.get_width() / 2, 600))


# resets the variables to the initial state
def reset_state():
    global win, lose, color, used_words, running, setup, choosing, length, used_letters, english_words, words, secret_word, text
    win = False
    lose = False
    color = (0, 0, 0)
    used_words = []
    running = True
    setup = True
    choosing = True
    length = 0
    used_letters = [-1 for i in range(0, 26)]
    english_words = load_words()
    words = []
    secret_word = ""
    text = ""


# display message if lost, secret word and "press enter to play again"
def display_lose_message():
    img = font3.render("You lose!", True, (200, 200, 200))
    screen.blit(img, (500 - img.get_width() / 2, 300))
    img = font6.render("The word was " + secret_word, True, (200, 200, 200))
    screen.blit(img, (500 - img.get_width() / 2, 600))
    img = font6.render("Press enter to play again", True, (200, 200, 200))
    screen.blit(img, (500 - img.get_width() / 2, 700))


# setup
def setup_game(ev):
    display_options()  # draw options on screen
    for event in ev:  # check position of mouse click and select word length
        pick_length(event)
    if not choosing:  # select words of chosen length from the dictionary and pick a random secret word
        pick_word()


# win
def win_game(ev):
    global running
    display_win_message()  # display win message
    # check for keypress
    for event in ev:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # reset game if pressed enter key
                reset_state()
            else:
                running = False


# lose
def lose_game(ev):
    global running
    display_lose_message()  # display lose message
    for event in ev:  # check for keypress
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # reset game if pressed enter key
                reset_state()
            else:
                running = False


# draw random messages/ comments and guess rectangles
def draw_messages():
    # draw empty guess rectangles
    for i in range(0, length):
        pygame.draw.rect(screen, (100, 100, 100),
                         (100 * (10 - length) / 2 + 10 / 2 + 90 * i + 10 * i, 150, 90, 135))
    # draw messages
    img = font5.render(text1, True, (200, 200, 200))
    screen.blit(img, (420, 30))
    img = font5.render(text2, True, (200, 200, 200))
    screen.blit(img, (420, 70))


# add word to the used words list, the letters of the word to the used letters list and assign them correctness
# scores (0/1/2 = letter not in word/ letter in word on wrong position/ letter in worn on correct position)
# check if the input word matches the secret word
def compute():
    global win
    x = match(text)  # match the word with the secret word
    for i in range(0, length):  # add the letters to the used letters list
        for j in range(0, 26):
            if text[i] == aux1[j] and used_letters[j] < x[i]:
                used_letters[j] = x[i]
    flg = True
    for i in x:  # check if all the letters are in the correct place
        if i != 2:
            flg = False
    if flg:
        print("you win")
        win = True
    used_words.append((text, x))  # add chosen to the used words list


# check the input word
def try_word():
    global text1, text2, text
    print(text)
    if len(text) != length:  # if the word is too short
        text1 = "Those aren't " + str(length) + " letters"
        text2 = "Do you know how to count?"
    elif text in words:  # if the word is in the dictionary
        text1 = "So you chose " + text + "?"
        text2 = random.choice(condecending_list)
        compute()
    else:  # if the word is not in the dictionary
        text1 = "What is " + text + "?"
        text2 = random.choice(insult_list)
    text = ''


# handles the keyboard input
def keyboard_input(ev):
    global lose,text
    for event in ev:  # handle input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # pressed "Enter"
                try_word()
            elif event.key == pygame.K_BACKSPACE:  # delete last written letter
                text = text[:-1]
            elif event.key == pygame.K_ESCAPE:  # give up, lose the game
                lose = True
            elif len(text) < length:  # add pressed key to the guess word
                text += event.unicode
    for i in range(0, length):  # draw letters in the guess rectangles
        if i < len(text):
            img = font4.render(text[i].upper(), True, (200, 200, 200))
            screen.blit(img, (45 - img.get_width() / 2 + 100 * (10 - length) / 2 + 10 / 2 + 90 * i + 10 * i, 170))


# draw and color the used letters
def draw_used_letters():
    for i in range(0, 26):  # draw the used letters and color their rectangles
        if used_letters[i] == 1:
            color = (255, 255, 50)
        elif used_letters[i] == 2:
            color = (50, 255, 50)
        elif used_letters[i] == -1:
            color = (100, 100, 100)
        else:
            color = (50, 50, 50)
        pygame.draw.rect(screen, color,
                         (7 + 38 * i, 300, 35, 45))
        img = font5.render(aux1[i].upper(), True, (50, 50, 50))
        screen.blit(img, (10 + 38 * i, 310, 35, 45))


# draw and color used words
def draw_used_words():
    for i in range(0, len(used_words)):  # draw the used words
        txt = used_words[len(used_words) - i - 1][0]
        x = used_words[len(used_words) - i - 1][1]
        for j in range(0, length):  # choose right color for each letter
            aux = int(i / 2)
            if x[j] == 2:
                color = (50, 255, 50)
            elif x[j] == 1:
                color = (255, 255, 50)
            else:
                color = (200, 200, 200)
            img = font5.render(txt[j].upper(), True, (50, 50, 50))
            # draw the rectangles and letters on screen
            if i % 2 == 0:
                pygame.draw.rect(screen, color,
                                 (5 + 40 * j, 350 + aux * 50, 30, 45))
                screen.blit(img, (20 - img.get_width() / 2 + 40 * j, 373 + aux * 50 - img.get_height() / 2, 30, 45))
            else:
                pygame.draw.rect(screen, color,
                                 (500 + 40 * j, 350 + aux * 50, 30, 45))
                screen.blit(img,
                            (515 - img.get_width() / 2 + 40 * j, 373 + aux * 50 - img.get_height() / 2, 30, 45))


# initialisation
pygame.init()
screen = pygame.display.set_mode([1000, 1000])
font1 = pygame.font.SysFont(None, 155)
img1 = font1.render('Wordle', True, (200, 200, 200))
font2 = pygame.font.SysFont(None, 50)
img2 = font2.render('Select word length:', True, (200, 200, 200))
font3 = pygame.font.SysFont(None, 300)
font4 = pygame.font.SysFont(None, 150)
font5 = pygame.font.SysFont(None, 40)
font6 = pygame.font.SysFont(None, 100)
length = 0  # chosen length of words
aux1 = "qwertyuiopasdfghjklzxcvbnm"  # all letters
used_letters = [-1 for i in range(0, 26)]  # list fo all values of the letters
english_words = load_words()  # loading all words from dictionary
words = []
secret_word = ""
text = ""
text1 = "Another stupid human..."
text2 = "Let's see what you got"
insult_list = ["Go read a dictionary!",
               "Do you know how to play this game?",
               "Maybe you should let someone else play",
               "Give me a break",
               "I hate you",
               "Can someone else play? Please?",
               "Your english teacher should be ashamed",
               "Did you even go to school?"]
condecending_list = ["You think that would help you?",
                     "Bad choice",
                     "Can you bring someone smarter?",
                     "You don't deserve to win",
                     "Laughable",
                     "Losers usually pick that one",
                     "It's so bad. I'm impressed"]
used_words = []  # list of used words
color = (0, 0, 0)
win = False
lose = False
running = True
setup = True
choosing = True

# main loop
while running:
    ev = pygame.event.get()
    for event in ev:
        if check_quit(event):  # check if escape key is pressed
            running = False
    display_title()  # display title and background color
    if setup:  # display options and choose word length
        setup_game(ev)
    elif win:  # display win screen
        win_game(ev)
    elif lose:  # display lose screen
        lose_game(ev)
    else:
        draw_messages()  # draw messages and guess rectangles
        keyboard_input(ev)
        draw_used_letters()
        draw_used_words()
    pygame.display.flip()
pygame.quit()
