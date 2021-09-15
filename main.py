
import threading
from threading import Thread
import random
import turtle
import time

#Creates a Timer class to be used to countdown 10s. It contains some initial values and
#has methods to start and stop the timer which can be called by functions. 
class Timer(turtle.Turtle):
    def __init__(self,action):
        turtle.Turtle.__init__(self)
        self.sec = 10
        self.action = action
        self.cancelled = False
        self.ht()
        self.penup()
        self.goto(-78,180)
        timer_erase()
        # self.write(str(self.sec))
    def start(self):
        self.clear()
        timer_erase()
        self.write(str(self.sec), font = ("Arial", 30, "bold"), align = "center")
        self.sec -= 1
        if self.cancelled == False:
            if self.sec > -1:
                screen.ontimer(self.start, 1000)
            else:
                self.action()
    def cancel(self):
        self.cancelled = True
        timer_erase()
        self.sec = 0

#Creates a class for Players, containing information regarding their names, amount of 
#money they have. This class has useful functions to add money, and to bankrupt.
class WOFPlayer:
    def __init__(self, name):
        self.name = name
        self.prizeMoney = 0
        self.prizes = []

    def addMoney(self, amt):
        self.prizeMoney = self.prizeMoney + amt

    def goBankrupt(self):
        self.prizeMoney = 0


#Setup screen and creates turtle called don.
screen = turtle.Screen()
screen.setup(width=1000, height=600, startx=150, starty=20)
screen.tracer(0)
don = turtle.Turtle(visible = False)
don.speed(0)

#imports the wheel pictures for spinning
screen.bgpic("bg.gif")

wheels = ["wheels/wheel1.gif", "wheels/wheel2.gif", "wheels/wheel3.gif", "wheels/wheel4.gif",
            "wheels/wheel5.gif", "wheels/wheel6.gif", "wheels/wheel7.gif", "wheels/wheel8.gif",
            "wheels/wheel9.gif", "wheels/wheel10.gif", "wheels/wheel11.gif", "wheels/wheel12.gif",
            "wheels/wheel13.gif", "wheels/wheel14.gif", "wheels/wheel15.gif", "wheels/wheel16.gif",
            "wheels/wheel17.gif", "wheels/wheel18.gif", "wheels/wheel19.gif", "wheels/wheel20.gif",
            "wheels/wheel21.gif", "wheels/wheel22.gif", "wheels/wheel23.gif", "wheels/wheel24.gif"]

for i in wheels:
    turtle.register_shape(i)
turtle.register_shape("timer1.gif")
#---------------------------------------------
#GLOBAL VIARIABLES
timer = 0
k = 0
timeup_flag = False
spin_flag = False
buy_vowel_flag = False
call_consonant_flag = False
solve_puzzle_flag = False

ACTUAL_PHRASE = ''
DISPLAY_PHRASE = ''
player_count = 0
player1,player2,player3 = WOFPlayer('Player 1'), WOFPlayer('Player 2'), WOFPlayer('Player 3')
players = [] 
curr_player = 0
wheel =['BANKRUPT', 300, 500, 450, 500, 800,'LOSE A TURN', 700,'FREE PLAY', 650, 'BANKRUPT', 900,
                500, 350, 600, 500, 400, 550, 800, 300, 700, 900, 500, 5000]
consonants = 'BCDFGHJKLMNPQRSTVWXYZ'
vowels = 'AEIOU'
available_letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
#---------------------------------------------

#Function to draw rectangle. Position (x,y) is the top left corner of the box.
def draw_rec(x,y,width, height, fill_color = 'white'):
    don.penup()
    don.setpos(x,y)
    don.pendown()
    don.fillcolor(fill_color)
    don.begin_fill()
    for i in range(2):
        don.forward(width)
        don.right(90)
        don.forward(height)
        don.right(90)
    don.end_fill()
    don.penup()

