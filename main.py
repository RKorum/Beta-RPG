import pygame, random, shutil, os

'''RPG

    Russian/Русский
- Игра на языке программирования python, сделана с помощью библиотеки pygame, нужно убивать врагов и получать опыт, повышая уровень и получая скиллпоинты
- Есть меню прокачки и меню со статистикой персонажа
- Враги появляются в одной случайно-заданной точке, есть список с возможными координатами появления
- Каждый уровень даёт по 3 скиллпоинта, скиллпоинты можно потратить на повышения здоровья или атаки

- Враги могут атаковать игрока, что конечно-же свойственно для любой игры жанра РПГ
- Для того чтобы восстановить здоровье нужно найти бонус красного цвета, но враги так-же могут забрать бонус вместо вас
- Если враг возьмёт бонус, то он станет сильнее (если он взял жёлтый бонус - он будет атаковать сильнее, если он взял красный - его здоровье увеличится)

- класс Player - сам игрок
- класс MagicBall - выстрелы игрока
- класс Enemy - враг
- класс Bonus - бонусы
- класс Helper - хендлер
- класс Run - запуск игры
(как только проект в релиз войдёт создам exe файл для запуска, и можно будет запустить код даже не имея пайтона на компьютере)

    English/Английский
- The game is in the python programming language, made using the pygame library, you need to kill enemies and gain experience by leveling up and getting skill points
- There is a leveling menu and a menu with character stats
- Enemies appear at one randomly-set point, there is a list with possible coordinates of appearance
- Each level gives 3 skillpoints, skillpoints can be spent on health upgrades or attacks

- Enemies can attack the player, which of course is typical for any RPG game
- In order to restore health, you need to find a red bonus, but enemies can also take the bonus instead of you
- If the enemy takes the bonus, he will become stronger (if he took the yellow bonus, he will attack harder, if he took the red one, his health will increase)

- Player class - the player himself
- MagicBall class - Player's shots
- Enemy class - the enemy
- Bonus class - bonuses
- Helper - handler class
- Run class - starting the game
(as soon as the project is released, I will create an exe file to run, and you can run the code even without having Python on your computer)
'''


