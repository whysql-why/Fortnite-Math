print("Hello world!")
import os
from libs import utils
# os.system("pip install pyyaml")
# os.system("pip install pillow")
from libs import data, question, config, AssetManagement, GameState, Anticheat, sql
from networking import packets
import random, sys, pygame, time, uuid, threading

session_id = uuid.uuid4()
# ============================================= 
multiplayer = False
not_connected = True
server_ip = "127.0.0.1"
server_port = 25565
username = "test"
# ============================================= 
# default port for Fortnite Math is 25565
# same as minecraft

if(multiplayer):
    GameState.set_state('multiplayer_var', True)
    # very good checks!! anticheat is client sided
    # "never trust the client"
    Anticheat.enable()

# <<<< Let's talk about setting different functions for different modes or states of the game
# yes done

# issues:
# f̶p̶s̶ ̶l̶a̶g̶:̶ ̶I̶ ̶t̶h̶i̶n̶k̶ ̶i̶t̶'̶s̶ ̶f̶p̶s̶ ̶l̶a̶g̶ ̶w̶i̶t̶h̶ ̶n̶a̶m̶e̶ ̶l̶o̶a̶d̶i̶n̶g̶.̶
# I̶f̶ ̶w̶e̶ ̶l̶o̶a̶d̶ ̶n̶a̶m̶e̶s̶ ̶b̶e̶f̶o̶r̶e̶ ̶g̶a̶m̶e̶ ̶b̶e̶g̶i̶n̶s̶ ̶i̶t̶ ̶w̶i̶l̶l̶ ̶m̶a̶k̶e̶ ̶i̶t̶ ̶e̶a̶s̶i̶e̶r̶?̶ ̶T̶h̶e̶n̶ ̶w̶e̶ ̶w̶o̶n̶'̶t̶ ̶n̶e̶e̶d̶ ̶t̶h̶r̶e̶a̶d̶i̶n̶g̶,̶ ̶a̶n̶d̶ ̶m̶a̶y̶b̶e̶ ̶b̶a̶d̶ ̶h̶a̶r̶d̶w̶a̶r̶e̶ ̶t̶h̶i̶s̶ ̶p̶r̶o̶g̶r̶a̶m̶ ̶r̶u̶n̶n̶i̶n̶g̶ ̶o̶n̶
# FPS lag, is not due to the name loading. It's based on computer preformance. Loading this program in my PC, works perfectly, 60 FPS always.
# loading this program, in codeHS(guessing running in docker) the hardware is not going to be good. minimum 500mb of ram.

os.environ['SDL_AUDIODRIVER'] = 'dsp' # sound driver for CODEHS
pygame.display.set_caption('FORTNITE BY EPIK GAMES') # title of the game, this will be shown in the window
pygame.init() # initialize pygame
pygame.font.init() # initialize font
clock = pygame.time.Clock() # clock for the game
screen = pygame.display.set_mode( (500 , 330) ) # screen size
font = pygame.font.Font(None, 20) # for text

utils.start_up(config)
utils.image_fix()
if(sql.check_if_first_time()):
    sql.setup() # setup if the database does not exist.
# backgrounds init
INTRO_BACKGROUND = pygame.image.load( 'assets/fortnite_menu.png' ) # load
INTRO_BACKGROUND = pygame.transform.scale( INTRO_BACKGROUND, ( 500,330 )) # scale 

MAIN_BACKGROUND = pygame.image.load( 'assets/island.png' ) # load
MAIN_BACKGROUND = pygame.transform.scale( MAIN_BACKGROUND, ( 500,330 )) # scale

# victory royale
VICTORY_ROYALE = pygame.image.load("assets/victory.png") # load
VICTORY_ROYALE = pygame.transform.scale(VICTORY_ROYALE, (360, 72)) # scale

# CLOUDS
CLOUDS = pygame.image.load("assets/clouds.png") # load
CLOUDS = pygame.transform.scale(CLOUDS, (500, 150)) # scale
CLOUDS_x = 0

# the TWO backbone varaibles of our game!!
currently = None
question_hold = ["0","0","0"]

