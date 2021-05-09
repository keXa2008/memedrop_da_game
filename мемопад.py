import pygame
import random


# Настройка игрового окна
def init(caption):
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()
    return screen, clock


def draw_text(screen, text, font_size, text_color, pos):
    basic_font = pygame.font.SysFont('Arial', font_size)
    text = basic_font.render(text, True, text_color)
    screen.blit(text, pos)


def create_player(color, size, speed, x, y):
    player = Block(color, size, speed)
    player.rect.x = x
    player.rect.y = y
    return player


WIN_WIDTH = 800
WIN_HEIGHT = 600
FPS = 30
# цвета    R    G    B
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

screen, clock = init('Мемопад')


class Block(pygame.sprite.Sprite):
    image_lst = ['0.png','1.png','2.png','3.png','4.png','5.png','6.png','7.png','8.png','9.png','10.png','11.png']

    def __init__(self, speed=5):
        super().__init__()
        img_file = random.choice(self.image_lst)
        self.image = pygame.image.load(img_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIN_WIDTH)
        self.rect.y = random.randrange(WIN_HEIGHT // 2)
        self.speed = speed
        self.image = pygame.transform.rotate(self.image, 180)
    def update(self):
        # Подвинуть блок "навстречу" автомобилю
        self.rect.y += self.speed
        if self.rect.y > WIN_WIDTH:
            self.rect.y = 0
            self.rect.x = random.randrange(WIN_WIDTH)


def change_state(event, current_state):
    if current_state == 0:  # начать игру
        current_state = 1
    elif current_state == 1:  # идет игра, нажали PAUSE
        current_state = 2
    elif current_state == 2:  # сняли с паузы
        current_state = 1
    return current_state


class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=5):
        super().__init__()
        self.image = pygame.image.load('Car.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed


# Создаем группы спрайтов:
block_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

# Создаем блоки - препятствия и добавляем их в группы:
for i in range(5):
    block = Block(random.randint(3, 6))
    block_list.add(block)
    all_sprites_list.add(block)

start_image = pygame.image.load("pingas.jpg").convert_alpha()
p1 = pygame.image.load('Car.png').convert()
p2 = pygame.image.load('Car_2.png').convert()
background_sound=pygame.mixer.Sound("pingas.mp3")
crash_sound=pygame.mixer.Sound("Ohhh Meme.mp3")
# Создаем спрайт игрока
player = Car(WIN_WIDTH // 2, WIN_HEIGHT-100)

# Добавляем игрока в группу all_sprites_list:
all_sprites_list.add(player)
text_pos = (WIN_WIDTH // 3, WIN_HEIGHT // 2)
current_state = 0
background_sound.play(-1)
while True:
    # обработка событий мыши  клавиатуры:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                current_state = change_state(event, current_state)
            if event.key == pygame.K_1:
                if current_state == 0:
                    player.image = pygame.image.load('Car.png').convert_alpha()
            if event.key == pygame.K_2:
                if current_state == 0:
                    player.image = pygame.image.load('Car_2.png').convert_alpha()
            if event.key == pygame.K_r:
                if current_state == 3:
                    current_state = 1
    screen.fill(GRAY)

    if current_state == 0:
        screen.blit(start_image, (-200, 0))
        draw_text(screen, 'Нажми 1 для выбора грустного', 36, BLUE, (WIN_WIDTH // 3, WIN_HEIGHT // 7))
        screen.blit(p1, (WIN_WIDTH//5, WIN_HEIGHT//7.5))
        draw_text(screen, 'Нажми 2 для выбора амогуса', 36, BLUE, (WIN_WIDTH // 3, WIN_HEIGHT // 3))
        screen.blit(p2, (WIN_WIDTH//5, WIN_HEIGHT//3))
        draw_text(screen, 'Нажми Пробел чтобы начать', 36, BLUE, text_pos)

    if current_state == 1:
        pos = pygame.mouse.get_pos()
        player.rect.x = pos[0] - player.rect.width // 2
        block_list.update()
        all_sprites_list.draw(screen)

    if current_state == 2:
        all_sprites_list.draw(screen)
        draw_text(screen, 'PAUSE', 36, RED, text_pos)

    if current_state == 3:
        draw_text(screen, 'LOL!!!!1!!', 36, RED, text_pos)
        crash_sound.play(0)


    if pygame.sprite.spritecollideany(player, block_list):
        current_state = 3

    # конец прорисовки окна
    pygame.display.update()
    clock.tick(FPS)