from typing import List, Optional, Tuple
from .tube import Tube, Shape
import random
from .shapes import SHAPES, COLORS

class TestTubeGame:
    def __init__(self, num_tubes: int = 12, tube_capacity: int = 4):
        self.num_tubes = num_tubes
        self.tube_capacity = tube_capacity
        self.tubes: List[Tube] = []
        self.selected_tube: Optional[int] = None
        self.initialize_game()

    def initialize_game(self):
        # 試験管を作成
        self.tubes = [Tube(self.tube_capacity) for _ in range(self.num_tubes)]
        
        # 図形の定義（記号は省略）
        CROSS = Shape('', (128, 0, 128))  # 十字（赤紫）
        GEAR = Shape('', (255, 255, 0))   # 歯車（黄）
        DIAMOND = Shape('', (0, 191, 255))  # ダイヤ（水色）
        HEX = Shape('', (0, 255, 0))      # 六角形（緑）
        CIRCLE_RED = Shape('', (255, 0, 0))  # 丸（赤）
        CIRCLE_PURPLE = Shape('', (147, 112, 219))  # 丸（紫）
        FLOWER = Shape('', (255, 182, 193))  # 花（ピンク）
        TRIANGLE = Shape('', (255, 165, 0))  # 三角（オレンジ）
        STAR = Shape('', (135, 206, 235))  # 星（水色）
        SQUARE = Shape('', (0, 128, 0))    # 四角（緑）
        EMPTY = Shape('', (0, 0, 0))       # 空（黒）

        # 初期配置を設定（上から下の順番）
        initial_state = [
            [CROSS, GEAR, DIAMOND, CROSS],  # 1：上から 十字(赤紫)→歯車(黄)→ダイヤ(水色)→十字(赤紫)
            [EMPTY, HEX, CROSS, CIRCLE_RED],  # 2：空→六角(緑)→十字(赤紫)→丸(赤)
            [CIRCLE_PURPLE, HEX, FLOWER, TRIANGLE],  # 3：紫丸→六角(緑)→花(ピンク)→三角(オレンジ)
            [EMPTY, GEAR, DIAMOND, EMPTY],  # 4：空→歯車(黄)→ダイヤ(水色)→空
            [EMPTY, STAR, HEX, FLOWER],  # 5：空→星(水色)→六角(緑)→花(ピンク)
            [SQUARE, CIRCLE_RED, EMPTY, EMPTY],  # 6：四角(緑)→丸(赤)→空→空
            [GEAR, FLOWER, HEX, SQUARE],  # 7：歯車(黄)→花(ピンク)→六角(緑)→四角(緑)
            [CIRCLE_PURPLE, STAR, DIAMOND, EMPTY],  # 8：紫丸→星(水色)→ダイヤ(水色)→空
            [CIRCLE_PURPLE, STAR, CIRCLE_RED, EMPTY],  # 9：紫丸→星(水色)→丸(赤)→空
            [DIAMOND, FLOWER, CROSS, CIRCLE_RED],  # 10：ダイヤ(水色)→花(ピンク)→十字(赤紫)→丸(赤)
            [TRIANGLE, TRIANGLE, TRIANGLE],  # 11：三角(オレンジ)×3
            []  # 12：空
        ]

        # 試験管に配置
        for tube_index, shapes in enumerate(initial_state):
            for shape in shapes:
                self.tubes[tube_index].add(shape)

    def select_tube(self, tube_index: int) -> bool:
        if tube_index < 0 or tube_index >= len(self.tubes):
            return False

        if self.selected_tube is None:
            if not self.tubes[tube_index].is_empty():
                self.selected_tube = tube_index
                return True
        else:
            return self.move_shape(self.selected_tube, tube_index)
        return False

    def move_shape(self, from_index: int, to_index: int) -> bool:
        if from_index == to_index:
            self.selected_tube = None
            return False

        from_tube = self.tubes[from_index]
        to_tube = self.tubes[to_index]

        if from_tube.is_empty() or to_tube.is_full():
            self.selected_tube = None
            return False

        shape = from_tube.pop()
        if shape and to_tube.add(shape):
            self.selected_tube = None
            return True
        
        if shape:
            from_tube.add(shape)
        self.selected_tube = None
        return False

    def is_game_complete(self) -> bool:
        return all(tube.is_complete() or tube.is_empty() for tube in self.tubes)

    def get_tube_contents(self) -> List[List[Shape]]:
        return [tube.shapes for tube in self.tubes]
