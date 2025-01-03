from typing import Dict, Tuple

# 色の定義
COLORS = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'purple': (128, 0, 128),
    'pink': (255, 192, 203),
    'orange': (255, 165, 0),
    'light_blue': (135, 206, 235),
    'dark_green': (0, 128, 0),
    'black': (0, 0, 0),
}

# 図形の定義
SHAPES = {
    'circle': '○',
    'star': '★',
    'diamond': '◆',
    'hexagon': '⬡',
    'cross': '✚',
    'flower': '✿',
    'triangle': '△',
    'square': '□',
    'gear': '⚙',
    'empty': '?',
}

def get_shape_color(shape_name: str, color_name: str) -> Tuple[str, Tuple[int, int, int]]:
    """図形とその色の組み合わせを取得する"""
    return SHAPES[shape_name], COLORS[color_name]
