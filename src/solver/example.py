from . import solve_puzzle
from .state import TubeState
from .solver import TubeSolver

# 色の定義
RED = (255, 0, 0)  # 赤
YELLOW = (255, 255, 0)  # 黄
LIGHT_BLUE = (0, 191, 255)  # 水色
PURPLE = (128, 0, 128)  # 赤紫
VIOLET = (148, 0, 211)  # 紫
ORANGE = (255, 165, 0)  # オレンジ
GREEN = (0, 255, 0)  # 緑
PINK = (255, 182, 193)  # ピンク
BLUE = (0, 0, 255)  # 青
DARK_GREEN = (0, 100, 0)  # 深緑
SKIN = (255, 218, 185)  # 肌色
UNKNOWN = (128, 128, 128)  # 未知の色（?マーク）

# 初期状態の定義（下から上の順）
initial_tubes = [
    # 上段の試験管（左から）
    [DARK_GREEN, GREEN, PURPLE, YELLOW],  # 1: 深緑/緑/赤紫/黄
    [GREEN, PINK, DARK_GREEN, SKIN],  # 2: 緑/ピンク/深緑/肌色
    [PURPLE, RED, LIGHT_BLUE, GREEN],  # 3: 赤紫/赤/水色/緑
    [RED, PINK, SKIN, YELLOW],  # 4: 赤/ピンク/肌色/黄
    [VIOLET, SKIN, ORANGE, BLUE],  # 5: 紫/肌色/オレンジ/青
    [YELLOW, BLUE, SKIN, GREEN],  # 6: 黄/青/肌色/緑
    
    # 下段の試験管（左から）
    [VIOLET, PINK, BLUE, PINK],  # 7: 紫/ピンク/青/ピンク
    [YELLOW, VIOLET, ORANGE, PURPLE],  # 8: 黄/紫/オレンジ/赤紫
    [BLUE, LIGHT_BLUE, ORANGE, LIGHT_BLUE],  # 9: 青/水色/オレンジ/水色
    [RED, DARK_GREEN, PURPLE, VIOLET],  # 10: 赤/深緑/赤紫/紫
    [RED, DARK_GREEN, ORANGE, LIGHT_BLUE],  # 11: 赤/深緑/オレンジ/水色
    [],  # 12: 空
    []   # 13: 空
]

def main():
    print("パズルを解く:")
    # パズルを解く
    solution = solve_puzzle(initial_tubes)
    
    # 解答を表示
    if not solution:
        print("解答が見つかりませんでした。")

if __name__ == "__main__":
    main() 