import pygame
import sys
import os
from pygame.locals import *

# 初始化 Pygame
pygame.init()

# 屏幕设置
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("经验升级游戏")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (70, 130, 180)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_GREEN = (144, 238, 144)

# 字体
font_large = pygame.font.SysFont('simhei', 36)
font_medium = pygame.font.SysFont('simhei', 24)
font_small = pygame.font.SysFont('simhei', 18)

# 游戏变量
username = "玩家"
current_exp = 0
current_rank = 0
max_exp_per_rank = 50000000  # 每个段位需要的经验值
ranks = ["经验新手", "经验老手", "经验高手", "经验大师", "经验大神"]
avatar = None
avatar_rect = None
game_complete = False
input_active = False
input_text = username

# 按钮类
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.clicked = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        if self.clicked:
            color = (min(color[0] + 20, 255), min(color[1] + 20, 255), min(color[2] + 20, 255))
        
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        
        text_surf = font_medium.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pos):
                self.clicked = True
                return True
        elif event.type == MOUSEBUTTONUP:
            self.clicked = False
        return False

# 创建按钮
upgrade_button = Button(WIDTH//2 - 100, 400, 200, 50, "升级经验", GREEN, LIGHT_GREEN)
change_name_button = Button(50, 50, 150, 40, "修改名字", LIGHT_BLUE, DARK_BLUE)
change_avatar_button = Button(50, 100, 150, 40, "更换头像", LIGHT_BLUE, DARK_BLUE)
restart_button = Button(WIDTH//2 - 150, 450, 140, 50, "重新开始", GREEN, LIGHT_GREEN)
wait_button = Button(WIDTH//2 + 10, 450, 140, 50, "等待下一部", YELLOW, (255, 255, 100))

# 创建输入框
input_rect = pygame.Rect(220, 50, 200, 40)

# 加载默认头像
def load_default_avatar():
    global avatar, avatar_rect
    avatar = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.circle(avatar, LIGHT_BLUE, (50, 50), 50)
    pygame.draw.circle(avatar, DARK_BLUE, (50, 50), 45, 3)
    text = font_small.render("头像", True, DARK_BLUE)
    text_rect = text.get_rect(center=(50, 50))
    avatar.blit(text, text_rect)
    avatar_rect = avatar.get_rect(center=(WIDTH - 100, 100))

load_default_avatar()

# 加载自定义头像
def load_custom_avatar():
    global avatar, avatar_rect
    try:
        # 在实际应用中，这里应该打开文件对话框选择图片
        # 为了简化，我们创建一个示例头像
        avatar = pygame.Surface((100, 100), pygame.SRCALPHA)
        
        # 随机颜色
        import random
        color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        
        pygame.draw.circle(avatar, color, (50, 50), 50)
        pygame.draw.circle(avatar, DARK_BLUE, (50, 50), 45, 3)
        
        # 绘制简单的笑脸
        pygame.draw.circle(avatar, BLACK, (35, 40), 5)  # 左眼
        pygame.draw.circle(avatar, BLACK, (65, 40), 5)  # 右眼
        pygame.draw.arc(avatar, BLACK, (30, 50, 40, 30), 0, 3.14, 2)  # 微笑
        
        avatar_rect = avatar.get_rect(center=(WIDTH - 100, 100))
        print("头像已更换！")
    except Exception as e:
        print(f"加载头像失败: {e}")

# 绘制经验条
def draw_exp_bar():
    bar_width = 600
    bar_height = 30
    bar_x = (WIDTH - bar_width) // 2
    bar_y = 300
    
    # 绘制背景
    pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height), border_radius=15)
    
    # 计算当前段位内的经验百分比
    exp_in_current_rank = current_exp % max_exp_per_rank
    exp_percentage = exp_in_current_rank / max_exp_per_rank
    
    # 绘制经验条
    fill_width = int(bar_width * exp_percentage)
    if fill_width > 0:
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, fill_width, bar_height), border_radius=15)
    
    # 绘制边框
    pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height), 2, border_radius=15)
    
    # 绘制经验文本
    exp_text = f"{exp_in_current_rank:,} / {max_exp_per_rank:,}"
    text_surf = font_small.render(exp_text, True, BLACK)
    text_rect = text_surf.get_rect(center=(WIDTH//2, bar_y + bar_height//2))
    screen.blit(text_surf, text_rect)

# 绘制输入框
def draw_input_box():
    color = DARK_BLUE if input_active else LIGHT_BLUE
    pygame.draw.rect(screen, color, input_rect, border_radius=5)
    pygame.draw.rect(screen, BLACK, input_rect, 2, border_radius=5)
    
    text_surf = font_small.render(input_text, True, BLACK)
    screen.blit(text_surf, (input_rect.x + 5, input_rect.y + 10))

# 绘制游戏完成界面
def draw_game_complete():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    congrats_text = font_large.render("恭喜你成为经验大神！", True, YELLOW)
    screen.blit(congrats_text, (WIDTH//2 - congrats_text.get_width()//2, 200))
    
    choice_text = font_medium.render("请选择下一步操作：", True, WHITE)
    screen.blit(choice_text, (WIDTH//2 - choice_text.get_width()//2, 350))
    
    restart_button.draw(screen)
    wait_button.draw(screen)

# 重置游戏
def reset_game():
    global current_exp, current_rank, game_complete
    current_exp = 0
    current_rank = 0
    game_complete = False

# 主游戏循环
clock = pygame.time.Clock()
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            
        # 处理输入框事件
        if event.type == MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                input_active = True
            else:
                input_active = False
                
        if event.type == KEYDOWN and input_active:
            if event.key == K_RETURN:
                if input_text.strip():  # 确保用户名不为空
                    username = input_text
                    print(f"用户名已修改为: {username}")
                input_active = False
            elif event.key == K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                # 限制用户名长度
                if len(input_text) < 15:
                    input_text += event.unicode
            
        # 处理按钮点击
        if upgrade_button.is_clicked(mouse_pos, event) and not game_complete:
            current_exp += 1
            # 检查是否升级段位
            if current_exp >= (current_rank + 1) * max_exp_per_rank:
                current_rank += 1
                # 检查是否达到最高段位
                if current_rank >= len(ranks) - 1:
                    current_rank = len(ranks) - 1
                    # 检查是否满经验
                    if current_exp >= len(ranks) * max_exp_per_rank:
                        game_complete = True
                        print("游戏完成！达到最高段位和满经验！")
                        
        if change_name_button.is_clicked(mouse_pos, event):
            input_active = True
            print("点击了修改名字按钮")
            
        if change_avatar_button.is_clicked(mouse_pos, event):
            load_custom_avatar()
            print("点击了更换头像按钮")
            
        if restart_button.is_clicked(mouse_pos, event) and game_complete:
            reset_game()
            print("游戏已重新开始")
            
        if wait_button.is_clicked(mouse_pos, event) and game_complete:
            print("等待下一部功能 - 游戏暂停在此状态")
    
    # 更新按钮悬停状态
    upgrade_button.check_hover(mouse_pos)
    change_name_button.check_hover(mouse_pos)
    change_avatar_button.check_hover(mouse_pos)
    restart_button.check_hover(mouse_pos)
    wait_button.check_hover(mouse_pos)
    
    # 绘制界面
    screen.fill(WHITE)
    
    # 绘制用户信息
    name_text = font_medium.render(f"用户名: {username}", True, BLACK)
    screen.blit(name_text, (220, 60))
    
    # 绘制输入框
    draw_input_box()
    
    # 绘制段位信息
    rank_text = font_large.render(f"当前段位: {ranks[current_rank]}", True, DARK_BLUE)
    screen.blit(rank_text, (WIDTH//2 - rank_text.get_width()//2, 150))
    
    # 绘制总经验
    total_exp_text = font_medium.render(f"总经验值: {current_exp:,}", True, BLACK)
    screen.blit(total_exp_text, (WIDTH//2 - total_exp_text.get_width()//2, 200))
    
    # 绘制经验条
    draw_exp_bar()
    
    # 绘制头像
    if avatar:
        screen.blit(avatar, avatar_rect)
    
    # 绘制按钮
    upgrade_button.draw(screen)
    change_name_button.draw(screen)
    change_avatar_button.draw(screen)
    
    # 绘制输入提示
    if input_active:
        hint_text = font_small.render("输入新名字后按回车确认", True, DARK_BLUE)
        screen.blit(hint_text, (input_rect.x, input_rect.y - 25))
    
    # 如果游戏完成，显示完成界面
    if game_complete:
        draw_game_complete()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()