#Whenever the player clicks on the screen, this function checks for the clicked
#position and determines if buttons can be pressed. If pressed, will deactivate all
#buttons. 
def check_coordinate(x,y):
    global wheel
    global timer
    global spin_flag, buy_vowel_flag, call_consonant_flag, solve_puzzle_flag
    global player1, player2, player3
    if -250<=y and y<=-220: 
        if (-30<=x and x<=60 and call_consonant_flag) : # call consonant button location
            deactivate_all()
            call_consonant(wheel[0])
            
        if (101<=x and x<=181 and buy_vowel_flag): #buy vowel button location
            deactivate_all()
            buy_vowel()
            
        if (222<=x and x<=302 and solve_puzzle_flag):
            deactivate_all()
            solve_puzzle()
            
        if (343<=x and x<=423 and spin_flag):
            deactivate_all()
            spin_wheel()
        
turtle.onscreenclick(check_coordinate, 1)
turtle.listen()


#Function to deactivate all the buttons. Players will not be able to click on them.
def deactivate_all():
    global spin_flag, buy_vowel_flag, call_consonant_flag, solve_puzzle_flag
    spin_flag = buy_vowel_flag = call_consonant_flag = solve_puzzle_flag = False
    #Call Consonant button
    draw_rec(-30, -220, 90, 30, fill_color= "dimgray")
    don.setpos(-30+6,-243)
    don.color("white")
    don.write("Call consonant", font=("Arial", 8, "bold"))
    don.color("black")
    #Buy Vowel button
    draw_rec(101, -220, 80, 30, fill_color= "dimgray")
    don.setpos(-20+136,-243)
    don.color("white")
    don.write("Buy vowel", font=("Arial", 8, "bold"))
    don.color("black")
    #Solve Button
    draw_rec(222, -220, 80, 30, fill_color = "dimgray")
    don.setpos(-20+121*2+27,-243)
    don.color("white")
    don.write("Solve", font=("Arial", 8, "bold"))
    don.color("black")
    #Spin button
    draw_rec(343, -220, 80, 30, fill_color= "dimgray")
    don.setpos(-20+121*3+27,-243)
    don.color("white")
    don.write("Spin", font=("Arial", 8, "bold"))
    don.color("black")
deactivate_all()

#Below are active functions for the various buttons. Once activated, players
# will then be able to click on the buttons. 
def activate_call_consonant():
    global call_consonant_flag
    call_consonant_flag = True
    draw_rec(-30, -220, 90, 30, fill_color= "lemonchiffon")
    don.setpos(-30+6,-243)
    don.write("Call Consonant", font=("Arial", 8, "bold"))

def activate_buy_vowel():
    global buy_vowel_flag
    buy_vowel_flag = True
    draw_rec(101,-220, 80, 30, fill_color= "lemonchiffon")
    don.setpos(-20+136,-243)
    don.write("Buy Vowel", font=("Arial", 8, "bold"))

def activate_solve():
    global solve_puzzle_flag
    solve_puzzle_flag = True
    draw_rec(222,-220, 80, 30, fill_color= "lemonchiffon")
    don.setpos(-20+121*2+27,-243)
    don.write("Solve", font=("Arial", 8, "bold"))

def activate_spin():
    global spin_flag
    spin_flag = True
    draw_rec(343, -220, 80, 30, fill_color= "lemonchiffon")
    don.setpos(-20+121*3+30,-243)
    don.write("Spin", font=("Arial", 8, "bold"))
    
    
#Draws Countdown Timer
timer_bg = turtle.Turtle()
timer_bg.penup()
timer_bg.setpos(-80,220)
timer_bg.shape("timer1.gif")
screen.update()

timer_eraser = turtle.Turtle() 
timer_eraser.penup()
timer_eraser.setpos(-80,170)
timer_eraser.color("white", "white")
def timer_erase():
    timer_eraser.pendown()
    timer_eraser.begin_fill()
    timer_eraser.circle(25)
    timer_eraser.end_fill()
    timer_eraser.pendown()

timer_pen = turtle.Turtle(visible = False) 
timer_pen.penup()
timer_pen.setpos(-78, 180)

    
#This function will be activated when time is up. Tells user to close input screen.
def timesup_input():
    global timeup_flag
    timeup_flag = True
    string = "TIME IS UP! please close the pop-up text input"
    change_display(string)

        