class Player:
    def __init__(self, x, y, width, height, image_path, current_hp, speed, current_damage, max_hp, current_level):
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.image = pygame.image.load(image_path)
        self.speed = speed
        self.current_hp = current_hp
        self.current_damage = current_damage
        self.max_hp = max_hp
        self.current_level = current_level

        self.default_xp_for_next_level = 10
        self.current_need_xp = self.default_xp_for_next_level * self.current_level
        self.current_xp = 0
        self.skillpoint = 0
        self.added_power = 0
        self.added_hp = 0

        self.attack_cd = 0
        self.default_cd_after_attack = 200

        self.direction = 'down'

        self.attacks = []
        self.bonuses = []

        self.animation_timer = 200
        self.animation_frame = 0

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.static_images = {
            'down': pygame.transform.smoothscale(pygame.image.load('Image/Player/static/playerstatic_down.png'),
                                                 (100, 100)),
            'up': pygame.transform.smoothscale(pygame.image.load('Image/Player/static/playerstatic_up.png'),
                                               (100, 100)),
            'right': pygame.transform.smoothscale(pygame.image.load('Image/Player/static/playerstatic_right.png'),
                                                  (100, 100)),
            'left': pygame.transform.smoothscale(pygame.image.load('Image/Player/static/playerstatic_left.png'),
                                                 (100, 100)),
        }
        self.attack_images = {
            'down': pygame.transform.smoothscale(pygame.image.load('Image/Player/animations/attack/player_attack_down.png'), (100, 100)),
            'up': pygame.transform.smoothscale(pygame.image.load('Image/Player/animations/attack/player_attack_up.png'), (100, 100)),
            'right': pygame.transform.smoothscale(pygame.image.load('Image/Player/animations/attack/player_attack_right.png'), (100, 100)),
            'left': pygame.transform.smoothscale(pygame.image.load('Image/Player/animations/attack/player_attack_left.png'), (100, 100))
        }
        self.dynamic_animations = {
            'walk_right': (
                pygame.transform.smoothscale(pygame.image.load('Image/Player/animations/walk_right/player_walk_1.png'), (100, 100)),
                pygame.transform.smoothscale(pygame.image.load('Image/Player/animations/walk_right/player_walk_2.png'), (100, 100)),
            ),
            'walk_left': (
                pygame.transform.smoothscale(pygame.image.load('Image/Player/animations/walk_left/player_walk_1.png'), (100, 100)),
                pygame.transform.smoothscale(pygame.image.load('Image/Player/animations/walk_left/player_walk_2.png'), (100, 100)),
            ),
            'walk_up': (
                pygame.transform.smoothscale(pygame.image.load('Image/Player/animations/walk_up/player_walk_1.png'), (100, 100)),
                pygame.transform.smoothscale(pygame.image.load('Image/Player/animations/walk_up/player_walk_2.png'), (100, 100)),
            ),
            'walk_down': (
                pygame.transform.smoothscale(pygame.image.load('Image/Player/animations/walk_down/player_walk_1.png'), (100, 100)),
                pygame.transform.smoothscale(pygame.image.load('Image/Player/animations/walk_down/player_walk_2.png'), (100, 100)),
            )
        }

        pygame.mixer.init()
        self.current_music = 'Summoning - Nightshade Forests.mp3'
        pygame.mixer.music.load(f'files/music/{self.current_music}')
        pygame.mixer.music.set_volume(100)
        pygame.mixer.music.play(-1)
        self.pause = False

    def change_animation(self, movement):
        if self.attack_cd <= 0:
            current_time = pygame.time.get_ticks()
            if current_time - self.animation_timer > 500:
                self.animation_timer = current_time
                self.animation_frame = 0 if self.animation_frame == 1 else 1

            if movement == 'right':
                self.image = self.dynamic_animations['walk_right'][self.animation_frame]
                self.direction = 'right'

            if movement == 'left':
                self.image = self.dynamic_animations['walk_left'][self.animation_frame]
                self.direction = 'left'

            if movement == 'up':
                self.image = self.dynamic_animations['walk_up'][self.animation_frame]
                self.direction = 'up'

            if movement == 'down':
                self.image = self.dynamic_animations['walk_down'][self.animation_frame]
                self.direction = 'down'

            if movement == 'static':
                self.image = self.static_images[self.direction]
        else:
            self.attack_cd -= 1
            self.image = self.attack_images[self.direction]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def save_game(self):
        files = f'x:{self.x}\n y:{self.y}\n current_hp:{self.current_hp}\n current_damage:{self.current_damage}\n max_hp:{self.max_hp}\n current_level:{self.current_level}\n current_xp:{self.current_xp}\n current_need_xp:{self.current_need_xp}\n skillpoint:{self.skillpoint}\n added_power:{self.added_power}\n added_health:{self.added_hp}\n current_song:{self.current_music}\n pause:{self.pause}'.encode('utf-8').hex()
        with open('files/txt/save_01.txt', 'w') as f:
            f.write(files)

    def load_files(self):
        with open('files/txt/save_01.txt', 'r') as f:
            files = f.readlines()
        if files:
            try:
                tempfiles = ''
                for i in files:
                    tempfiles += f'{bytes.fromhex(i).decode('utf-8')}\n'
                files = tempfiles.split('\n')
                self.x = float(files[0].split('x:')[1])
                self.y = float(files[1].split('y:')[1])

                self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

                self.current_hp = int(files[2].split('current_hp:')[1])
                self.current_damage = int(files[3].split('current_damage:')[1])
                self.max_hp = int(files[4].split('max_hp:')[1])
                self.current_level = int(files[5].split('current_level:')[1])
                self.current_xp = int(files[6].split('current_xp:')[1])
                self.current_need_xp = int(files[7].split('current_need_xp:')[1])
                self.skillpoint = int(files[8].split('skillpoint:')[1])
                self.added_power = int(files[9].split('added_power:')[1])
                self.added_hp = int(files[10].split('added_health:')[1])

                self.current_music = files[11].split('current_song:')[1]
                pygame.mixer.music.load(f'files/music/{self.current_music}')
                pygame.mixer.music.set_volume(100)
                pygame.mixer.music.play(-1)

                self.pause = bool(files[12].split('pause:')[1])
                if self.pause:
                    pygame.mixer.music.pause()
            except Exception:
                pass

    def attack(self):
        if self.attack_cd <= 0:
            self.image = self.attack_images[self.direction]
            self.attacks.append(
                MagicBall(x=self.x + 3, y=self.y + 45, damage=self.current_damage, speed=1, direction=self.direction))
            self.attack_cd = self.default_cd_after_attack

    def level_up(self):
        self.current_level += 1
        self.skillpoint += 3
        self.current_xp -= self.current_need_xp
        self.current_need_xp = self.default_xp_for_next_level * self.current_level

    def add_bonus(self):
        self.bonuses.append(Bonus(x=random.randint(100, 1100), y=random.randint(100, 600)))


