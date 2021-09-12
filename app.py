from flask import Flask, render_template, request
import os 

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def index(): 
    if request.method == "POST":
        proposition = request.form.get("proposition")
        output = checking_correctness(proposition)
        correctness = output['correctness']
        error = output['error']
        if correctness: 
            return render_template("page.html", proposition = proposition, correctness="correct")
        else: 
            return render_template("page.html", proposition = proposition, correctness="not correct", error = error)
    else:
        return render_template("page.html")

def checking_correctness(proposition):
    #check edge cases when proposition is missing. 
    if len(proposition) == 0:
        return {'correctness': False, 'error': "Proposition is empty"}

    # num of ( and ) must match
    parsed_prop = proposition.replace('(', '( ').replace(')', ' )').split(' ')
    idx = 0
    while idx < len(parsed_prop):
        if parsed_prop[idx] == '':
            parsed_prop.pop(idx)
        else:
            idx += 1
    paran_list = []
    for chr in parsed_prop:
        if chr == '(':
            paran_list.append(chr)
        elif chr == ')':
            if len(paran_list) == 0:
                return {'correctness': False, 'error': "Missing '('."}
            else: 
                paran_list.pop(0)
    if len(paran_list) != 0:
        return {'correctness': False, 'error': "Missing ')'."}
        
    # make sure the left side of ( is an operator, and right side of ) is either nothing or an operator. 
    parsed_prop = proposition.replace('(', '( ').replace(')', ' )').split(' ')
    idx = 0
    while idx < len(parsed_prop):
        if parsed_prop[idx] == '':
            parsed_prop.pop(idx)
        else:
            idx += 1
    print(parsed_prop)
    for idx in range(0, len(parsed_prop)):
        if parsed_prop[idx] == '(' and idx != 0 and parsed_prop[idx - 1] not in ['and', 'or', 'not', '(']:
            return {'correctness': False, 'error': "Left side of '(' cannot be an variable."}
        if parsed_prop[idx] == ')' and idx != len(parsed_prop) - 1 and parsed_prop[idx + 1] not in ['and', 'or', 'not']:
            return {'correctness': False, 'error': "The right side of ')' cannot be a variable."}

    #check operators
    parsed_prop = proposition.replace('(', ' ').replace(')', ' ').split(' ')
    for operator in parsed_prop:
        if len(operator) <= 1:
            continue
        elif operator not in ['and', 'or', 'not']:
            return {'correctness': False, 'error': "Unknown operator \"" + operator + "\"."}

    #check and/or operator
    parsed_prop = proposition.replace('(', '( ').replace(')', ' )').replace('and', ' * ').replace('or', ' * ').replace('  ', ' ').split(' ')
    idx = 0
    while idx < len(parsed_prop):
        if parsed_prop[idx] == '':
            parsed_prop.pop(idx)
        else:
            idx += 1
    for idx in range(0, len(parsed_prop)):
        if parsed_prop[idx] == '*':
            if idx == 0:
                return {'correctness': False, 'error': "'and'/'or' operator missing left operand."}
            elif parsed_prop[idx - 1] == '(':
                return {'correctness': False, 'error': "Cannot attach 'and'/'or' operator to '('."}
            elif idx == len(parsed_prop) - 1:
                return {'correctness': False, 'error': "'and'/'or' operator missing right operand."}
    
    #check not operator
    parsed_prop = proposition.replace('(', '( ').replace(')', ' )').replace('not', '*').replace('  ', ' ').split(' ')
    idx = 0
    while idx < len(parsed_prop):
        if parsed_prop[idx] == '':
            parsed_prop.pop(idx)
        else:
            idx += 1
    for idx in range(0, len(parsed_prop)):
        if parsed_prop[idx] == '*':
            if idx == len(parsed_prop) - 1:
                return {'correctness': False, 'error': "Not operator missing operand."}
            elif parsed_prop[idx + 1] in ['and', 'or']:
                return {'correctness': False, 'error': "Not operator cannot have 'and'/'or' as an operand."}
            elif idx > 0 and parsed_prop[idx - 1] != '(' and len(parsed_prop[idx - 1]) == 1:
                return {'correctness': False, 'error': "Not operator cannot have an variable on its left side."}

    return {'correctness': True, 'error': 'Great Job.'}
