from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS

from sudoku.main import Board
from sudoku.solvers.z3_solver import Z3Solver


bp = Blueprint('/', __name__)


@bp.route('/sudoku/mock', methods=['GET'])
def mock_sudoku():
    res = { 'answer': list(range(0, 81)), 'solved': True }
    return jsonify(res)


@bp.route('/sudoku/solve', methods=['POST'])
def solve_sudoku():
    """
    Solve sudoku api

    """

    # Allow only localhost access
    origin = request.origin
    if origin.replace('http://', '').replace('https://', '').split(':')[0] != 'localhost':
        return

    payload = request.json
    cell_values = payload.get('cellValues')
    block_size = payload.get('blockSize')
    board_size = block_size ** 2

    if (not cell_values) or (not board_size):
        return jsonify({'answer': [], 'solved': False})

    b = Board(cell_values, board_size)
    valid = b.is_valid

    if not valid:
        return jsonify({'answer': [], 'solved': False})

    solver = Z3Solver(b)
    solver.solve()
    solved = b.is_solved

    if not solved:
        b.show()
        return jsonify({'answer': [], 'solved': False})

    answer = b.get_cell_values()
    return jsonify({'answer': answer, 'solved': True})
