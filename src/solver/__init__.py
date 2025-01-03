from .state import TubeState
from .solver import TubeSolver

def solve_puzzle(tubes) -> list:
    """パズルを解く
    
    Args:
        tubes: 試験管の初期状態のリスト。各試験管は色のRGBタプルのリスト。
        
    Returns:
        移動手順のリスト。各要素は (from_idx, to_idx) のタプル。
        解けない場合は空のリスト。
    """
    initial_state = TubeState(tubes)
    solver = TubeSolver()
    solution = solver.solve(initial_state)
    return solution if solution else [] 