from typing import List, Tuple, Dict, Set, Optional
from queue import PriorityQueue
from collections import defaultdict
from dataclasses import dataclass, field
from .state import TubeState
import random

# 色の定義
EMPTY = -1
UNKNOWN = -2

@dataclass(order=True)
class PrioritizedState:
    priority: int
    moves: int = field(compare=False)
    state: TubeState = field(compare=False)

class TubeSolver:
    def __init__(self):
        self.seen_states: Set[str] = set()
        self.eval_cache = {}
        
    def solve(self, initial_state: TubeState, max_iterations: int = 200000) -> Optional[List[Tuple[int, int]]]:
        """パズルを解くメインロジック"""
        print("パズルを解く:")
        print("探索を開始します...")
        
        visited = {}  # 状態のハッシュ値をキーとし、その状態に到達した最小の深さを値とする
        queue = [(initial_state, [], 0)]
        best_score = float('-inf')
        best_state = None
        best_moves = None
        iterations = 0
        states_explored = 0
        no_improvement_count = 0

        while queue and iterations < max_iterations:
            # スコアが高い状態を優先的に探索
            if iterations % 100 == 0:  # 定期的にソート
                queue.sort(key=lambda x: self._evaluate(x[0], x[2]), reverse=True)
            current_state, moves, depth = queue.pop(0)  # 先頭から取り出す
            states_explored += 1
            
            if iterations % 1000 == 0:
                print(f"\n探索回数: {iterations}")
                print(f"探索済み状態数: {states_explored}")
                current_score = self._evaluate(current_state, depth)
                print(f"現在のスコア: {current_score}")
                print(f"最高スコア: {best_score}")
                print(f"現在の手数: {depth}")
                if best_moves:
                    for i, (from_tube, to_tube, color) in enumerate(best_moves, 1):
                        self._print_state(
                            state=current_state,
                            move_count=i,
                            from_tube=from_tube,
                            to_tube=to_tube,
                            moved_color=self._get_color_name(color),
                            score=best_score
                        )
            
            state_hash = current_state.get_hash()
            if state_hash in visited and visited[state_hash] <= depth:
                continue
            visited[state_hash] = depth
            
            score = self._evaluate(current_state, depth)
            if score > best_score:
                best_score = score
                best_state = current_state
                best_moves = moves
                no_improvement_count = 0
                print(f"\n新しい最高スコア: {best_score}")
                if best_moves:
                    for i, (from_tube, to_tube, color) in enumerate(best_moves, 1):
                        self._print_state(
                            state=current_state,
                            move_count=i,
                            from_tube=from_tube,
                            to_tube=to_tube,
                            moved_color=self._get_color_name(color),
                            score=best_score
                        )
            else:
                no_improvement_count += 1
                
            # 一定回数改善が見られない場合、探索をリセット
            if no_improvement_count > 2000:  # より長く待つように調整
                print("\n探索をリセットします...")
                queue = [(best_state, best_moves, len(best_moves))]
                visited.clear()
                no_improvement_count = 0
                continue

            if current_state.is_solved():
                print("\n解が見つかりました!")
                if moves:
                    for i, (from_tube, to_tube, color) in enumerate(moves, 1):
                        self._print_state(
                            state=current_state,
                            move_count=i,
                            from_tube=from_tube,
                            to_tube=to_tube,
                            moved_color=self._get_color_name(color),
                            score=score
                        )
                return True, moves
                
            # 有効な移動手順を生成
            next_moves = self._get_valid_moves(current_state)
            
            # 移動手順をスコアで評価してソート
            scored_moves = []
            for from_tube, to_tube in next_moves:
                new_state = current_state.copy()
                color = new_state.tubes[from_tube][-1]
                new_state.move(from_tube, to_tube)
                move_score = self._evaluate(new_state, depth + 1)
                scored_moves.append((move_score, from_tube, to_tube))
            
            # スコアの高い順に並べ替え
            scored_moves.sort(reverse=True)
            
            # 上位の手順のみを探索（深さに応じて探索範囲を調整）
            max_moves = max(8, 25 - depth)  # 探索範囲を広げる
            for move_score, from_tube, to_tube in scored_moves[:max_moves]:
                new_state = current_state.copy()
                color = new_state.tubes[from_tube][-1]
                new_state.move(from_tube, to_tube)
                new_moves = moves + [(from_tube, to_tube, color)]
                
                # 同じ状態でも、より少ない手数で到達できる場合は探索を続ける
                new_hash = new_state.get_hash()
                if new_hash not in visited or visited[new_hash] > depth + 1:
                    queue.append((new_state, new_moves, depth + 1))
                
            iterations += 1

        print("\n解が見つかりませんでした。")
        print(f"探索回数: {iterations}")
        print(f"最高スコア: {best_score}")
        if best_moves:
            for i, (from_tube, to_tube, color) in enumerate(best_moves, 1):
                self._print_state(
                    state=best_state,
                    move_count=i,
                    from_tube=from_tube,
                    to_tube=to_tube,
                    moved_color=self._get_color_name(color),
                    score=best_score
                )
        return False, best_moves
        
    def _evaluate(self, state: TubeState, depth: int) -> int:
        """状態を評価する関数"""
        score = 0
        
        # 完成したチューブのボーナスを大きく
        completed_tubes = 0
        for tube in state.tubes:
            if len(tube) == 4 and all(c == tube[0] for c in tube):
                completed_tubes += 1
                score += 20000  # 完成ボーナスを2倍に
        
        # 空のチューブのボーナス
        empty_tubes = sum(1 for tube in state.tubes if not tube)
        score += empty_tubes * 300  # 空チューブのボーナスを増加
        
        # 連続した同じ色のボーナス
        for tube in state.tubes:
            if not tube:
                continue
            consecutive = 1
            for i in range(len(tube)-1):
                if tube[i] == tube[i+1]:
                    consecutive += 1
                    score += consecutive * 200  # 連続ボーナスを2倍に
            
            # チューブが完成に近い場合の追加ボーナス
            if len(tube) >= 2 and all(c == tube[0] for c in tube):
                score += len(tube) * 500
        
        # 深さペナルティを調整（より小さく）
        score -= depth * 3
        
        # 同じ色が異なるチューブに分散しているペナルティ（より重く）
        color_locations = {}
        for i, tube in enumerate(state.tubes):
            for color in tube:
                if color not in color_locations:
                    color_locations[color] = set()
                color_locations[color].add(i)
        
        for locations in color_locations.values():
            if len(locations) > 1:  # 同じ色が複数のチューブに存在する場合
                score -= len(locations) * 200  # ペナルティを2倍に
        
        return score
        
    def _generate_moves(self, state: TubeState) -> List[TubeState]:
        """可能な手を全て生成"""
        moves = []
        empty_tubes = []
        
        # 空の試験管を先に見つける
        for i, tube in enumerate(state.tubes):
            if not tube:
                empty_tubes.append(i)
        
        for i, from_tube in enumerate(state.tubes):
            # 移動元の試験管が空なら飛ばす
            if not from_tube:
                continue
                
            # 移動元の試験管が完成していれば飛ばす
            if len(from_tube) == 4 and all(c == from_tube[0] for c in from_tube):
                continue
                
            # 移動元の一番上の色を取得
            top_color = from_tube[0]  # インデックス0が一番上
            
            # まず、同じ色がある試験管への移動を試みる
            found_same_color = False
            for j, to_tube in enumerate(state.tubes):
                if i == j or len(to_tube) >= 4:
                    continue
                    
                if to_tube and to_tube[0] == top_color:  # インデックス0と比較
                    found_same_color = True
                    new_state = state.copy()
                    if new_state.move(i, j):
                        moves.append(new_state)
                        
            # 同じ色が見つからなかった場合のみ、空の試験管への移動を考慮
            if not found_same_color and empty_tubes:
                # 空の試験管が複数ある場合は1つだけ使用
                new_state = state.copy()
                if new_state.move(i, empty_tubes[0]):
                    moves.append(new_state)
        
        return moves
        
    def _is_redundant_move(self, old_state: TubeState, new_state: TubeState) -> bool:
        """無意味な移動かどうかをチェック"""
        last_move = new_state.moves[-1]
        from_idx, to_idx = last_move
        
        # 空の試験管を経由する無意味な移動をチェック
        if len(old_state.tubes[to_idx]) == 0:
            # 他の空の試験管があれば冗長
            empty_tubes = sum(1 for tube in old_state.tubes if not tube)
            if empty_tubes > 1:
                return True
        
        # 同じ色を持つ試験管間の無意味な移動をチェック
        if len(new_state.moves) >= 2:
            prev_from, prev_to = new_state.moves[-2]
            if prev_to == from_idx and prev_from == to_idx:
                return True
        
        return False 
        
    def _get_color_name(self, color):
        if color is None:
            return "不明"
        
        color_names = {
            (255, 0, 0): "赤",            # RED
            (255, 255, 0): "黄",          # YELLOW
            (0, 191, 255): "水色",        # LIGHT_BLUE
            (128, 0, 128): "赤紫",        # PURPLE
            (148, 0, 211): "紫",          # VIOLET
            (255, 165, 0): "オレンジ",    # ORANGE
            (0, 255, 0): "緑",            # GREEN
            (255, 182, 193): "ピンク",    # PINK
            (0, 0, 255): "青",            # BLUE
            (0, 100, 0): "深緑",          # DARK_GREEN
            (255, 218, 185): "肌色",      # SKIN
            (128, 128, 128): "不明"       # UNKNOWN
        }
        return color_names.get(color, "不明")

    def _print_state(self, state, move_count=None, from_tube=None, to_tube=None, moved_color=None, score=None):
        if move_count is not None:
            print(f"\n{move_count:2d}手目: ", end="")
            if from_tube is not None and to_tube is not None and moved_color is not None:
                print(f"試験管{from_tube+1:2d} → 試験管{to_tube+1:2d} ({moved_color}を移動)")
        
        print("\n現在の状態:")
        if score is not None:
            print(f"スコア: {score}")
            print(f"手数: {move_count if move_count is not None else 0}")
        
        print("\n試験管の状態:")
        for i, tube in enumerate(state.tubes):
            colors = [self._get_color_name(color) for color in tube]
            print(f"試験管{i+1:2d}: {colors}")

    def _is_unknown_color(self, color):
        """色が不明かどうかを判定する"""
        return color == (128, 128, 128)  # グレーを不明な色として扱う

    def _is_valid_initial_state(self, state: TubeState) -> bool:
        """初期状態が妥当かどうかをチェック"""
        # 各色の出現回数を数える
        color_counts = {}
        for tube in state.tubes:
            for color in tube:
                color_counts[color] = color_counts.get(color, 0) + 1
        
        # 各色が4つずつあるかチェック
        return all(count == 4 for count in color_counts.values()) 

    def _get_valid_moves(self, state):
        """有効な移動手順を生成する"""
        valid_moves = []
        empty_tubes = []
        
        # 空の試験管を先に見つける
        for i, tube in enumerate(state.tubes):
            if not tube:
                empty_tubes.append(i)
        
        # 完成したチューブは移動元から除外
        for from_tube in range(len(state.tubes)):
            if not state.tubes[from_tube]:  # 空の試験管からは移動できない
                continue
            if len(state.tubes[from_tube]) == 4 and all(c == state.tubes[from_tube][0] for c in state.tubes[from_tube]):
                continue
            
            from_color = state.tubes[from_tube][-1]
            
            # 同じ色が連続している場合は、その色をまとめて移動することを優先
            consecutive_count = 1
            for i in range(len(state.tubes[from_tube])-2, -1, -1):
                if state.tubes[from_tube][i] == from_color:
                    consecutive_count += 1
                else:
                    break
            
            # まず、同じ色がある試験管への移動を試みる
            found_same_color = False
            for to_tube in range(len(state.tubes)):
                if from_tube == to_tube or len(state.tubes[to_tube]) >= 4:
                    continue
                
                if state.tubes[to_tube] and state.tubes[to_tube][-1] == from_color:
                    if len(state.tubes[to_tube]) + consecutive_count <= 4:
                        valid_moves.insert(0, (from_tube, to_tube))  # 優先度の高い移動を先頭に
                        found_same_color = True
            
            # 同じ色が見つからなかった場合のみ、空の試験管への移動を考慮
            if not found_same_color and empty_tubes:
                # 空の試験管が複数ある場合は1つだけ使用
                valid_moves.append((from_tube, empty_tubes[0]))
        
        return valid_moves

    def _print_move(self, move, move_number):
        from_tube, to_tube = move
        color = self._get_color_name(self.state.tubes[from_tube][-1])
        print(f"\n{move_number:2d}手目: 試験管{from_tube + 1:2d} → 試験管{to_tube + 1:2d} ({color}を移動)")
        print("\n現在の状態:")
        self._print_state() 