

def victory_dance(screen, x, y, guy_emote_sprite, main_background, victory_royale, pygame, time):
    for sprite in guy_emote_sprite:
        screen.blit(main_background, (0, 0))
        screen.blit(victory_royale, (0, 0))
        sprite = pygame.transform.scale(sprite, (100, 100))
        screen.blit(sprite, (x, y))
        pygame.display.update()
        time.sleep(0.25) # delay or it not look like emoting.


def check_jump(event, game_ready, bus_starting, jumping, battle_bus_rectangle, pygame, config, data, screen, main_background):
    collection = [False, False, False, False, [False, 0, 0]]
    if not game_ready and not bus_starting:
        if config.get_config()[0]['log-everything']:
            print("Loading ALL assets.")
        data.write("All assets loaded!", "log.txt")
        collection[0] = True  # game_ready
        collection[1] = True  # bus_starting
        screen.blit(main_background, (0, 0))
        pygame.display.update()
    if battle_bus_rectangle.x > 0 and battle_bus_rectangle.x < 500 and not jumping:
        data.write("player jumped!", "log.txt")
        if config.get_config()[0]['log-everything']:
            print("\n[debug]: detected player wanting to jump off the battle bus!\n")
        collection[2] = True  # jumping
        collection[3] = True  # player_jumping_question
        collection[4] = ["True", battle_bus_rectangle.x, battle_bus_rectangle.y]  # draw_player_jumping_var
    return collection

# [0] = game_ready
# [1] = bus_starting
# [2] = jumping
# [3] = player_jumping_question
# [4] = draw_player_jumping_var


# the code to render the fps counter based on the get_fps() method.
def fps_counter(clock, screen, font):
    num_fps = int(clock.get_fps())
    if(num_fps < 20):
        fps = font.render(f"{num_fps} FPS", True, (254,5,5))
    if(num_fps > 50):
        fps = font.render(f"{num_fps} FPS", True, (49,253,3))
    if(num_fps < 50 and num_fps > 20):
        fps = font.render(f"{num_fps} FPS", True, (255,222,89))
    screen.blit(fps, (30, 30))

def start_up(config):
    if(config.get_config()[0]['log-everything']): # check if the log-everything is enabled in the config 
        print("\nTIP: If you see black screen, \nRestart the game!")
        print("Your Graphics Screen might not be loaded properly.")
        print("Or You just enabled graphics screen as the program was running,")
        print("In that case, please restart the game!")


# temp files docs:
# questions.txt <-- stores previous questions, only use is in config.yml
# add more when more files are needed.


def write_question(string):
    with open('temp/questions.txt', 'w') as file:
        file.write(string)
    if(config.get_config()[0]['log-everything']):
        print("Question is written to file.")
        print(f"Log Previous Questions is set to: {config.get_config()[0]['log-previous-questions']}")