from typing import List, Tuple, Optional
from copy import deepcopy

class TubeState:
    def __init__(self, tubes: List[List[Tuple[int, int, int]]], moves: List[Tuple[int, int]] = None):
        self.tubes = tubes  # 各試験管の状態（色のリスト）
        self.moves = moves or []  # 移動履歴 [(from_idx, to_idx), ...]
        
    def copy(self) -> 'TubeState':
        return TubeState(deepcopy(self.tubes), deepcopy(self.moves))
        
    def get_top_color(self, tube_idx: int) -> Optional[Tuple[int, int, int]]:
        """指定した試験管の一番上の色を取得"""
        if not self.tubes[tube_idx]:
            return None
        return self.tubes[tube_idx][-1]  # 末尾（一番上）の色を返す
        
    def can_move(self, from_idx: int, to_idx: int) -> bool:
        """移動可能かどうかを判定"""
        # 同じ試験管への移動は不可
        if from_idx == to_idx:
            return False
            
        # 移動元が空なら不可
        if not self.tubes[from_idx]:
            return False
            
        # 移動先が満杯なら不可
        if len(self.tubes[to_idx]) >= 4:
            return False
            
        # 移動先が空なら可能
        if not self.tubes[to_idx]:
            return True
            
        # 移動先の一番上が不明な色なら不可
        if self.tubes[to_idx][-1] == (128, 128, 128):
            return False
            
        # 色が同じ場合のみ可能
        return self.get_top_color(from_idx) == self.get_top_color(to_idx)
        
    def move(self, from_idx: int, to_idx: int) -> bool:
        """液体を移動。成功したらTrueを返す"""
        if not self.can_move(from_idx, to_idx):
            return False
            
        color = self.tubes[from_idx].pop()  # 一番上（末尾）の色を取得
        self.tubes[to_idx].append(color)  # 一番上（末尾）に追加
        self.moves.append((from_idx, to_idx))
        return True
        
    def is_solved(self) -> bool:
        """パズルが解けているかどうかを判定"""
        for tube in self.tubes:
            # 空の試験管はOK
            if not tube:
                continue
                
            # 4つ揃っていない、または色が混ざっている場合はNG
            if len(tube) != 4 or any(c != tube[0] for c in tube[1:]):
                return False
                
        return True
        
    def get_hash(self) -> str:
        """状態のハッシュ値を取得"""
        # 試験管の状態をソートしてタプルに変換
        sorted_tubes = sorted(tuple(tube) for tube in self.tubes)
        return str(sorted_tubes)
        
    def __str__(self) -> str:
        return f"Tubes: {self.tubes}, Moves: {self.moves}"

    def get_state_at_move(self, move_number: int) -> List[List[Tuple[int, int, int]]]:
        """指定された手数までの移動を適用した状態を返す"""
        if move_number <= 0:
            return self.tubes

        # 初期状態をコピー
        current_tubes = deepcopy(self.tubes)
        
        # 指定された手数まで移動を適用
        for i in range(min(move_number, len(self.moves))):
            from_idx, to_idx = self.moves[i]
            if current_tubes[from_idx]:  # 移動元が空でない場合
                color = current_tubes[from_idx].pop()
                current_tubes[to_idx].append(color)
                
        return current_tubes 