#displays instruction
draw_rec(0,-150,400,50)
don.penup()
don.setpos(3, -145)
don.color("white")
don.write("INSTRUCTIONS", font=("Arial", 8, "bold"))
don.color("black")

instruction = turtle.Turtle(visible = False)
instruction.penup()
instruction.setpos(10, -185)
instruction.pendown()
instruction.write("Welcome to Wheel of Fortune".upper(), font=("Arial", 10, "bold"))

#For drawing of player's name  at the top where it displays the amount of money 
#each of the player has
player_name = turtle.Turtle(visible = False)       #Used to write player's name
player_name.penup()
def draw_player_name(name1, name2, name3):
    #Draw Player1 Box
    draw_rec(32,280,100,60)
    draw_rec(32,260,100,40)
    player_name.setpos(82,263)
    player_name.write(name1, align = "center")
    #Draw Player2 Box
    draw_rec(153,280,100,60)
    draw_rec(153,260,100,40)
    player_name.setpos(203,263)
    player_name.write(name2, align = "center")
    #Draw Player3 Box
    draw_rec(274,280,100,60)
    draw_rec(274,260,100,40)
    player_name.setpos(324,263)
    player_name.write(name3, align = "center")

player_money = turtle.Turtle(visible = False)
player_money.penup()
#Whenever there is a change in the amount of money, this function updates the screen.
def update_money(p1,p2,p3):
    player_money.clear()
    #write player1 money
    player_money.setpos(82,230)
    player_money.write("$" + str(p1), font = ('Arial', 12, 'bold'), align="center")
    #write player2 money 
    player_money.setpos(203,230)
    player_money.write("$" + str(p2), font = ('Arial', 12, 'bold'), align = "center")
    #write player3 money
    player_money.setpos(324,230)
    player_money.write("$" + str(p3), font = ('Arial', 12, 'bold'), align = "center")


wheel_pen = turtle.Turtle()
wheel_pen.penup()
wheel_pen.setpos(-250, -50)
wheel_pen.pendown()
wheel_pen.shape("wheels/wheel1.gif")
screen.update()

#Animation of the spinning of wheels
def spin_wheel_show(j):
    global wheels
    for i in range(j):
        n = wheels.pop(0)
        wheels.append(n)
        wheel_pen.shape(wheels[0])
        screen.update()
        time.sleep(0.1)
        
#Draw triangle at the top of the wheel to determine the ending position of the wheel.
triangle_pen = turtle.Turtle()
triangle_pen.penup()
triangle_pen.resizemode("user")
triangle_pen.shapesize(2,3,2)
triangle_pen.setpos(-250,220)
triangle_pen.color("orange", "yellow")
triangle_pen.shape("triangle")
triangle_pen.right(90)
screen.update()

#frame for the display of phrase
rec_x, rec_y = 0, 200
draw_rec(rec_x - 5,rec_y + 5,410,210, "darkorchid")
draw_rec(rec_x,rec_y,400,200, "darkblue")

#draws out the boxes to show the phrase 
def draw_white():
    rec_x, rec_y = 0, 200
    y = rec_y - 1
    for i in range(4):
        x = rec_x + 2
        for j in range(15):
            draw_rec(x,y,25,48)
            x += 26.5
        y -= 50
draw_white()
    

##  draws out the boxes to show available letters
y_a = -25
for i in range(2):
    x_a = rec_x + 2 + 26.5
    for j in range(13):
        draw_rec(x_a,y_a,25,48)
        x_a += 26.5
    y_a -= 50
letters_pen = turtle.Turtle(visible = False)
phrase_pen = turtle.Turtle(visible = False)

#displays updated available letters everytime its called
#vowels are displayed in red
def update_letters_display(available_letters, vowels):
    letters_pen.clear()
    y = -70
    for i in range(2):
        x = 34
        for j in range(13):
            letters_pen.color('black')
            if available_letters[j + 13*i] in vowels:
                letters_pen.color('red')
            letters_pen.penup()
            letters_pen.setpos(x,y)
            letters_pen.pendown()
            letters_pen.write(available_letters[j + 13*i], font = ('Arial', 15, 'bold'))
            x += 26.5
        y -= 50

