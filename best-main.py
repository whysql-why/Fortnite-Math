print("Hello world!")
import os
from libs import data, utils, question, config, AssetManagement
import random, sys, pygame, time

# FPS lag is based on computer performance
# Loading this program in my PC, works perfectly, 60 FPS always
# In codeHS (docker) minimum 500mb of ram needed

os.environ['SDL_AUDIODRIVER'] = 'dsp' # sound driver for CODEHS
pygame.display.set_caption('FORTNITE BY EPIK GAMES')
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 330))
font = pygame.font.Font(None, 20)

utils.start_up(config)

# Load and scale images
def load_image(path, size):
    img = pygame.image.load(path)
    return pygame.transform.scale(img, size)

# backgrounds init
intro_background = load_image('assets/fortnite_menu.png', (500, 330))
main_background = load_image('assets/island.png', (500, 330))
victory_royale = load_image('assets/victory.png', (360, 72))
cloud = load_image('assets/clouds.png', (500, 150))
battle_bus = load_image('assets/battle_bus.png', (100, 100))

# game state controls
game_ready = False
bus_starting = False
player_joined = False
jumping = False
questions_answered = 0
TOTAL_QUESTIONS = 8
currently = None
weapon_has = False
global_weapon = None
Hand = False
spawn_enemy = False
question_hold = ["0","0","0"]
game_start = False

# setup battle bus
battle_bus_rectangle = battle_bus.get_rect()
battle_bus_rectangle.x = 0
battle_bus_rectangle.y = 0

# Cloud position
clouds_x = 0

# Player counts for display
PLAYER_COUNTS = {
    0: "100", 1: "86", 2: "74", 3: "69",
    4: "61", 5: "49", 6: "22", 7: "14", 8: "3"
}

data.write("loaded all vars", "log.txt")

def handle_clouds():
    global clouds_x
    clouds_x -= 1
    if clouds_x <= -500:
        clouds_x = 0
    screen.blit(cloud, (clouds_x, 0))
    screen.blit(cloud, (clouds_x + 500, 0))

def handle_question():
    global questions_answered, spawn_enemy, weapon_has, global_weapon
    returned_question_hold = question.return_question_hold()
    
    print(f"\n==== QUESTION {questions_answered + 1}/{TOTAL_QUESTIONS}! ====")
    if not config.get_config()[0]['skip-questions']:
        question_answer = input(f"{returned_question_hold[0][1]} {returned_question_hold[1][0]} {returned_question_hold[0][2]} \n==================\n Your Answer: ")
        write_quest = f"| {returned_question_hold[0][1]} {returned_question_hold[1][0]} {returned_question_hold[0][2]} | Your answer: {question_answer}\n"
        data.write_question(write_quest)
        right_or_no = question.check_answer(returned_question_hold[0], returned_question_hold[1], question_answer)
    else:
        right_or_no = True
    
    if right_or_no:
        questions_answered += 1
        if questions_answered >= TOTAL_QUESTIONS:
            handle_victory()
        else:
            print(f"Good Job! {TOTAL_QUESTIONS - questions_answered} questions remaining!")
            global_weapon = AssetManagement.drop_weapon()
            weapon_has = True
            spawn_enemy = True

def handle_victory():
    print("\n=== VICTORY ROYALE! ===")
    print(config.get_messages()[1][random.randint(0, len(config.get_messages()[1]) - 1)])
    print("=========================")
    while True:
        victory_dance(screen, player_sprite_rectangle.x, player_sprite_rectangle.y)

# main game loop
while True:
    clock.tick(60)
    screen.fill((255, 255, 255))
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not game_ready and not bus_starting:
                game_ready = True
                bus_starting = True
            elif battle_bus_rectangle.x > 0 and battle_bus_rectangle.x < 500 and not jumping:
                jumping = True
                data.write("player jumped!", "log.txt")

    # Draw current game state
    if game_ready:
        screen.blit(main_background, (0, 0))
        handle_clouds()
        
        if bus_starting:
            screen.blit(battle_bus, battle_bus_rectangle)
            battle_bus_rectangle.x += 1
            
            if battle_bus_rectangle.x == 500:
                data.write("Bus is off the screen.", "log.txt")
                if not jumping:
                    if config.get_config()[0]['log-everything']:
                        print("Player not even jumping.")
                        print("Ending game early.")
                    exit(0)
                player_joined = True
                bus_starting = False
                game_start = True
                get_bad_guy = True
    else:
        screen.blit(intro_background, (0, 0))

    # Handle enemy and questions
    if currently is not None:
        if currently[1].x <= 500 and currently[1].x > currently[2][0]:
            currently[1].x -= 1
            screen.blit(currently[0], currently[1])
        else:
            if question_hold[0] == "0":
                screen.blit(currently[0], currently[1])
                handle_question()
            else:
                screen.blit(currently[0], currently[1])
    elif spawn_enemy or (game_start and get_bad_guy):
        currently = AssetManagement.better_bad_guy_generator()
        if game_start:
            currently[1].x = 500
            game_start = False
        question_hold = ["0","0","0"]
        spawn_enemy = False

    # Draw player count if in game
    if player_joined:
        players_remain = font.render(PLAYER_COUNTS.get(questions_answered, "100"), True, (255,255,255))
        screen.blit(players_remain, (420, 100))

    utils.fps_counter(clock, screen, font)
    pygame.display.update()