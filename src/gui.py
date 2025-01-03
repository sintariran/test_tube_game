import pygame
import sys
from .game import TestTubeGame
from .tube import Shape

class TestTubeGameGUI:
    def __init__(self, width: int = 800, height: int = 600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("試験管パズル")
        
        self.game = TestTubeGame()
        self.tube_width = 60
        self.tube_height = 200
        self.shape_height = self.tube_height // 4
        
        # 背景色
        self.bg_color = (20, 20, 50)
        self.tube_color = (200, 200, 200, 128)
        
    def draw_tube(self, x: int, y: int, tube_index: int):
        # 試験管の描画
        tube_rect = pygame.Rect(x, y, self.tube_width, self.tube_height)
        pygame.draw.rect(self.screen, self.tube_color, tube_rect, 2)
        
        # 試験管の内容物を描画（下から上に）
        shapes = self.game.tubes[tube_index].shapes
        for i, shape in enumerate(reversed(shapes)):
            shape_y = y + self.tube_height - (i + 1) * self.shape_height
            shape_rect = pygame.Rect(x, shape_y, self.tube_width, self.shape_height)
            pygame.draw.rect(self.screen, shape.color, shape_rect)
            
        # 選択された試験管をハイライト
        if self.game.selected_tube == tube_index:
            pygame.draw.rect(self.screen, (255, 255, 0), tube_rect, 3)
            
    def get_tube_index(self, pos: tuple[int, int]) -> int:
        x, y = pos
        tube_spacing = self.width // (self.game.num_tubes + 1)
        for i in range(self.game.num_tubes):
            tube_x = (i + 1) * tube_spacing - self.tube_width // 2
            if tube_x <= x <= tube_x + self.tube_width and \
               self.height // 2 - self.tube_height <= y <= self.height // 2:
                return i
        return -1
        
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    tube_index = self.get_tube_index(event.pos)
                    if tube_index != -1:
                        self.game.select_tube(tube_index)
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.game = TestTubeGame()
                        
            # 画面の描画
            self.screen.fill(self.bg_color)
            
            # 試験管の配置
            tube_spacing = self.width // (self.game.num_tubes + 1)
            for i in range(self.game.num_tubes):
                x = (i + 1) * tube_spacing - self.tube_width // 2
                y = self.height // 2 - self.tube_height
                self.draw_tube(x, y, i)
                
            # ゲームクリア判定
            if self.game.is_game_complete():
                font = pygame.font.Font(None, 74)
                text = font.render("クリア!", True, (255, 255, 0))
                text_rect = text.get_rect(center=(self.width // 2, 100))
                self.screen.blit(text, text_rect)
                
            pygame.display.flip()
            clock.tick(60)

def main():
    game = TestTubeGameGUI()
    game.run()

if __name__ == "__main__":
    main()