# animation vars, this was never used since the animation was not working.
player_run = 0
draw_player_jumping_var = [False, 0, 0]
player_jumping_question = False
game_start = False
inventory = [] # inventory storage. for weapon management.

# weapon handler vars
current_weapon = None
current_weapon_rect = None


# setup battle bus
BATTLE_BUS = pygame.image.load('assets/battle_bus.png')
BATTLE_BUS = pygame.transform.scale( BATTLE_BUS, (100, 100) )
BATTLE_BUS_rectangle = BATTLE_BUS.get_rect()
BATTLE_BUS_rectangle.x = 0
BATTLE_BUS_rectangle.y = 0

guy_emote_sprite = [ # why did I think this was a good idea? pygame is so bad with this.
    pygame.image.load("assets/guy_emote_1.png"),
    pygame.image.load("assets/guy_emote_2.png")
] # switched to final victory dance. Lol


def victory_dance(screen, x, y):
    for sprite in guy_emote_sprite:
        screen.blit(MAIN_BACKGROUND, (0, 0))
        screen.blit(VICTORY_ROYALE, (0, 0))
        sprite = pygame.transform.scale(sprite, (100, 100))
        screen.blit(sprite, (x, y))
        pygame.display.update()
        time.sleep(0.25) # delay or it not look like emoting.

# setup bad guys
BUILDING_GUY = pygame.image.load("bad-guys/building_guy.png")
GUY_HEALING = pygame.image.load("bad-guys/GUY_HEALING.png")
HEAL_GUY = pygame.image.load("bad-guys/HEAL_GUY.png")
L_CAMPER = pygame.image.load("bad-guys/L_CAMPER.png")
L_CAMPER_2 = pygame.image.load("bad-guys/L_CAMPER_2.png")
PICKAXE_GUY = pygame.image.load("bad-guys/PICKAXE_GUY.png")
REVOLVER_GUY = pygame.image.load("bad-guys/REVOLVER_GUY.png")
SHOTGUN_GUY = pygame.image.load("bad-guys/SHOTGUN_GUY.png")
TEAM_GUY = pygame.image.load("bad-guys/TEAM_GUY.png")
TEAMERS_IN_SOLOS = pygame.image.load("bad-guys/TEAMERS_IN_SOLOS.png")
TREE_GUY = pygame.image.load("bad-guys/TREE_GUY.png")
TRUCK_GUY = pygame.image.load("bad-guys/TRUCK_GUY.png")
# GUY_HEALING = pygame.transform.scale( GUY_HEALING, (100, 100) ) <-- Is there an issue with this? It's rendering weirdly onto the screen, the position is not right?

# map vars
map_100 = pygame.image.load("assets/map/100.png")
map_100 = pygame.transform.scale(map_100, (100, 100))
map_80 = pygame.image.load("assets/map/80.png")
map_80 = pygame.transform.scale(map_80, (100, 100))
map_70 = pygame.image.load("assets/map/70.png")
map_70 = pygame.transform.scale(map_70, (100, 100))
map_60 = pygame.image.load("assets/map/60.png")
map_60 = pygame.transform.scale(map_60, (100, 100))
map_50 = pygame.image.load("assets/map/50.png")
map_50 = pygame.transform.scale(map_50, (100, 100))
map_40 = pygame.image.load("assets/map/40.png")
map_40 = pygame.transform.scale(map_40, (100, 100))
map_20 = pygame.image.load("assets/map/20.png")
map_20 = pygame.transform.scale(map_20, (100, 100))
map_5 = pygame.image.load("assets/map/5.png")
map_5 = pygame.transform.scale(map_5, (100, 100))

# player setup

hard_coded_x_y = ["False", "0", 0, 0]
player_sprite = [
    pygame.image.load("assets/Running_1.png"),
    pygame.image.load("assets/Running_2.png"),
    pygame.image.load("assets/Running_3.png"),
    pygame.image.load("assets/Running_4.png")
]
player_counter = pygame.image.load("assets/player_counter.png")
player_counter = pygame.transform.scale(player_counter, (15, 15))

player_jumping = pygame.image.load("assets/Parachute.png")
player_jumping = pygame.transform.scale(player_jumping,(100,100))
player_jumping_rect = player_jumping.get_rect()
player_jumping_rect.x = 0
player_jumping_rect.y = 0

