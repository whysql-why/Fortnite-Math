# storage, i guess this is a good way to do this and it will reduce the main file size!!
state = {
    'background': False,
    'game_ready': False,
    'bus_starting': False,
    'dead': None,
    'fortnite_menu': None,
    'parachute': None,
    'player_joined': False,
    'get_bad_guy': False,
    'currently': None,
    'weapon_has': False,
    'global_weapon': None,
    'hand': False,
    'spawn_enemy': False,
    'question_hold': ["0","0","0"],
    'questions_answered': 0,
    'total_questions': 8,
    'jumping': False
}

def reset_game_state():
    state.update({
        'background': False,
        'game_ready': False,
        'bus_starting': False,
        'dead': None,
        'fortnite_menu': None,
        'parachute': None,
        'player_joined': False,
        'get_bad_guy': False,
        'currently': None,
        'weapon_has': False,
        'global_weapon': None,
        'hand': False,
        'spawn_enemy': False,
        'question_hold': ["0","0","0"],
        'questions_answered': 0,
        'jumping': False
    })

def get_state(key):
    return state.get(key)

def set_state(key, value):
    state[key] = value