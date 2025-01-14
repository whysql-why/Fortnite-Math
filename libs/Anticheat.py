from libs import config

def enable():
    if(config.get_config()[0]['skip-questions'] or config.get_config()[0]['log-bad-guys-position'] or config.get_config()[0]['log-everything'] or config.get_config()[0]['question-answer-log-before'] or config.get_config()[0]['log-previous-questions']):
        print("=========================================")
        print("Anticheat detected player to be cheating.")
        print("=========================================")
        exit(0)
    if(config.get_config()[1]['only-multiplication'] or config.get_config()[1]['only-division'] or config.get_config()[1]['only-addition'] or config.get_config()[1]['only-subtraction']):
        print("=========================================")
        print("Anticheat detected player to be cheating.")
        print("=========================================")
        exit(0)
    print("====================================================")
    print("Anticheat detected player to be NOT using any cheats")
    print("====================================================")