data.write("loaded all vars", "log.txt")


if(config.get_config()[0]['log-everything']):
    print("Config is now loaded into memory!")
    print("\n\n [CONFIG] \n\n")
    print(f"log_bad_guys_position: {config.get_config()[0]['log-bad-guys-position']}\nlog_everything: {config.get_config()[0]['log-everything']}\nquestion_answer_log_before: {config.get_config()[0]['question-answer-log-before']}\nlog_previous_questions: {config.get_config()[0]['log-previous-questions']}")
    print("\n")

def drop_weapon():
    files = random.choice(os.listdir("guns")) # get random weapon from the guns folder 
    return files # return that weapon

# main game loop

# <<<< What / why are we threading?
# hoping to thread when "players" are thanking the bus driver.
# since code runs in a "straight" line. When we (hopefully), make the thanking bus driver on different thread, so it doesn't "lag" main thread, reducing fps(the bus moves slow).
# there might be different ways to do this, but hopefully this is the right way.

# moved code to game thread. there was a issue with threading and OpenGL, maybe it fixed?
# never was fixed. Pygame and threading do not get along with each other. :(

# <<<< Add comments for what is happening in your game loop
# done

PLAYER_COUNTS = {
    0: "100",
    1: "86",
    2: "74",
    3: "69",
    4: "61",
    5: "49",
    6: "22",
    7: "14",
    8: "3"
}

MAP_STATE = {
    0: map_100,
    1: map_80,
    2: map_70,
    3: map_60,
    4: map_50,
    5: map_40,
    6: map_20,
    7: map_5
}
# below is the code to change map based on the questions answered. 
def get_current_map(questions_answered):
    return MAP_STATE.get(questions_answered, map_100)
# changed to dictionary. much better.