class MagicBall:
    def __init__(self, x, y, damage, speed, direction) -> None:
        self.x = x
        self.y = y
        self.width = 'temp'
        self.height = 'temp'
        self.damage = damage
        self.speed = speed
        self.direction = direction
        self.rect = pygame.Rect(self.x, self.y, 10 if self.direction == 'up' or self.direction == 'down' else 40,
                                40 if self.direction == 'up' or self.direction == 'down' else 10)

    def attack_update(self):
        if self.direction == 'up':
            self.y -= self.speed
            self.width = 10
            self.height = 40
        elif self.direction == 'down':
            self.y += self.speed
            self.width = 10
            self.height = 40
        elif self.direction == 'right':
            self.x += self.speed
            self.width = 40
            self.height = 10
        elif self.direction == 'left':
            self.x -= self.speed
            self.width = 40
            self.height = 10
        self.rect = pygame.Rect(self.x, self.y, 10 if self.direction == 'up' or self.direction == 'down' else 40,
                                40 if self.direction == 'up' or self.direction == 'down' else 10)


class Enemy:
    def __init__(self, hp, damage):
        self.x = random.choice([1100, 600, 10])
        self.y = random.choice([0, 350 if self.x >= 600 else 600, 650])

        self.hp = hp
        self.damage = damage

        self.width, self.height = 90, 90

        self.animations = {
            'left': (
                pygame.transform.smoothscale(pygame.image.load('Image/Enemy/animations/left/enemy_run_left_2.png'), (self.width, self.height)),
                pygame.transform.smoothscale(pygame.image.load('Image/Enemy/animations/left/enemy_run_left.png'), (self.width, self.height))
            ),
            'right': (
                pygame.transform.smoothscale(pygame.image.load('Image/Enemy/animations/right/enemy_run_right.png'), (self.width, self.height)),
                pygame.transform.smoothscale(pygame.image.load('Image/Enemy/animations/right/enemy_run_right_2.png'), (self.width, self.height))
            ),
            'static': (
                pygame.transform.smoothscale(pygame.image.load('Image/Enemy/static/enemy_static_2.png'), (self.width, self.height)),
                pygame.transform.smoothscale(pygame.image.load('Image/Enemy/static/enemy_static.png'), (self.width, self.height))
            )
        }

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.image = self.animations['left'][0]
        self.animation_timer = 200
        self.phase_of_animation = 0
        self.speed = 0.3

        self.attack_timer = 0
        self.wait_attack = False
        self.enemy_static = False

    def change_animation(self, movement):
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > 500:
            self.phase_of_animation = 0 if self.phase_of_animation == 1 else 1
            self.animation_timer = current_time

        if movement == 'left':
            self.image = self.animations['left'][self.phase_of_animation]
        if movement == 'right':
            self.image = self.animations['right'][self.phase_of_animation]
        if movement == 'static':
            self.image = self.animations['static'][self.phase_of_animation]

        self.rect = pygame.Rect(self.x, self.y, 10 if movement == 'up' or movement == 'down' else 40,
                                40 if movement == 'up' or movement == 'down' else 10)

    def attack(self, obj):
        if not self.wait_attack:
            obj.current_hp -= self.damage
            self.wait_attack = True
            self.attack_timer = 200

        elif self.attack_timer <= 0:
            self.wait_attack = False

        else:
            self.attack_timer -= 1


class Bonus:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.radius = 20

        self.types_of_bonus = ['health', 'xp']
        self.type = random.choice(self.types_of_bonus)

        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)

    def user_use_bonus(self, user: Player):
        if self.type == 'health':
            if user.current_hp != user.max_hp:
                user.current_hp += random.randint(1, user.max_hp - user.current_hp)
        elif self.type == 'xp':
            user.current_xp += random.randint(1, user.current_xp)

    def enemy_use_bonus(self, enemy: Enemy):
        if self.type == 'health':
            enemy.hp += random.randint(5, enemy.hp)
        elif self.type == 'xp':
            enemy.damage += random.randint(5, enemy.damage + 5)
        if enemy.speed > 0.1:
            enemy.speed -= 0.1

        if enemy.height < 100 and enemy.height < 100:
            # увеличиваем его в размерах
            enemy.width += 20
            enemy.height += 20
            # текстурки синхронизируем
            enemy.animations = {
                'left': (
                    pygame.transform.smoothscale(pygame.image.load('Image/Enemy/animations/left/enemy_run_left_2.png'), (enemy.width, enemy.height)),
                    pygame.transform.smoothscale(pygame.image.load('Image/Enemy/animations/left/enemy_run_left.png'), (enemy.width, enemy.height))
                ),
                'right': (
                    pygame.transform.smoothscale(pygame.image.load('Image/Enemy/animations/right/enemy_run_right.png'), (enemy.width, enemy.height)),
                    pygame.transform.smoothscale(pygame.image.load('Image/Enemy/animations/right/enemy_run_right_2.png'), (enemy.width, enemy.height))
                ),
                'static': (
                    pygame.transform.smoothscale(pygame.image.load('Image/Enemy/static/enemy_static_2.png'), (enemy.width, enemy.height)),
                    pygame.transform.smoothscale(pygame.image.load('Image/Enemy/static/enemy_static.png'), (enemy.width, enemy.height))
                )
            }


