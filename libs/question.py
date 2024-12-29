
# question.py
# created on 2024-12-20
# This file is for generating questions and checking answers!
# written by: Epik Games group


import random
from libs import config

# get a math question.
def get_math_question():
    p = random.randint(1, 4)
    pfirst = random.randint(0, 500)
    sfirst = random.randint(0, 500)
    return [p, pfirst, sfirst]

# check the answer to the math question.
def check_answer(question_hold, local_var, answer_checker):
    # print(f"Question Hold: {question_hold} | local var: {local_var} | answer checker: {answer_checker}")
    if(local_var[0] == '+'):
        if(int(question_hold[1]) + int(question_hold[2]) == int(answer_checker)):
            print("RIGHT ANSWER!")
            return True
    if(local_var[0] == '-'):
        if(int(question_hold[1]) - int(question_hold[2]) == int(answer_checker)):
            print("RIGHT ANSWER!")
            return True
    if(local_var[0] == 'x'):
        if(int(question_hold[1]) * int(question_hold[2]) == int(answer_checker)):
            print("RIGHT ANSWER!")
            return True
    if(local_var[0] == '÷'):
        if(int(question_hold[1]) / int(question_hold[2]) == int(answer_checker)):
            print("RIGHT ANSWER!")
            return True
    print("=== WRONG ANSWER ===")
    print("\n\n")
    print(config.get_messages()[0][random.randint(0, len(config.get_messages()[0]) - 1)])
    print("\n\n=============")
    return False

def return_question_hold():
    question_hold = get_math_question() # I AM NOT MAKING IT IN THE SCREEN. WE DO NOT HAVE TIME TO BUILD ALL THAT. ONLY TERMINAL QUESTIONS AND ANSWERS.
    # get_math_question(): [random digit from 1-4, another_digit, digit]. putting [0] as "0" is a state change variable. That is how it breaks, if you manually configure it as 0.
    local_var = []
    multi = config.get_config()[1]['only-multiplication']
    divis = config.get_config()[1]['only-division']
    addit = config.get_config()[1]['only-addition']
    subt = config.get_config()[1]['only-subtraction']
    if(multi and not divis and not addit and not subt):
        local_var.append("x")
    if(divis and not multi and not addit and not subt):
        local_var.append("÷")
    if(addit and not multi and not divis and not subt):
        local_var.append("+")
    if(subt and not multi and not divis and not addit):
        local_var.append("-")

    if(question_hold[0] == 1):
        if(config.get_config()[0]['log-everything']):
            print("[+]")
        local_var.append("+")
    if(question_hold[0] == 2):
        if(config.get_config()[0]['log-everything']):
            print("[-]")
        local_var.append("-")
    if(question_hold[0] == 3):
        if(config.get_config()[0]['log-everything']):
            print("[x]")
        local_var.append("x")
    if(question_hold[0] == 4):
        if(config.get_config()[0]['log-everything']):
            print("[÷]")
        local_var.append("÷")
    return question_hold, local_var