# updates the phrase to be displayed.
# called at the start and everytime a letter is correctly guessed or phrase solved
def update_display_phrase(display_phrase):
    phrase_pen.clear()
    display_phrase = display_phrase.split(' ')
    total_len = 0
    count = 0
    display = [[],[],[],[]]
    for i in display_phrase:
        if len(i) + total_len < 15:
            total_len += len(i) +1 
        else:
            total_len = len(i)
            count += 1
        display[count].append(i)
    for j in range(len(display)):
        display[j] = ' '.join(display[j])
    y = 199
    for i in range(4):
        x = 2
        for j in range(len(display[i])):
            if display[i][j] == '_':
                string = ' '
            else:
                string = display[i][j]
            if display[i][j] != " ":
                draw_rec(x,y,25,48, 'light green')
                x += 2
                y -= 45
                phrase_pen.penup()
                phrase_pen.setpos(x+5,y+8)
                phrase_pen.pendown()
                phrase_pen.write(string, font = ('Arial', 15, 'bold'))
                phrase_pen.penup()
                y += 45
                x -= 2
            
            x += 26.5
        y -= 50

##gets a vowel from the players through pop up text input 
# starts the timer so that the player has 10s to input their choice 
#returns None is 10s are up               
def get_vowel():
    global timeup_flag
    global timer
    timer = Timer(timesup_input)
    timer.start()
    k = screen.textinput("Vowel", "Enter your vowel: ")
    if timeup_flag:
        timeup_flag = False
        return None
    else:
        timer.cancel()
        return k
        
##gets a consonant from the players through pop up text input 
# starts the timer so that the player has 10s to input their choice    
def get_consonant():
    global timeup_flag
    global timer

    timer = Timer(timesup_input)
    timer.start()
    k = screen.textinput("Consonant", "Enter your consonant: ")
    if timeup_flag:
        timeup_flag = False
        return None
    else:
        timer.cancel()
        return k

##gets the letter from the players through pop up text input 
# starts the timer so that the player has 10s to input their choice            
def get_letter():
    global timeup_flag
    global timer
    timer = Timer(timesup_input)
    timer.start()
    k = screen.textinput("Letter", "Enter your letter: ") 
    if timeup_flag:
        timeup_flag = False
        return None
    else:
        timer.cancel()
        return k

##gets the solution from the players through pop up text input 
# starts the timer so that the player has 10s to input their choice         
def get_solution():
    global timeup_flag
    global timer
    timer = Timer(timesup_input)
    timer.start()
    k = screen.textinput("Solution", "Enter your solution: ") 
    if timeup_flag:
        timeup_flag = False
        return None
    else:
        timer.cancel()
        return k

#gets the decision from the players on whether to continue after puzzle is solved through pop up text input
def get_new_round():
    k=0
    while ((k != 'Y') and (k != 'N')):
        k = screen.textinput("Start New Round", "Input Y or N")
    return k

#changes the instruction displayed on the instruction box
def change_display(prompt):
    prompt = prompt.upper()
    instruction.clear()
    instruction.write(prompt, font=("Arial", 10, "bold"))

#gets the names of the players from the players through pop up text input    
def get_names():
    name1 = screen.textinput("player1", "Enter player 1 name:")
    name2 = screen.textinput("player2", "Enter player 2 name:")
    name3 = screen.textinput("player3", "Enter player 3 name:")
    return [name1, name2, name3]








#############################################################################
## PYTHON FUNCTIONS ##






# changes the status of the current player to the next person. activated everytime a player loses
def get_next_player():
    global player_count
    global players
    global curr_player
    player_count += 1
    # return players[player_count%3]
    curr_player = players[player_count%3]
    

#checks whether an input is a valid consonant or vowel(i.e. not alr guessed and is a consonant or vowel)
def check_letter(k, option):
    global vowels
    global consonants
    global curr_player
    global available_letters
    if option == 'c':
        x = consonants
    elif option == 'v':
        x = vowels

    try:
        k = k.upper()
        if (k in x and k in available_letters and len(k) == 1):
            # if (option == 'c' or curr_player.prizeMoney >= 250):
            available_letters[available_letters.index(k)] = ' '
            update_letters_display(available_letters, vowels)
            return True
        else:
            return False
    except:
        return False