while True:
    if(not multiplayer or not not_connected): # um
        clock.tick(60)
        screen.fill((255, 255, 255)) # small way to make code go faster, clear previous images instead of just drawing over top of it.

        # this is the "Fortnite" loading screen.
        if not GameState.get_state('game_ready'):
            screen.blit( INTRO_BACKGROUND, ( 0, 0 ) )
        if player_jumping_question:
            draw_player_jumping_var[0] = "True"
            player_jumping_question = False

        # all pygame events and "jumping" and "Start Game" logic here.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Goodbye world!")
                packets.disconnect(server_ip, server_port, session_id, username)
                exit(1)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jump = utils.check_jump(event, GameState.get_state('game_ready'), GameState.get_state('bus_starting'), GameState.get_state('jumping'), BATTLE_BUS_rectangle, pygame, config, data, screen, MAIN_BACKGROUND)
                    if jump[0]:
                        GameState.set_state('game_ready', True)
                    if jump[1]:
                        GameState.set_state('bus_starting', True)
                    if jump[2]:
                        GameState.set_state('jumping', True)
                    if jump[3]:
                        player_jumping_question = True
                    if jump[4]:
                        draw_player_jumping_var = jump[4]
        # make the bus move to the end of the screen
        # after it has moved to the end, print END.

        if(GameState.get_state('background')):
            screen.blit(MAIN_BACKGROUND, (0, 0))

        # below is the code to make the bus move to the end of the screen
        # after it has moved to the end, print END.
        if GameState.get_state('game_ready') and GameState.get_state('bus_starting'):
            GameState.set_state('background', True)
            BATTLE_BUS_rectangle.x = BATTLE_BUS_rectangle.x + 1
            CLOUDS_x -= 1
            if CLOUDS_x <= -500:
                CLOUDS_x = 500
            screen.blit(CLOUDS, (CLOUDS_x, 0)) # draw first CLOUDS
            screen.blit(CLOUDS, (CLOUDS_x + 500, 0)) # draw second CLOUDS
            screen.blit(BATTLE_BUS, BATTLE_BUS_rectangle)
            if (BATTLE_BUS_rectangle.x == 500):
                data.write("Bus is off the screen.", "log.txt")
                if(config.get_config()[0]['log-everything']):
                    print("End") # no longer jump.
                if(not GameState.get_state('jumping')):
                    if(config.get_config()[0]['log-everything']):
                        print("Player not even jumping.")
                        print("Ending game early.")
                    exit(0) # xd
                GameState.set_state('player_joined', True)
                GameState.set_state('bus_starting', False)
                game_start = True
                GameState.set_state('get_bad_guy', True) # get bad guy the first time.
        if(hard_coded_x_y[0] == "True" and hard_coded_x_y[1] == "1"):
            player_sprite_rectangle = player_sprite[0].get_rect()
            player_sprite_rectangle.x = hard_coded_x_y[2] + 50
            player_sprite_rectangle.y = hard_coded_x_y[3] + 50
            screen.blit(player_sprite[0], player_sprite_rectangle)
            hard_coded_x_y[1] = "0"
            # wow, this just won't work. Animation just isn't working.
            #  no animations will be included sadly.

        if(hard_coded_x_y[0] == "True" and hard_coded_x_y[1] == "0"):
            player_sprite_rectangle = player_sprite[0].get_rect()
            player_sprite_rectangle.x = hard_coded_x_y[2] + 50
            player_sprite_rectangle.y = hard_coded_x_y[3] + 50
            screen.blit(player_sprite[0], player_sprite_rectangle)
            hard_coded_x_y[1] = "1"

        if(draw_player_jumping_var[0] == "True"):
            x = draw_player_jumping_var[1]
            y = draw_player_jumping_var[2]
            y += 1 # stupid fix. wow
            draw_player_jumping_var[2] = y
            screen.blit(player_jumping, (x, y))
            draw_player_jumping_var[0] = False
            player_jumping_question = True
            if(y == 150):
                player_jumping_question = False
                # animate_running(x, y)
                hard_coded_x_y = ["True", "0", x, y] # value, count, xcoordinate, ycoordinate.

        # below code, handles bad-guys and questions.
        if(currently != None): # there is something in varaible currently.
            if(currently[1].x <= 500 and currently[1].x > currently[2][0]):
                currently[1].x -= 1
                if(config.get_config()[0]['log-bad-guys-position']):
                    print("X: ", currently[1].x, "Y: ", currently[1].y, "[mostly unused]")
                screen.blit(currently[0], currently[1]) # smooth.
            else:
                if(question_hold[0] == "0"): # no question yet
                    screen.blit(currently[0], currently[1])
                    returned_question_hold = question.return_question_hold()
                    for i in range(10):
                        print(" \n ")
                    print(f"==== QUESTION {GameState.get_state('questions_answered') + 1}/{GameState.get_state('total_questions')}! ====")
                    if(not config.get_config()[0]['skip-questions']):
                        question_answer = input(f"{returned_question_hold[0][1]} {returned_question_hold[1][0]} {returned_question_hold[0][2]} \n==================\n Your Answer: ")
                        write_quest = f"| {returned_question_hold[0][1]} {returned_question_hold[1][0]} {returned_question_hold[0][2]} | Your answer: {question_answer}\n"
                        right_or_no = question.check_answer(returned_question_hold[0], returned_question_hold[1], question_answer)
                    else:
                        print("no skill, can't answer any questions? had to use the config to skip questions.")
                        right_or_no = True
                    # below is code to doing stuff if the answer is right or not.
                    if(right_or_no):
                        GameState.set_state('questions_answered', GameState.get_state('questions_answered') + 1)
                        if(GameState.get_state('questions_answered') >= GameState.get_state('total_questions')):
                            print(f"GG!")
                        else:
                            print(f"Good Job! {GameState.get_state('total_questions') - GameState.get_state('questions_answered')} questions remaining!")
                        # drop a weapon.
                        global_weapon = drop_weapon()
                        GameState.set_state('weapon_has', True)
                        # check if the player has answered all the questions, this means there are no one left in the game expect for the player!!!
                        if GameState.get_state('questions_answered') >= GameState.get_state('total_questions'):
                            sql.add_wins(1) # add a win.
                            wins, loses = sql.get_data()
                            winlose = sql.get_ratio()
                            print("\n=== VICTORY ROYALE! ===")
                            print(config.get_messages()[1][random.randint(0, len(config.get_messages()[1]) - 1)])
                            print("┌=======================┐")
                            print(f"| WINS: {wins}          |")
                            print(f"| LOSES: {loses}        |")
                            print(f"| W/L: {winlose}        |")
                            print("└=======================┘")
                            while True:
                                victory_dance(screen, player_sprite_rectangle.x, player_sprite_rectangle.y)
                        else:
                            GameState.set_state('spawn_enemy', True)
                    else:
                        # wrong answer, "crash" the game
                        exit(1)
                else:
                    screen.blit(currently[0], currently[1])
        else:
            if(GameState.get_state('spawn_enemy')):
                currently = AssetManagement.better_bad_guy_generator()
                question_hold = ["0","0","0"]
                GameState.set_state('spawn_enemy', False)
        if(game_start and GameState.get_state('get_bad_guy')):
            currently = AssetManagement.better_bad_guy_generator()
            currently[1].x = 500
            question_hold = ["0","0","0"]
            GameState.set_state('get_bad_guy', False)
        if(GameState.get_state('weapon_has') and global_weapon != None and not GameState.get_state('hand')):
            # print(f"{weapon_has} | {global_weapon}")
            local_weapon = pygame.image.load('guns/' + global_weapon)
            local_weapon_rect = local_weapon.get_rect()
            #  365, 210 <-- in ground
            #  75, 205 <-- Hand
            local_weapon_rect.x = 365
            local_weapon_rect.y = 220 # floating, all images have different res, so this will be a issue.
            # maybe resize other images to the same size? that would be much better and it will fix some image position issues.
            screen.blit(local_weapon, local_weapon_rect)
            pygame.display.update()
            right_or_no = False
            currently = None
            while(local_weapon_rect.x <= 365 and local_weapon_rect.x > player_sprite_rectangle.x):
                local_weapon_rect.x -= 1
                screen.blit(MAIN_BACKGROUND, (0, 0))
                screen.blit(player_sprite[0], player_sprite_rectangle)
                screen.blit(local_weapon, local_weapon_rect)
                current_map = get_current_map(GameState.get_state('questions_answered'))
                screen.blit(current_map, (400, 0))
                players_remain = font.render(PLAYER_COUNTS.get(GameState.get_state('questions_answered'), "100"), True, (255,255,255))
                screen.blit(player_counter, (402, 100))
                screen.blit(players_remain, (420, 100))
                pygame.display.update()
                if(local_weapon_rect.x == player_sprite_rectangle.x):
                    GameState.set_state('hand', True)
        if(GameState.get_state('hand')):
            # If the weapon is at the player's hand.
            currently = AssetManagement.better_bad_guy_generator()
            currently[1].x = 500
            local_weapon = pygame.image.load('guns/' + global_weapon)
            local_weapon_rect = local_weapon.get_rect()
            local_weapon_rect.x = player_sprite_rectangle.x
            local_weapon_rect.y = 207
            screen.blit(local_weapon, local_weapon_rect)
            current_weapon = local_weapon
            current_weapon_rect = local_weapon_rect
            inventory.append(local_weapon)
            inventory.append(local_weapon_rect)
            GameState.set_state('hand', False)
            GameState.set_state('weapon_has', False)
            global_weapon = None
            GameState.set_state('spawn_enemy', True)

        # the player count renderer
        if(GameState.get_state('player_joined')):
            current_map = get_current_map(GameState.get_state('questions_answered'))
            players_remain = font.render(PLAYER_COUNTS.get(GameState.get_state('questions_answered'), "100"), True, (255,255,255))
            screen.blit(players_remain, (420, 100))
            screen.blit(player_counter, (402, 100))
            # again based on the questions answered, the map will change.
            screen.blit(current_map, (400, 0))
        # global renderer for the weapon.
        if current_weapon and current_weapon_rect:
            screen.blit(current_weapon, current_weapon_rect)
        utils.fps_counter(clock, screen, font)
        pygame.display.update() #universal display refresh update()
    if(multiplayer and not_connected):
        print(f"Connecting to {server_ip}:{server_port}")
        if(packets.connect(server_ip, server_port, session_id, username)):
            print(f"Connected to {server_ip}:{server_port}!")
            not_connected = False # connected now