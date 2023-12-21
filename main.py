import json
import random

import pygame as pg

# Инициализация pg
pg.init()
pg.mixer.init()

# Размеры окна
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550

DOG_WIDTH = 310
DOG_HEIGHT = 500

FOOD_SIZE = 200

TOY_SIZE = 100

DOG_Y = 100

ICON_SIZE = 80
PADDING = 5

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60

MENU_NAV_XPAD = 90
MENU_NAV_YPAD = 130

font = pg.font.Font(None, 40)
font_m = pg.font.Font(None, 16)
font_maxi = pg.font.Font(None, 200)

sounds = {'click_sound': pg.mixer.Sound('sounds/minecraft_click.mp3')}


def render_text(text, t_font=font):
    return t_font.render(str(text), True, pg.Color('black'))


def load_image(img, w, h):
    img = pg.image.load(img).convert_alpha()
    img = pg.transform.scale(img, (w, h))
    return img


def play_sound(sound) -> None:
    sound.play()


class Item:
    def __init__(self, name, price, file, is_bought, is_put_on):
        self.name = name
        self.price = price
        self.is_bought = is_bought
        self.is_put_on = is_put_on

        self.file = file
        self.image = load_image(file, DOG_WIDTH // 1.7, DOG_HEIGHT // 1.7)
        self.full_image = load_image(file, DOG_WIDTH, DOG_HEIGHT)


class Toy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = load_image(random.choice(['images/toys/ball.png', 'images/toys/red bone.png',
                                               'images/toys/blue bone.png']), TOY_SIZE, TOY_SIZE, )
        self.rect = self.image.get_rect()
        self.rect.x = (random.randint(MENU_NAV_XPAD, SCREEN_WIDTH - MENU_NAV_XPAD - 100))
        self.rect.y = 30

    def update(self):
        self.rect.y += 1
        if self.rect.y == SCREEN_HEIGHT - MENU_NAV_YPAD:
            self.kill()


class ClothesMenu:
    def __init__(self, game, data):
        self.game = game
        self.menu_page = load_image('images/menu/menu_page.png', SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bottom_label_off = load_image('images/menu/bottom_label_off.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bottom_label_on = load_image('images/menu/bottom_label_on.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = load_image('images/menu/top_label_off.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = load_image('images/menu/top_label_on.png', SCREEN_WIDTH, SCREEN_HEIGHT)

        self.items = []
        for item in data:
            self.items.append(Item(*item.values()))

        self.current_item = 0

        self.price_t = render_text(self.items[self.current_item].price)
        self.price_tr = self.price_t.get_rect(center=(SCREEN_WIDTH // 2, 177))
        self.name_t = render_text(self.items[self.current_item].name)
        self.name_tr = self.name_t.get_rect(center=(SCREEN_WIDTH // 2, 120))

        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.next_b = Button(SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH, SCREEN_HEIGHT - MENU_NAV_YPAD, 'Вперед',
                             width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2), func=self.to_next)

        self.prev_b = Button(MENU_NAV_XPAD + 30, SCREEN_HEIGHT - MENU_NAV_YPAD, 'Назад',
                             width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2), func=self.to_previous)

        self.buy_b = Button(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 1.4 // 2, SCREEN_HEIGHT // 1.5 + 7, 'Купить',
                            width=int(BUTTON_WIDTH // 1.4), height=int(BUTTON_HEIGHT // 1.4), func=self.buy)

        self.use_b = Button(MENU_NAV_XPAD + 30, SCREEN_HEIGHT - MENU_NAV_YPAD - PADDING - 50, 'Надеть',
                            width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2), func=self.use_item)

        self.text_bought = render_text('Куплено')
        self.buy_text_rect = self.text_bought.get_rect()
        self.buy_text_rect.midright = (SCREEN_WIDTH - 140, 200)

        self.text_put_on = render_text('Надето')
        self.use_text_rect = self.text_put_on.get_rect()
        self.use_text_rect.midright = (SCREEN_WIDTH - 150, 130)

    def to_next(self):
        if self.current_item != len(self.items) - 1:
            self.current_item += 1
        else:
            self.current_item = 0

        self.price_t = render_text(self.items[self.current_item].price)
        self.price_tr = self.price_t.get_rect(center=(SCREEN_WIDTH // 2, 177))

        self.name_t = render_text(self.items[self.current_item].name)
        self.name_tr = self.name_t.get_rect(center=(SCREEN_WIDTH // 2, 120))

    def to_previous(self):
        if self.current_item > 0:
            self.current_item -= 1
        else:
            self.current_item = len(self.items) - 1

        self.price_t = render_text(self.items[self.current_item].price)
        self.price_tr = self.price_t.get_rect(center=(SCREEN_WIDTH // 2, 177))

        self.name_t = render_text(self.items[self.current_item].name)
        self.name_tr = self.name_t.get_rect(center=(SCREEN_WIDTH // 2, 120))

    def buy(self):
        if not self.items[self.current_item].is_bought and self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price
            self.items[self.current_item].is_bought = True

    def use_item(self):
        if self.items[self.current_item].is_bought:
            self.items[self.current_item].is_put_on = not self.items[self.current_item].is_put_on

    def update(self):
        self.buy_b.update()
        self.next_b.update()
        self.prev_b.update()
        self.use_b.update()

    def is_clicked(self, event):
        self.next_b.is_clicked(event)
        self.buy_b.is_clicked(event)
        self.use_b.is_clicked(event)
        self.prev_b.is_clicked(event)

    def draw(self, screen):
        screen.blit(self.menu_page, (0, 0))

        screen.blit(self.items[self.current_item].image, self.item_rect)

        # screen.blit(self.price_t, self.price_tr)
        # screen.blit(self.name_t, self.name_tr)

        self.buy_b.draw(screen)
        self.next_b.draw(screen)
        self.prev_b.draw(screen)
        self.use_b.draw(screen)

        if self.items[self.current_item].is_bought:
            screen.blit(self.bottom_label_on, (0, 0))
        else:
            screen.blit(self.bottom_label_off, (0, 0))
        if self.items[self.current_item].is_put_on:
            screen.blit(self.top_label_on, (0, 0))
        else:
            screen.blit(self.top_label_off, (0, 0))

        screen.blit(self.price_t, self.price_tr)
        screen.blit(self.name_t, self.name_tr)
        screen.blit(self.text_put_on, self.use_text_rect)
        screen.blit(self.text_bought, self.buy_text_rect)


class Food:
    def __init__(self, name, price, image, satiety, medicine_power=0):
        self.name = name
        self.image = load_image(image, FOOD_SIZE, FOOD_SIZE)
        self.price = price
        self.satiety = satiety
        self.medicine_power = medicine_power


class FoodMenu:
    def __init__(self, game):
        self.game = game
        self.menu_page = load_image('images/menu/menu_page.png', SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bottom_label_off = load_image('images/menu/bottom_label_off.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bottom_label_on = load_image('images/menu/bottom_label_on.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = load_image('images/menu/top_label_off.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = load_image('images/menu/top_label_on.png', SCREEN_WIDTH, SCREEN_HEIGHT)

        self.items = [Food('Мясо', 30, 'images/food/meat.png', 10),
                      Food('Яблоко', 20, 'images/food/apple.png', 5),
                      Food('Косточка', 15, 'images/food/bone.png', 2),
                      Food('Корм', 40, 'images/food/dog food.png', 15),
                      Food('Элитный корм', 100, 'images/food/dog food elite.png', 25, medicine_power=2),
                      Food('Витаминки', 200, 'images/food/medicine.png', 1, medicine_power=10)]

        self.current_item = 0

        self.price_t = render_text(self.items[self.current_item].price)
        self.price_tr = self.price_t.get_rect(center=(SCREEN_WIDTH // 2, 177))
        self.name_t = render_text(self.items[self.current_item].name)
        self.name_tr = self.name_t.get_rect(center=(SCREEN_WIDTH // 2, 120))

        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.next_b = Button(SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH, SCREEN_HEIGHT - MENU_NAV_YPAD, 'Вперед',
                             width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2), func=self.to_next)

        self.prev_b = Button(MENU_NAV_XPAD + 30, SCREEN_HEIGHT - MENU_NAV_YPAD, 'Назад',
                             width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2), func=self.to_previous)

        self.eat_b = Button(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 1.4 // 2, SCREEN_HEIGHT // 1.5 + 7, 'Сьесть',
                            width=int(BUTTON_WIDTH // 1.4), height=int(BUTTON_HEIGHT // 1.4), func=self.eat)

    def to_next(self):
        if self.current_item != len(self.items) - 1:
            self.current_item += 1
        else:
            self.current_item = 0

        self.price_t = render_text(self.items[self.current_item].price)
        self.price_tr = self.price_t.get_rect(center=(SCREEN_WIDTH // 2, 177))

        self.name_t = render_text(self.items[self.current_item].name)
        self.name_tr = self.name_t.get_rect(center=(SCREEN_WIDTH // 2, 120))

    def to_previous(self):
        if self.current_item > 0:
            self.current_item -= 1
        else:
            self.current_item = len(self.items) - 1

        self.price_t = render_text(self.items[self.current_item].price)
        self.price_tr = self.price_t.get_rect(center=(SCREEN_WIDTH // 2, 177))

        self.name_t = render_text(self.items[self.current_item].name)
        self.name_tr = self.name_t.get_rect(center=(SCREEN_WIDTH // 2, 120))

    def eat(self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price

            self.game.satiety += self.items[self.current_item].satiety

            if self.game.satiety > 100:
                self.game.satiety = 100

            self.game.health += self.items[self.current_item].medicine_power

            if self.game.health > 100:
                self.game.health = 100

    def update(self):
        self.eat_b.update()
        self.next_b.update()
        self.prev_b.update()

    def is_clicked(self, event):
        self.next_b.is_clicked(event)
        self.eat_b.is_clicked(event)
        self.prev_b.is_clicked(event)

    def draw(self, screen):
        screen.blit(self.menu_page, (0, 0))

        screen.blit(self.items[self.current_item].image, self.item_rect)

        # screen.blit(self.price_t, self.price_tr)
        # screen.blit(self.name_t, self.name_tr)

        self.eat_b.draw(screen)
        self.next_b.draw(screen)
        self.prev_b.draw(screen)

        screen.blit(self.price_t, self.price_tr)
        screen.blit(self.name_t, self.name_tr)


class Button:
    def __init__(self, x, y, text, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, t_font=font, func=None):
        self.idle_img = load_image('images/button.png', width, height)
        self.press_img = load_image('images/button_clicked.png', width, height)
        self.img = self.idle_img
        self.rect = self.img.get_rect()
        self.rect.topleft = (x, y)

        self.ispressed = False

        self.font = t_font
        self.text = render_text(text, self.font)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

        self.func = func

    def draw(self, screen):
        screen.blit(self.img, self.rect)
        screen.blit(self.text, self.text_rect)

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if self.ispressed:
                self.img = self.press_img
            else:
                self.img = self.idle_img

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                sounds['click_sound'].play()
                self.ispressed = True
                self.func()
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.ispressed = False


class Dog(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.img = load_image('images/dog.png', DOG_WIDTH // 2, DOG_HEIGHT // 2)
        self.rect = self.img.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.centery = SCREEN_HEIGHT - MENU_NAV_YPAD - 10

    def update(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_d]:
            if self.rect.right < SCREEN_WIDTH - MENU_NAV_XPAD + 15:
                self.rect.x += 1
        elif keys[pg.K_a]:
            if self.rect.x > MENU_NAV_XPAD - 3:
                self.rect.x -= 1


class MiniGame:
    def __init__(self, game):
        self.game = game

        self.bg = load_image('images/game_background.png', SCREEN_WIDTH, SCREEN_HEIGHT)

        self.dog = Dog()
        self.toys = pg.sprite.Group()

        self.score = 0

        self.start_time = pg.time.get_ticks()
        self.interval = 1000 * 5

    def new_game(self):
        self.dog = Dog()
        self.toys = pg.sprite.Group()

        self.score = 0

        self.start_time = pg.time.get_ticks()
        self.interval = 1000 * 5

    def update(self):
        self.dog.update()
        self.toys.update()
        if random.randint(0, 100) == 0:
            self.toys.add(Toy())
        hits = pg.sprite.spritecollide(self.dog, self.toys, True, pg.sprite.collide_rect_ratio(0.6))
        self.score += len(hits)
        if pg.time.get_ticks() == self.start_time + self.interval:
            self.game.happiness += int(self.score // 2)
            self.game.mode = 'main'

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))

        screen.blit(self.dog.img, self.dog.rect)

        screen.blit(render_text(self.score), (MENU_NAV_XPAD + 20, 80))

        self.toys.draw(screen)


class Game:
    def __init__(self):

        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Виртуальный питомец")

        with open('save.json', encoding='utf-8') as f:
            data = json.load(f)

        self.happiness = data['happiness']
        self.satiety = data['satiety']
        self.health = data['health']
        self.money = data['money']
        self.coins_ps = data['coins_ps']
        self.costs_of_upgrade = {}

        for k, w in data['costs_of_upgrade'].items():
            self.costs_of_upgrade[int(k)] = w

        self.dog_img = load_image('images/dog.png', 310, 500)

        self.bg = load_image('images/background.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.happy_icon = load_image('images/happiness.png', ICON_SIZE, ICON_SIZE)
        self.satiety_icon = load_image('images/satiety.png', ICON_SIZE, ICON_SIZE)
        self.health_icon = load_image('images/health.png', ICON_SIZE, ICON_SIZE)
        self.money_icon = load_image('images/money.png', ICON_SIZE, ICON_SIZE)

        button_x = SCREEN_WIDTH - BUTTON_WIDTH - PADDING

        self.mode = 'main'

        self.clothes_menu = ClothesMenu(self, data["clothes"])

        self.food_menu = FoodMenu(self)

        self.mini_game = MiniGame(self)

        self.eat_b = Button(button_x, PADDING + ICON_SIZE * 1, 'Еда', func=self.food_menu_on)
        self.clothes_b = Button(button_x, PADDING + ICON_SIZE * 2, 'Одежда', func=self.clothes_menu_on)
        self.game_b = Button(button_x, PADDING + ICON_SIZE * 3, 'Игры', func=self.game_on)

        self.upgrade_b = Button(SCREEN_WIDTH - ICON_SIZE, 0, 'Улучшить',
                                width=BUTTON_WIDTH // 3, height=BUTTON_HEIGHT // 3,
                                t_font=font_m, func=self.increase_money)

        self.buttons = [self.eat_b, self.clothes_b, self.game_b, self.upgrade_b]

        self.INCREASE_COINS = pg.USEREVENT + 1
        pg.time.set_timer(self.INCREASE_COINS, 1000)

        self.DECREASE = pg.USEREVENT + 1
        pg.time.set_timer(self.DECREASE, 1000)

        self.run()

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()

    def clothes_menu_on(self):
        self.mode = 'Clothes menu'

    def food_menu_on(self):
        self.mode = 'Food menu'

    def game_on(self):
        self.mode = 'minigame'
        self.mini_game.new_game()

    def increase_money(self):
        for cost in self.costs_of_upgrade.keys():
            if not self.costs_of_upgrade[cost]:
                if self.money >= cost:
                    self.coins_ps += 1
                    self.money -= cost
                    self.costs_of_upgrade[cost] = True
                    break

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:

                if self.mode == 'gameover':
                    data = {
                        "happiness": 100,
                        "satiety": 100,
                        "health": 100,
                        "money": 10,
                        "coins_ps": 1,
                        "costs_of_upgrade": {
                            "100": False,
                            "1000": False,
                            "5000": False,
                            "10000": False
                        },
                        "clothes": [
                            {
                                "name": "Синяя футболка",
                                "price": 10,
                                "image": "images/items/blue t-shirt.png",
                                "is_bought": False,
                                "is_put_on": False
                            },
                            {
                                "name": "Красная футболка",
                                "price": 30,
                                "image": "images/items/red t-shirt.png",
                                "is_bought": False,
                                "is_put_on": False
                            },
                            {
                                "name": "Желтая футболка",
                                "price": 50,
                                "image": "images/items/yellow t-shirt.png",
                                "is_bought": False,
                                "is_put_on": False
                            },
                            {
                                "name": "Ботинки",
                                "price": 50,
                                "image": "images/items/boots.png",
                                "is_bought": False,
                                "is_put_on": False
                            },
                            {
                                "name": "Шляпка",
                                "price": 55,
                                "image": "images/items/hat.png",
                                "is_bought": False,
                                "is_put_on": False
                            },
                            {
                                "name": "Кепка",
                                "price": 25,
                                "image": "images/items/cap.png",
                                "is_bought": False,
                                "is_put_on": False
                            },
                            {
                                "name": "Бантик",
                                "price": 15,
                                "image": "images/items/bow.png",
                                "is_bought": False,
                                "is_put_on": False
                            },
                            {
                                "name": "Солнечные очки",
                                "price": 35,
                                "image": "images/items/sunglasses.png",
                                "is_bought": False,
                                "is_put_on": False
                            },
                            {
                                "name": "Серебрянная цепочка",
                                "price": 70,
                                "image": "images/items/silver chain.png",
                                "is_bought": False,
                                "is_put_on": False
                            },
                            {
                                "name": "Золотая цепочка",
                                "price": 100,
                                "image": "images/items/gold chain.png",
                                "is_bought": False,
                                "is_put_on": False
                            }
                        ]
                    }

                else:
                    data = {
                        "happiness": self.happiness,
                        "satiety": self.satiety,
                        "health": self.health,
                        "money": self.money,
                        "coins_ps": self.coins_ps,
                        "costs_of_upgrade": {
                            "100": self.costs_of_upgrade[100],
                            "1000": self.costs_of_upgrade[1000],
                            "5000": self.costs_of_upgrade[5000],
                            "10000": self.costs_of_upgrade[10000]
                        },
                        "clothes": []
                    }

                    for item in self.clothes_menu.items:
                        data['clothes'].append({"name": item.name,
                                                "price": item.price,
                                                "image": item.file,
                                                "is_bought": item.is_bought,
                                                "is_put_on": item.is_put_on})

                with open('save.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False)

                pg.quit()
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.mode = 'main'

            if event.type == self.INCREASE_COINS:
                self.money += self.coins_ps

            if event.type == self.DECREASE:
                chance = random.randint(0, 10)
                if chance < 5:
                    self.satiety -= 1
                elif 9 >= chance > 5:
                    self.happiness -= 1
                else:
                    self.health -= 1

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.money += self.coins_ps

            if self.mode == 'main':
                for b in self.buttons:
                    b.is_clicked(event)
            elif self.mode == 'Food menu':
                self.food_menu.is_clicked(event)
            elif self.mode == 'Clothes menu':
                self.clothes_menu.is_clicked(event)

    def update(self):
        if self.mode == 'Clothes menu':
            self.clothes_menu.update()
        elif self.mode == 'Food menu':
            self.food_menu.update()
        elif self.mode == 'main':
            for b in self.buttons:
                b.update()
        elif self.mode == 'minigame':
            self.mini_game.update()

        if self.satiety <= 0 or self.happiness <= 0 or self.health <= 0:
            self.mode = 'gameover'

    def draw(self):
        self.screen.blit(self.bg, (0, 0))

        self.screen.blit(self.happy_icon, (PADDING, PADDING))
        self.screen.blit(self.satiety_icon, (PADDING, PADDING * 2 + ICON_SIZE))
        self.screen.blit(self.health_icon, (PADDING, PADDING * 3 + ICON_SIZE * 2))
        self.screen.blit(self.money_icon, (SCREEN_WIDTH - PADDING - 75, PADDING - 5))
        self.screen.blit(self.dog_img, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 150))

        self.screen.blit(render_text(self.happiness, font), (PADDING + ICON_SIZE, PADDING * 6))
        self.screen.blit(render_text(self.satiety, font), (PADDING + ICON_SIZE, PADDING * 7 + ICON_SIZE * 1))
        self.screen.blit(render_text(self.health, font), (PADDING + ICON_SIZE, PADDING * 8 + ICON_SIZE * 2))
        self.screen.blit(render_text(self.money, font), (SCREEN_WIDTH - ICON_SIZE - PADDING * 4, PADDING * 6))

        for b in self.buttons:
            b.draw(self.screen)

        for item in self.clothes_menu.items:
            if item.is_put_on:
                self.screen.blit(item.full_image, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 150))

        if self.mode == 'Clothes menu':
            self.clothes_menu.draw(self.screen)

        if self.mode == 'Food menu':
            self.food_menu.draw(self.screen)

        if self.mode == 'minigame':
            self.mini_game.draw(self.screen)

        if self.mode == 'gameover':
            text = font_maxi.render('ПРОИГРЫШ', True, 'red')
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)

        pg.display.flip()


if __name__ == "__main__":
    Game()
