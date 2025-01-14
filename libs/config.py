import yaml, os

config_load = None

# 0 = log-bad-guys-position
# 1 = log-everything
# 2 = question-answer-log-before
# 3 = log-previous-questions
# 4 = skip-questions
# 5 = only-multiplication
# 6 = only-division
# 7 = only-addiction
# 8 = only-subtraction

# yaml for better messages management.
# start loading config.

with open('config.yml') as file:
    config_load = yaml.safe_load(file)
with open('messages.yml') as file:
    messages = yaml.safe_load(file)

def get_messages():
    death_messages = messages['death_messages']
    victory_messages = messages['victory_messages']
    return death_messages, victory_messages
def reload_config():
    with open('config.yml') as file:
        config_load = yaml.safe_load(file)
        return config_load
def get_config():
    config = config_load['debug']
    config_question = config_load['questions']
    return config, config_question
    # get_config()[1]['only-multiplication'] # example
    # get_config()[0]['log-bad-guys-position']