#checks whether the letter is in the phrase and compares with current display phrase.
#If it is, update display phrase and returns a list [True,count]
#If not in phrase, then return [False, 0]
def check_inphrase(k):
    global DISPLAY_PHRASE
    global ACTUAL_PHRASE
    NEW_DISPLAY_PHRASE = ""
    length = len(ACTUAL_PHRASE)
    count = 0
    if(k.upper() in ACTUAL_PHRASE):
        for i in range(length):
            if k.upper() == ACTUAL_PHRASE[i]:
                NEW_DISPLAY_PHRASE += ACTUAL_PHRASE[i]
                count += 1
            else:
                NEW_DISPLAY_PHRASE += DISPLAY_PHRASE[i]
        DISPLAY_PHRASE = NEW_DISPLAY_PHRASE
        update_display_phrase(DISPLAY_PHRASE)
        return (True, count)
    else:
        return (False, 0)


# called upon for every decision not from spin. allows player to click the buy vowel (if they have enough money), spin or solve buttons 
def choose_action():
    global curr_player
    if curr_player.prizeMoney>=250:
        string = curr_player.name + ", Buy Vowel, Spin Wheel or Solve."
    else:
        string = curr_player.name + ", Spin Wheel or Solve."
    change_display(string)

    activate_solve()
    activate_spin()
    if curr_player.prizeMoney>=250:
        activate_buy_vowel()
    

#is called upon if the spin falls on any number. allows the player to choose bet buy vowel(if they have enough money), solve, or call consonant
def Number(amount):
    global timer
    if curr_player.prizeMoney>=250:
        string = "Please Buy Vowel, Call Consonant or Solve"
    else:
        string = "Please Call Consonant or Solve"
    change_display(string)
    
    if curr_player.prizeMoney>=250:
        activate_buy_vowel()
    activate_call_consonant()
    activate_solve()


#claled upon when player clicks call_consonant
def call_consonant(amount):
    global curr_player
    string = curr_player.name + ", choose any available consonant."
    change_display(string)
    k = get_consonant()
    if k == None:
        get_next_player()
    else:
        if not check_letter(k, 'c'):
            string = "Consonant not valid!"
            change_display(string)
            get_next_player()
            
        else:
            status = check_inphrase(k)
            if status[0]:
                curr_player.addMoney(status[1] * amount)
                update_money(player1.prizeMoney, player2.prizeMoney, player3.prizeMoney)
                string = "Consonant is in phrase!"
                change_display(string)
            else:
                string = "Consonant not in phrase."
                change_display(string)
                get_next_player()
    time.sleep(1.5)
    choose_action()    

#called upon when player clicks buy vowel. player can input any vowel from the available ones. invalid(not available or not a vowel) vowel will result in the turn going to the net player
def buy_vowel():
    global curr_player
    string = curr_player.name + ", choose any available vowel."
    change_display(string)
    v = get_vowel()
    if v == None:
        get_next_player()
    else:
        curr_player.addMoney(-250)
        update_money(player1.prizeMoney, player2.prizeMoney, player3.prizeMoney)
        if not check_letter(v, 'v'):
            string = "Vowel not valid!"
            change_display(string)
            get_next_player()        
        else:
            if(check_inphrase(v)[0]):
                string = "Right choice!"
                change_display(string)
            else:
                string = "Vowel not in phrase."
                change_display(string)
                get_next_player()
    time.sleep(1.5)
    choose_action()

# called upon when spin falls on free play. player can input any letter from the available letters. invalid inputs will allow the player to have another turn
def free_play():
    global curr_player

    string = curr_player.name + ", choose any available letter."
    change_display(string)
    k = get_letter()
    if k != None:
        if not check_letter(k, 'v') and not check_letter(k, 'c'):
            string = "Letter not valid!"
            change_display(string)
        elif not (check_inphrase(k)[0]) :
            string = "Letter not in phrase."
            change_display(string)
    time.sleep(1.5)
    choose_action()



