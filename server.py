from functools import reduce
from flask import Flask, json, render_template, redirect, request, jsonify
from flask.helpers import flash, url_for
import requests

import sudoku_solver

app = Flask(__name__)
app.secret_key = 's4ad56r7qw4af5awer456asfc2sa7dtas5'


@app.route('/')
def home():
    return(redirect(url_for('sudoku')))


@app.route('/sudoku')
def sudoku():
    return render_template('sudoku-solver.html')


@app.route('/solve_sudoku', methods=['POST'])
def solve_sudoku():
    

    json = request.json
    
    sudoku = json['sudoku']
    max_solutions = json['max_solutions']

    if not sudoku_solver.sudoku_validator(sudoku,count_blank_spaces=False):
        return jsonify({'error': 'The sudoku you provided is not a valid one, please provide a valid sudoku'})

    over_hundred = False

    if max_solutions > 100:
        over_hundred = True
        max_solutions = 100
    

    solutions = []
    size = 3
    solver = sudoku_solver.sudoku_solver((size, size), sudoku)

    for s in solver:
        # Here we create a copy of the list object given by solver
        lst = [[x for x in n] for n in s.copy()]  
        solutions.append(lst)

        if len(solutions) == max_solutions:
            solver.close()
        
    if over_hundred:
        return jsonify({
            'warning': 'The number of solutions cannot be more than 100', 
            'solutions': solutions, 'num_solutions': len(solutions)})

    return jsonify({'solutions': solutions, 'num_solutions': len(solutions)})


@app.route('/api')
def sudoku_api_doc():
    return render_template('API.html')


@app.route('/api_example')
def api_example():

    sudoku_example = [[0, 0, 0, 0, 3, 0, 0, 0, 0],
    [1, 2, 0, 7, 4, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 4],
    [0, 0, 5, 0, 0, 0, 7, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 3, 0, 0, 6, 1, 0, 2, 8],
    [0, 0, 0, 9, 0, 0, 0, 0, 2],
    [4, 6, 0, 0, 0, 0, 8, 3, 0],
    [0, 0, 7, 0, 0, 0, 0, 0, 9]]

    data = {'sudoku': sudoku_example, 'max_solutions': 10}
    response = requests.post(url='https://sudoku-solver-with-python.herokuapp.com/solve_sudoku', json=data)
    return response.json()

# web: gunicorn server:app
if __name__ == '__main__':
    app.run(debug=True)