class Helper:
    def __init__(self):
        self.enemies = []

    @staticmethod
    def build():
        pygame.display.set_caption('RPG')
        icon = pygame.image.load('Image/icon/icon.png')
        pygame.display.set_icon(icon)
        width = 1200
        height = 700
        screen = pygame.display.set_mode((width, height))

        return width, height, screen

    def spawn_enemy(self, damage):
        if len(self.enemies) < 1:
            self.enemies.append(Enemy(hp=100, damage=damage))


class Runner:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.main_menu = True
        self.new_game_confirm = False
        self.menu_opened = False
        self.menu_with_skillpoints_opened = False
        self.updates_check = False

        self.settings = False
        self.music_choicer = False
        self.wait_music = False

        self.youhavesp = pygame.font.Font(None, 25).render(f'У вас есть доступные очки навыков, вы можете открыть меню прокачки, нажав клавишу "G"', True, (90, 90, 90))
        self.bonus_ticks = random.randint(5000, 12000)

    def run(self):
        helper = Helper()
        width, height, screen = helper.build()

        player = Player(x=200, y=100,
                        width=32, height=35,
                        image_path='Image/Player/static/playerstatic_down.png',
                        current_hp=100, speed=0.2, current_damage=5, max_hp=100, current_level=1)

        player.load_files()

        while True:
            # база
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    player.save_game()
                    pygame.quit()
                if self.wait_music and event.type == pygame.DROPFILE:
                    print(event.file)
                    shutil.copy(event.file, 'files/music/')
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g and not self.main_menu:
                        self.menu_opened = not self.menu_opened

            # самое интересное
            if not self.menu_opened and not self.main_menu:
                keys = pygame.key.get_pressed()

                if player.attack_cd <= 0:
                    if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.y > -4:
                        player.y -= player.speed if not keys[pygame.K_LCTRL] else player.speed * 1.5
                        player.change_animation(movement='up')
                    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.y < height - 111:
                        player.y += player.speed if not keys[pygame.K_LCTRL] else player.speed * 1.5
                        player.change_animation(movement='down')
                    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x > -35:
                        player.x -= player.speed if not keys[pygame.K_LCTRL] else player.speed * 1.5
                        player.change_animation(movement='left')
                    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x < width - 80:
                        player.x += player.speed if not keys[pygame.K_LCTRL] else player.speed * 1.5
                        player.change_animation(movement='right')
                    if not keys[pygame.K_w] and not keys[pygame.K_UP] and not keys[pygame.K_s] and not keys[pygame.K_DOWN] and not keys[pygame.K_a] and not keys[pygame.K_LEFT] and not keys[pygame.K_d] and not keys[pygame.K_RIGHT]:
                        player.change_animation(movement='static')

                    # делаем возможность атаковать нажатием левой кнопки мыши
                    if pygame.mouse.get_pressed()[0]:
                        player.attack()

                player.change_animation('')

                # врагов добавляем
                helper.spawn_enemy(damage=5 if player.current_level > 7 else 1)

                for enemy in helper.enemies:
                    if player.bonuses:
                        for bonus in player.bonuses:
                            pygame.draw.circle(screen, (255, 0, 0) if bonus.type == 'health' else (255, 255, 0), bonus.rect.center, bonus.radius)
                            if abs(player.x - bonus.x) <= 50 and abs(player.y - bonus.y) <= 90:
                                bonus.user_use_bonus(player)
                                player.bonuses.remove(bonus)
                            if abs(enemy.x - bonus.x) <= 50 and abs(enemy.y - bonus.y) <= 90:
                                bonus.enemy_use_bonus(enemy)
                                player.bonuses.remove(bonus)

                            # механика движения врага, он ещё может твои бонусы забирать теперь
                            if abs(enemy.rect.centerx - player.rect.centerx) < abs(enemy.rect.centerx - bonus.rect.centerx) and abs(enemy.rect.centery - player.rect.centery) < abs(enemy.rect.centery - bonus.rect.centery):
                                if enemy.x < player.x + 50:
                                    enemy.change_animation('right')
                                    enemy.x += enemy.speed
                                    enemy.enemy_static = False
                                if enemy.y < player.y:
                                    enemy.y += enemy.speed
                                    enemy.enemy_static = False
                                if enemy.x > player.x - 60:
                                    enemy.change_animation('left')
                                    enemy.x -= enemy.speed
                                    enemy.enemy_static = False
                                if enemy.y > player.y:
                                    enemy.y -= enemy.speed
                                    enemy.enemy_static = False

                            else:
                                if enemy.x < bonus.x:
                                    enemy.change_animation('right')
                                    enemy.x += enemy.speed / 2
                                    enemy.enemy_static = False
                                if enemy.x > bonus.x:
                                    enemy.change_animation('left')
                                    enemy.x -= enemy.speed / 2
                                    enemy.enemy_static = False
                                if enemy.y < bonus.y:
                                    enemy.y += enemy.speed / 2
                                    enemy.enemy_static = False
                                if enemy.y > bonus.y:
                                    enemy.y -= enemy.speed / 2
                                    enemy.enemy_static = False
                    else:
                        # механика движения врага, если нет бонусов
                        if enemy.x < player.x + 50:
                            enemy.change_animation('right')
                            enemy.x += enemy.speed
                            enemy.enemy_static = False
                        if enemy.y < player.y:
                            enemy.y += enemy.speed
                            enemy.enemy_static = False
                        if enemy.x > player.x - 60:
                            enemy.change_animation('left')
                            enemy.x -= enemy.speed
                            enemy.enemy_static = False
                        if enemy.y > player.y:
                            enemy.y -= enemy.speed
                            enemy.enemy_static = False

                    if abs(enemy.x - player.x) <= 70 and abs(enemy.y - player.y) <= 15:
                        enemy.enemy_static = True
                        enemy.change_animation('static')

                    if enemy.enemy_static:
                        enemy.attack(player)

                    for magicball in player.attacks:
                        magicball.attack_update()
                        if 0 > magicball.x + magicball.width or magicball.x > width or magicball.y + magicball.height < 0 or magicball.y > height:
                            player.attacks.remove(magicball)

                        if abs(magicball.x - enemy.x) < enemy.width and abs(magicball.y - enemy.y) < enemy.height:
                            enemy.hp -= magicball.damage
                            player.attacks.remove(magicball)

                        pygame.draw.rect(screen, (255, 0, 0), (magicball.x, magicball.y, magicball.width, magicball.height))
                    screen.blit(enemy.image, (enemy.x, enemy.y))

                    if int(enemy.hp) <= 0:
                        helper.enemies.remove(enemy)
                        player.current_xp += 1

                if int(player.current_hp) <= 0:
                    player.current_xp = 0
                    player.current_hp = player.max_hp
                    player.x, player.y = 200, 100

                if len(player.bonuses) > 1:
                    player.bonuses.pop(0)
                if self.bonus_ticks <= 0:
                    player.add_bonus()
                    self.bonus_ticks = random.randint(5000, 6000)
                else:
                    self.bonus_ticks -= 1

                # создаём текст на экране
                text_hp = pygame.font.Font(None, 25).render(f'Здоровье: {player.current_hp}/{player.max_hp}', True, (255, 0, 0))
                screen.blit(text_hp, (0, height - 25))

                if player.skillpoint > 0:
                    screen.blit(self.youhavesp, (0, height - 55))

                screen.blit(player.image, (player.x, player.y))

            elif self.main_menu:
                if not self.new_game_confirm and not self.updates_check and not self.settings:
                    screen.blit(pygame.font.Font(None, 40).render('RPG BETA 1.4', True, (235, 0, 0)), (width / 2 - 150, 5))
                    screen.blit(pygame.transform.smoothscale(pygame.image.load('Image/Player/animations/attack/player_attack_left.png'), (500, 500)),(600, 80))
                    with open('files/txt/save_01.txt', 'r') as f:
                        file = f.readlines()

                    text_new_game = pygame.font.Font(None, 40).render('[*] Начать новую игру', True, (255, 255, 255))
                    text_continue = pygame.font.Font(None, 40).render('[*] Продолжить игру', True, (255, 255, 255) if file else (100, 100, 100))
                    update_list = pygame.font.Font(None, 40).render('[*] Список Изменений', True, (255, 255, 255))
                    settings_text = pygame.font.Font(None, 40).render('[*] Настройки', True, (255, 255, 255))
                    text_exit = pygame.font.Font(None, 40).render('[*] Выход', True, (255, 0, 0))

                    text_new_game_rect = pygame.Rect(25, 100, text_new_game.get_width(), text_new_game.get_height())
                    text_continue_rect = pygame.Rect(25, 150, text_continue.get_width(), text_continue.get_height())
                    update_list_rect = pygame.Rect(25, 200, update_list.get_width(), update_list.get_height())
                    settings_text_rect = pygame.Rect(25, 250, settings_text.get_width(), settings_text.get_height())
                    text_exit_rect = pygame.Rect(25, 300, text_exit.get_width(), text_exit.get_height())

                    if pygame.mouse.get_pressed()[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        if text_new_game_rect.collidepoint(mouse_pos):
                            if file:
                                self.new_game_confirm = True
                            else:
                                self.main_menu = False

                        if text_continue_rect.collidepoint(mouse_pos) and file:
                            self.main_menu = False

                        elif text_continue_rect.collidepoint(mouse_pos) and not file:
                            screen.blit(pygame.font.Font(None, 30).render('У вас нет ещё ни одного сохранения', True, (100, 100, 100)), (15, height - 40))

                        if update_list_rect.collidepoint(mouse_pos):
                            self.updates_check = True

                        if settings_text_rect.collidepoint(mouse_pos):
                            self.settings = True

                        if text_exit_rect.collidepoint(mouse_pos):
                            player.save_game()
                            pygame.quit()

                    screen.blit(text_new_game, text_new_game_rect)
                    screen.blit(text_continue, text_continue_rect)
                    screen.blit(update_list, update_list_rect)
                    screen.blit(settings_text, settings_text_rect)
                    screen.blit(text_exit, text_exit_rect)

                elif self.settings:
                    if not self.music_choicer and not self.wait_music:
                        screen.blit(pygame.font.Font(None, 50).render('Настройки', True, (235, 0, 0)), (450, 5))

                        music_choicer_text = pygame.font.Font(None, 40).render('[*] Настройки музыки', True, (255, 255, 255))
                        music_choicer_rect = pygame.Rect(25, 80, music_choicer_text.get_width(), music_choicer_text.get_height())
                        screen.blit(music_choicer_text, music_choicer_rect)

                        text_exit = pygame.font.Font(None, 40).render('<<', True, (255, 0, 0))
                        text_exit_rect = pygame.Rect(5, 30, text_exit.get_width(), text_exit.get_height())
                        screen.blit(text_exit, text_exit_rect)

                        if pygame.mouse.get_pressed()[0]:
                            mouse_pos = pygame.mouse.get_pos()
                            if music_choicer_rect.collidepoint(mouse_pos):
                                self.music_choicer = True
                            if text_exit_rect.collidepoint(mouse_pos):
                                self.settings = False

                    elif self.wait_music:
                        screen.fill((0, 0, 0))
                        screen.blit(pygame.font.Font(None, 30).render('Добавление песни', True, (255, 255, 255)), (500, 5))
                        screen.blit(pygame.font.Font(None, 50).render('Перетащите файл mp3 в это окно для добавления', True, (144, 144, 144)), (100, 300))
                        text_exit = pygame.font.Font(None, 40).render('<<', True, (255, 0, 0))
                        text_exit_rect = pygame.Rect(10, 20, text_exit.get_width(), text_exit.get_height())
                        if pygame.mouse.get_pressed()[0]:
                            mouse_pos = pygame.mouse.get_pos()
                            if text_exit_rect.collidepoint(mouse_pos):
                                self.wait_music = False
                        screen.blit(text_exit, text_exit_rect)

                    else:
                        screen.fill((0, 0, 0))
                        y_m = 100
                        x_m = 25
                        music_texts = [pygame.font.Font(None, 30).render(music.split('.')[0], False, (255, 255, 255) if player.current_music == music else (144, 144, 144)) for music in os.listdir('files/music')]
                        music_rects = []

                        text_exit = pygame.font.Font(None, 40).render('<<', True, (255, 0, 0))
                        text_exit_rect = pygame.Rect(5, 5, text_exit.get_width(), text_exit.get_height())

                        add_music_text = pygame.font.Font(None, 30).render('Добавить песню', True, (255, 255, 255))
                        add_music_text_rect = pygame.Rect(20, height-100, add_music_text.get_width(), add_music_text.get_height())

                        stop_music_text = pygame.font.Font(None, 30).render('Остановить музыку', True, (255, 255, 255) if not player.pause else (144, 144, 144))
                        stop_music_rect = pygame.Rect(500, height-100, stop_music_text.get_width(), stop_music_text.get_height())
                        for i, music in enumerate(os.listdir('files/music')):
                            music_rects.append(pygame.Rect(x_m, y_m, music_texts[i].get_width(), music_texts[i].get_height()))
                            if y_m < height-100:
                                y_m += 25
                            else:
                                y_m = 100
                                x_m += 100

                        screen.blit(add_music_text, add_music_text_rect)
                        if pygame.mouse.get_pressed()[0]:
                            mouse_pos = pygame.mouse.get_pos()
                            for i, rect in enumerate(music_rects):
                                if rect.collidepoint(mouse_pos):
                                    player.current_music = os.listdir('files/music')[i]
                                    pygame.mixer.music.load(f'files/music/{player.current_music}')
                                    pygame.mixer.music.play(-1)
                            if text_exit_rect.collidepoint(mouse_pos):
                                self.music_choicer = False
                            if add_music_text_rect.collidepoint(mouse_pos):
                                self.wait_music = True
                            if stop_music_rect.collidepoint(mouse_pos):
                                player.pause = not player.pause
                                if player.pause:
                                    pygame.mixer.music.pause()
                                else:
                                    pygame.mixer.music.unpause()

                        for i, music in enumerate(music_texts):
                            screen.blit(music, music_rects[i])
                        screen.blit(pygame.font.Font(None, 50).render('Выбор песни', True, (235, 0, 0)), (450, 5))
                        screen.blit(text_exit, text_exit_rect)
                        screen.blit(stop_music_text, stop_music_rect)

                elif self.updates_check:
                    screen.fill((0, 0, 0))
                    screen.blit(pygame.transform.smoothscale(pygame.image.load('Image/Player/static/playerstatic_left.png'), (400, 400)), (700, 300))
                    text_for_exit = pygame.font.Font(None, 40).render('<<', True, (255, 0, 0))
                    screen.blit(pygame.font.Font(None, 50).render('Список обновлений', True, (255, 255, 255)), (500, 5))

                    screen.blit(pygame.font.Font(None, 30).render('1.0 - сделана игра с нуля, уже были такие функции как движение игрока, анимации и так далее.', True, (255, 255, 255)), (25, 100))
                    screen.blit(pygame.font.Font(None, 30).render('1.1 - немного оптимизировал игру, укоротил название в главном меню с \"RPG BETA 1.0 TEST\", на \"RPG BETA 1.1\".', True, (255, 255, 255)), (25, 150))
                    screen.blit(pygame.font.Font(None, 30).render('1.2 - фикс одного бага (враг не увеличивался при поднятии бонусов), добавление списка изменений.', True, (255, 255, 255)), (25, 200))
                    screen.blit(pygame.font.Font(None, 30).render('Переделаны текстуры атаки игрока', True, (255, 255, 255)), (800, 230))
                    screen.blit(pygame.font.Font(None, 30).render('1.3 - Добавлена музыка на фон (вы можете её изменить и позже переключать из добавленных), и настройки.', True, (255, 255, 255)), (25, 270))
                    screen.blit(pygame.font.Font(None, 30).render('1.4 - Добавлена возможность остановить музыку в настройках.', True, (255, 255, 255)), (25, 320))

                    text_for_exit_rect = pygame.Rect(5, 5, text_for_exit.get_width(), text_exit.get_height())
                    screen.blit(text_for_exit, text_for_exit_rect)
                    if pygame.mouse.get_pressed()[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        if text_for_exit_rect.collidepoint(mouse_pos):
                            self.updates_check = False
                else:
                    screen.fill((0, 0, 0))
                    # рисуем рамку
                    pygame.draw.line(screen, (100, 100, 100), (width / 2 - 300, 200), (width / 2 - 300, 500), 5)
                    pygame.draw.line(screen, (100, 100, 100), (width / 2 - 300, 500), (width / 2 + 300, 500), 5)
                    pygame.draw.line(screen, (100, 100, 100), (width / 2 + 300, 500), (width / 2 + 300, 200), 5)
                    pygame.draw.line(screen, (100, 100, 100), (width / 2 - 300, 200), (width / 2 + 300, 200), 5)

                    screen.blit(pygame.font.Font(None, 29).render('Вы уверены? Все сохранения будут безвозвратно удалены', False, (255, 255, 255)), (width / 2 - 295, 250))
                    text_confirm = pygame.font.Font(None, 30).render('Да', True, (255, 0, 0))
                    text_cancel = pygame.font.Font(None, 30).render('Нет', True, (0, 255, 0))

                    screen.blit(text_confirm, (width / 2 - 280, 400))
                    screen.blit(text_cancel, (width / 2 + 200, 400))

                    text_confirm_rect = pygame.Rect(width / 2 - 280, 400, text_confirm.get_width(), text_confirm.get_height())
                    text_cancel_rect = pygame.Rect(width / 2 + 200, 400, text_cancel.get_width(), text_cancel.get_height())

                    if pygame.mouse.get_pressed()[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        if text_confirm_rect.collidepoint(mouse_pos):
                            with open('files/txt/save_01.txt', 'w') as f:
                                f.write('')
                            player = Player(x=200, y=100,
                                            width=32, height=35,
                                            image_path='Image/Player/static/playerstatic_down.png',
                                            current_hp=100, speed=0.2, current_damage=5, max_hp=100, current_level=1)
                            self.new_game_confirm = False
                            self.main_menu = False
                        if text_cancel_rect.collidepoint(mouse_pos):
                            self.new_game_confirm = False
            elif self.menu_with_skillpoints_opened:
                text = pygame.font.Font(None, 50).render(f'Меню прокачки навыков', True, (255, 255, 255))
                screen.blit(text, (400, 30))

                back = pygame.font.Font(None, 40).render(f'<<', True, (255, 0, 0))
                back_rect = pygame.Rect(0, 30, back.get_width(), back.get_height())
                screen.blit(back, back_rect)

                text = pygame.font.Font(None, 30).render(f'На данный момент у вас {player.skillpoint} очков навыка', True, (255, 255, 255))
                screen.blit(text, (410, 70))

                power_of_player = pygame.font.Font(None, 30).render(f'Сила персонажа: {player.current_damage} ({player.added_power}) [+]', False, (255, 255, 255))
                power_of_player_rect = pygame.Rect(10, 100, power_of_player.get_width(), power_of_player.get_height())
                screen.blit(power_of_player, power_of_player_rect)

                health_of_player = pygame.font.Font(None, 30).render(f'Здоровье персонажа: {player.max_hp} ({player.added_hp}) [+]', False, (255, 255, 255))
                health_of_player_rect = pygame.Rect(10, 140, health_of_player.get_width(), health_of_player.get_height())
                screen.blit(health_of_player, health_of_player_rect)


                if pygame.mouse.get_pressed()[0]:
                    mouse_pos = pygame.mouse.get_pos()
                    if power_of_player_rect.collidepoint(mouse_pos) and player.skillpoint > 0:
                        player.added_power += 1
                        player.skillpoint -= 1
                        player.current_damage += 5

                    elif health_of_player_rect.collidepoint(mouse_pos) and player.skillpoint > 0:
                        player.added_hp += 1
                        player.skillpoint -= 1
                        player.max_hp += 5

                    elif power_of_player_rect.collidepoint(mouse_pos) and player.skillpoint <= 0 or health_of_player_rect.collidepoint(mouse_pos) and player.skillpoint <= 0:
                        text = pygame.font.Font(None, 30).render(f'У вас недостаточно очков навыков', True, (90, 90, 90))
                        screen.blit(text, (0, 600))

                    elif back_rect.collidepoint(mouse_pos):
                        self.menu_with_skillpoints_opened = False

            elif self.menu_opened:
                font = pygame.font.Font(None, 30)

                text = pygame.font.Font(None, 50).render('Меню вашего персонажа', True, (255, 255, 255))
                screen.blit(text, (width / 2 - 50, 0))

                text = font.render(f'Здоровье: {player.current_hp}/{player.max_hp}', False, (255, 255, 255))
                screen.blit(text, (200, 100))
                text = font.render(f'Атака: {player.current_damage}', False, (255, 255, 255))
                screen.blit(text, (200, 130))
                text = font.render(f'Уровень: {player.current_level}', False, (255, 255, 255))
                screen.blit(text, (200, 160))
                text = font.render(f'Сейчас очков опыта: {player.current_xp}', True, (255, 255, 255))
                screen.blit(text, (200, 190))
                text = font.render(f'Сейчас очков навыков: {player.skillpoint}', True, (255, 255, 255))
                screen.blit(text, (200, 220))
                text = font.render(f'До следующего уровня: {str(str('-' * player.current_need_xp)[:10]).replace('-', '=', player.current_xp)} {player.current_need_xp - player.current_xp}', True, (255, 255, 255))
                screen.blit(text, (0, 600))
                screen.blit(pygame.transform.smoothscale(pygame.image.load('Image/Player/static/playerstatic_down.png'), (500, 500)), (590, 100))

                greeting_menu_button = font.render(f'<< В главное меню', True, (255, 0, 0))
                screen.blit(greeting_menu_button, (10, 5))
                greeting_menu_button_rect = pygame.Rect(10, 5, greeting_menu_button.get_width(), greeting_menu_button.get_height())

                skillpoints_button = font.render(f'Использовать Skillpoints', True, (90, 90, 90))
                screen.blit(skillpoints_button, (200, 270))
                skillpoints_rect = pygame.Rect(200, 270, skillpoints_button.get_width(), skillpoints_button.get_height())
                if pygame.mouse.get_pressed()[0]:
                    mouse_pos = pygame.mouse.get_pos()
                    if skillpoints_rect.collidepoint(mouse_pos):
                        self.menu_with_skillpoints_opened = True
                    elif greeting_menu_button_rect.collidepoint(mouse_pos):
                        self.main_menu = True
                        self.menu_opened = False

            if player.current_xp >= player.current_need_xp:
                player.level_up()

            # keys = pygame.key.get_pressed()
            # if keys[pygame.K_k] and keys[pygame.K_r] and keys[pygame.K_m]:
            #     player.current_xp += 10
            pygame.display.flip()
            self.clock.tick(800)


if __name__ == "__main__":
    run = Runner()
    run.run()