#called upon when player clicks solve. player can choose to continue where a new phrase is set or the game ends
def solve_puzzle():
    global available_letters
    global vowels
    global curr_player
    global DISPLAY_PHRASE
    global ACTUAL_PHRASE
    global timer
    solution = get_solution()
    if (solution != None):
        if solution.upper() == ACTUAL_PHRASE:
            player = players[(player_count+1)%3]
            player.goBankrupt()
            player = players[(player_count+2)%3]
            player.goBankrupt()
            update_money(player1.prizeMoney, player2.prizeMoney, player3.prizeMoney)
            update_display_phrase(ACTUAL_PHRASE)
            time.sleep(1)
            player = players[(player_count+3)%3]
            string = player.name + " won with $" + str(player.prizeMoney) + ". The game has ended!"
            change_display(string)                       

            time.sleep(4)
            x = get_new_round()
            if x == 'Y':
                get_display_phrase()
                draw_white()
                update_display_phrase(DISPLAY_PHRASE)
                available_letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                update_letters_display(available_letters, vowels)
                curr_player = player
                string = curr_player.name +  " starts. Please press spin wheel."
                change_display(string)
                activate_spin()
                if curr_player.prizeMoney>=250:
                    activate_buy_vowel()
            else:
                string = "Thank you for playing wheel of fortune!"
                change_display(string)
                time.sleep(4)
                
        else:
            string = solution + ' is wrong!' 
            change_display(string)
            get_next_player()
            time.sleep(1.5)
            choose_action()
    else:
        time.sleep(1.5)
        get_next_player()
        choose_action()


## is called once player presses spin
def spin_wheel():
    global curr_player
    global wheel

    random_spin = random.randint(40, 64)
    spin_wheel_show(random_spin) # spin the physical wheel
    for i in range(random_spin):
        n = wheel.pop(0)
        wheel.append(n)
        choice = wheel[0]

    if choice == "BANKRUPT":
        curr_player.goBankrupt()
        update_money(player1.prizeMoney, player2.prizeMoney, player3.prizeMoney)
        string = "You have been BANKRUPT!" 
        change_display(string)
        time.sleep(1.5)
        get_next_player()
        choose_action()
        
    elif choice == "LOSE A TURN":
        string = "You lost your turn!"
        change_display(string)
        time.sleep(1.5)
        get_next_player()
        choose_action()
        
    elif choice == "FREE PLAY":
        string = "You have selected Free Play!"
        change_display(string)
        time.sleep(1.5)
        free_play()
        
    else:
        string = "You have selected $ " + str(choice)
        change_display(string)
        time.sleep(1.5)
        Number(choice)
# gets a new phrase to be guesses everytime its called
def get_display_phrase():
    global ACTUAL_PHRASE
    global DISPLAY_PHRASE
    myfile = open("Text File.txt")
    content = myfile.readlines()
    myfile.close()
    i = random.randint(0, len(content)-1)
    ACTUAL_PHRASE = content[i][0:-1]
    DISPLAY_PHRASE = ''
    for i in ACTUAL_PHRASE:
        if i == ' ':
            DISPLAY_PHRASE += ' '
        else:
            DISPLAY_PHRASE += '_'

# starts the whole game by getting the players names and initialising the game parameters(eg.money displays the blanks etc)
def get_players_name():
    global DISPLAY_PHRASE
    global player1, player2, player3, players, curr_player
    global timer
    draw_player_name("Player1", "Player2", "Player3")
    get_display_phrase()
    names = get_names()
    if names[0] != None and names[0] != '':
        player1 = WOFPlayer(names[0])
    if (names[1] != None and names[1] != ''):
        player2 = WOFPlayer(names[1])
    if (names[2] != None and names[2] != ''):
        player3 = WOFPlayer(names[2])
    draw_player_name(player1.name, player2.name, player3.name)
    players = [player1, player2, player3]
    curr_player = player1
    string = curr_player.name +  " starts. Please press spin wheel."
    change_display(string)
    update_display_phrase(DISPLAY_PHRASE)
    update_letters_display(available_letters, vowels)
    update_money(player1.prizeMoney, player2.prizeMoney ,player3.prizeMoney)
    activate_spin()

get_players_name()

turtle.done()



