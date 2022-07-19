import pygame
from sys import exit
from random import randrange, choice


class Player(pygame.sprite.Sprite): # create player
    def __init__(self, heat, speed):
        super().__init__()
        self.image = pygame.Surface((48, 48))
        self.image.fill((20, 20, 20))
        pygame.draw.polygon(self.image, pygame.Color(30, 144, 255), ((0, 0), (48, 24), (0, 48)))
        self.rect = self.image.get_rect(center=(100, height/2))
        self.speed = speed
        self.heat = heat
        self.weapon = weapon
        self.wep_h = weapon_heat

    def move(self): # move player
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.y - self.speed > 48:
            self.rect.y -= self.speed
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.y + self.speed + 32 < height:
            self.rect.y += self.speed
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.x - self.speed > 0:
            self.rect.x -= self.speed
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.x + self.speed + 32 < width:
            self.rect.x += self.speed

    def shoot(self): # player shooting
        global heat
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    if self.weapon == 'laser' and heat + weapon_heat <= 100:
                        lasers.add(Projectile(self.rect.center, self.weapon))
                        heat += 10
                    elif self.weapon == 'plasma' and heat + weapon_heat + 3 <= 100:
                        lasers.add(Projectile(self.rect.topleft, self.weapon))
                        lasers.add(Projectile(self.rect.bottomleft, self.weapon))
                        heat += 13
                    elif self.weapon == 'rail' and heat + weapon_heat + 2 <= 100:
                        lasers.add(Projectile(self.rect.topleft, self.weapon))
                        lasers.add(Projectile(self.rect.center, self.weapon))
                        lasers.add(Projectile(self.rect.bottomleft, self.weapon))
                        heat += 12

    def change_wep(self): # weapon upgrades
        global weapon
        self.weapon = weapon

    def update(self):
        self.move()
        self.shoot()
        self.change_wep()


class Projectile(pygame.sprite.Sprite): # player projectiles
    def __init__(self,pos, type):
        super().__init__()
        if type == 'laser':
            self.image = pygame.Surface((48, 8))
            self.image.fill((255,20,147))
            self.rect = self.image.get_rect(center=pos)
            self.pos = pos
            self.speed = 15
        elif type == 'plasma':
            self.image = pygame.Surface((12, 12))
            self.image.fill((20, 20, 20))
            pygame.draw.circle(self.image, (0, 191, 255), (6, 6), 6)
            self.rect = self.image.get_rect(center=pos)
            self.pos = pos
            self.speed = 15
        elif type == 'rail':
            self.image = pygame.Surface((24, 6))
            self.image.fill((244, 164, 96))
            self.rect = self.image.get_rect(center=pos)
            self.pos = pos
            self.speed = 15

    def move(self): # projectile motion
        self.rect.x += self.speed
        if self.rect.x > width - 20:
            self.kill()

    def update(self):
        self.move()


class Rock(pygame.sprite.Sprite): # big obstacle
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((64, 64))
        self.image.fill((20, 20, 20))
        pygame.draw.circle(self.image, (139, 0, 0), (32, 32), 32)
        #self.image = pygame.image.load(os.path.join("assets", "aster2.png"))
        self.rect = self.image.get_rect(center=(width + 100, randrange(70, height - 70)))
        self.type = "red"
        self.speed = speed

    def update(self): # move it slow
        self.rect.x -= self.speed
        if self.rect.x < -100:
            self.kill()


class Asteroid(pygame.sprite.Sprite): # medium obstacle
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((48, 48))
        self.image.fill((20, 20, 20))
        pygame.draw.circle(self.image, (0, 139, 0), (24, 24), 24)
        self.rect = self.image.get_rect(center=(width + 100, randrange(70, height - 70)))
        self.type = "green"
        self.speed = int(speed * 1.40)

    def update(self): # move it faster
        self.rect.x -= self.speed
        if self.rect.x < -100:
            self.kill()


class Comet(pygame.sprite.Sprite): # small obstacle
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill((20, 20, 20))
        pygame.draw.circle(self.image, (255, 250, 240), (16, 16), 16)
        self.rect = self.image.get_rect(center=(width + 100, randrange(70, height - 70)))
        self.type = "comet"
        self.speed = speed * 2

    def update(self): # go fast
        self.rect.x -= self.speed
        if self.rect.x < -100:
            self.kill()


class Button: # menus need buttons
    def __init__(self, text, w, h, pos, num):
        self.pressed = False
        self.type = num
        self.updated = False

        self.rect = pygame.Rect(pos, (w, h))
        self.color = (238, 232, 170)
        self.text = button_font.render(text, True, (20, 20, 20))
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def show_button(self): # see buttons
        pygame.draw.rect(screen, self.color, self.rect, border_radius=12)
        screen.blit(self.text, self.text_rect)
        self.mouse_control()

    def mouse_control(self): # change colors, track mouse
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.color = (70, 130, 180)
            if self.type <= 5:
                if pygame.mouse.get_pressed()[0]:
                    self.pressed = True
                else:
                    if self.pressed:
                        button_handle(self.type)
                        self.pressed = False
            else:
                if pygame.mouse.get_pressed()[0]:
                    self.pressed = True
                else:
                    if self.pressed:
                        if science >= up_cost:
                            upgrade_handle(self.type)
                            self.updated = True
                            self.pressed = False
        else:
            if self.updated:
                self.color = (169, 169, 169)
            else:
                self.color = (238, 232, 170)


def collision(ship, lasers, rocks): # handle collisions in game
    global score, science, probes, game_state, heat
    for rock in rocks:
        if pygame.sprite.spritecollide(rock, ship, False): # player death
            end_surf = middle_font.render(f"Ship Destroyed", False, (238, 232, 170))
            end_rect = end_surf.get_rect(center=(width / 2, height / 2 - 45))
            end_score_surf = middle_font.render(f"Score:{score}", False, (238, 232, 170))
            end_score_rect = end_score_surf.get_rect(center=(width / 2, height / 2 + 45))
            screen.blit(end_surf, end_rect)
            screen.blit(end_score_surf, end_score_rect)
            pygame.display.update()
            pygame.time.delay(2000)
            reset_stats()
            rocks.empty()
            lasers.empty()
            game_state = "main_menu"

        if pygame.sprite.groupcollide(rocks, lasers, True, True): # projectile hitting an obstacle
            if rock.type == "red":
                score += 10
                probes += 1
            elif rock.type == "green":
                score += 15
                probes += 1
            elif rock.type == "comet":
                score += 50
                probes += 5
    if probes >= 10:
        probes = 0
        science += 1


def labels(score, heat): # top screen info
    score_surf = top_font.render(f'Score: {score}', False, (238, 232, 170))
    score_rect = score_surf.get_rect(center=(width / 2, 30))
    screen.blit(score_surf, score_rect)

    heat_label = top_font.render(f'Heat:', False, (238, 232, 170))
    heat_label_rect = heat_label.get_rect(center=(50,30))
    screen.blit(heat_label, heat_label_rect)
    pygame.draw.rect(screen, (0, 255, 0), (100, 20, 200, 25))
    pygame.draw.rect(screen, (255, 0, 0), (100, 20, heat/0.5, 25))
    pygame.draw.rect(screen, (238, 232, 170), (100, 20, 200, 25), 4)

    score_surf = top_font.render(f'Knowledge: {science}', False, (238, 232, 170))
    score_rect = score_surf.get_rect(center=(width - 110, 30))
    screen.blit(score_surf, score_rect)

def game_quit(): # exit game
    pygame.quit()
    exit()

def heat_sink(vents): # reduce heat
    global heat
    if heat > 0:
        heat -= vents

def button_handle(type): # check what buttons do
    global game_state
    if type == 1:
        game_state = 'play'
    elif type == 2:
        game_state = 'upgrades'
    elif type == 3:
        game_state = 'controls'
    elif type == 5:
        game_state = 'main_menu'
    elif type == 4:
        game_quit()

def game_menu(): # start screen
    button1.show_button()
    button2.show_button()
    button3.show_button()
    button4.show_button()
    title_surf = middle_font.render(f'Comet Chaser', True, (238, 232, 170))
    title_rect = title_surf.get_rect(center=(640, 100))
    screen.blit(title_surf, title_rect)

def game_controls(): # game controls info screen
    movement_surf = control_font.render(f'WASD or Arrow keys - Move', True, (238, 232, 170))
    movement_rect = movement_surf.get_rect(center=(640, 180))
    screen.blit(movement_surf, movement_rect)
    shoot_surf = control_font.render(f'Space - Engage weapon ', True, (238, 232, 170))
    shoot_rect = shoot_surf.get_rect(center=(640, 240))
    screen.blit(shoot_surf, shoot_rect)
    back_to_menu_surf = control_font.render(f'Esc - Return to menu', True, (238, 232, 170))
    back_to_menu_rect = back_to_menu_surf.get_rect(center=(640, 310))
    screen.blit(back_to_menu_surf, back_to_menu_rect)
    button5.show_button()

def ship_upgrades(): # updates screen
    global up_cost
    upgrade_surf = control_font.render('Plasma Pulse', True, (238, 232, 170))
    upgrade_rect = upgrade_surf.get_rect(center=(180, 100))
    screen.blit(upgrade_surf, upgrade_rect)
    upgrade_surf = control_font.render('Rail Torpedo', True, (238, 232, 170))
    upgrade_rect = upgrade_surf.get_rect(center=(180, 240))
    screen.blit(upgrade_surf, upgrade_rect)
    upgrade_surf = control_font.render('Forward Thrusters', True, (238, 232, 170))
    upgrade_rect = upgrade_surf.get_rect(center=(600, 100))
    screen.blit(upgrade_surf, upgrade_rect)
    upgrade_surf = control_font.render('Course Engines', True, (238, 232, 170))
    upgrade_rect = upgrade_surf.get_rect(center=(600, 240))
    screen.blit(upgrade_surf, upgrade_rect)
    upgrade_surf = control_font.render('Heat Sink', True, (238, 232, 170))
    upgrade_rect = upgrade_surf.get_rect(center=(1000, 100))
    screen.blit(upgrade_surf, upgrade_rect)
    upgrade_surf = control_font.render('Weapon Cooler', True, (238, 232, 170))
    upgrade_rect = upgrade_surf.get_rect(center=(1000, 240))
    screen.blit(upgrade_surf, upgrade_rect)

    cost_surf = control_font.render(f'Equip for {up_cost} knowledge', True, (238, 232, 170))
    cost_rect = cost_surf.get_rect(center=(640, 600))
    screen.blit(cost_surf, cost_rect)

    button5.show_button()
    button6.show_button()
    button7.show_button()
    button8.show_button()
    button9.show_button()
    button10.show_button()
    button11.show_button()

def upgrade_handle(type): # put upgrades into play
    global rock_speed, heat, player_speed, up_cost, weapon, science, vents, weapon_heat
    if type == 6:
        weapon = 'plasma'
        science -= up_cost
        up_cost = int(up_cost * 1.50)
    elif type == 7:
        weapon = 'rail'
        science -= up_cost
        up_cost = int(up_cost * 1.50)
    elif type == 8:
        rock_speed = 10
        science -= up_cost
        up_cost = int(up_cost * 1.50)
    elif type == 9:
        player_speed = 20
        science -= up_cost
        up_cost = int(up_cost * 1.50)
    elif type == 10:
        vents = 12
        science -= up_cost
        up_cost = int(up_cost * 1.50)
    elif type == 11:
        weapon_heat = 8
        science -= up_cost
        up_cost = int(up_cost * 1.50)

def reset_stats(): # reset on player death
    global score, heat, science, probes, weapon, player_speed, rock_speed, vents, weapon_heat
    score = 0
    heat = 0
    science = 0
    probes = 0
    weapon = 'laser'
    player_speed = 12
    rock_speed = 6
    vents = 6
    weapon_heat = 10

def run_game(): # draw all on screen
    ship.draw(screen)
    ship.update()
    rocks.draw(screen)
    rocks.update()
    lasers.draw(screen)
    lasers.update()
    collision(ship, lasers, rocks)
    labels(score, heat)

# initiate pygame
pygame.init()
width, height = 1280, 720
screen = pygame.display.set_mode((width,height), flags=pygame.RESIZABLE)
pygame.display.set_caption("Comet Chaser")
clock = pygame.time.Clock()

# fonts
top_font = pygame.font.SysFont("comicsans", 30)
middle_font = pygame.font.SysFont("comicsans", 75)
control_font = pygame.font.SysFont("comicsans", 50)
button_font = pygame.font.SysFont("comicsans", 20)

# button obj
button1 = Button('Play', 200, 40, (550, 250), 1)
button2 = Button('Upgrades', 200, 40, (550, 300), 2)
button3 = Button('Controls', 200, 40, (550, 350), 3)
button4 = Button('Quit', 200, 40, (550, 400), 4)
button5 = Button('Back', 200, 40, (550, 450), 5)
button6 = Button('Equip', 200, 40, (120, 150), 6)
button7 = Button('Equip', 200, 40, (120, 300), 7)
button8 = Button('Equip', 200, 40, (550, 150), 8)
button9 = Button('Equip', 200, 40, (550, 300), 9)
button10 = Button('Equip', 200, 40, (900, 150), 10)
button11 = Button('Equip', 200, 40, (900, 300), 11)

# control game states
game_state = 'main_menu'
# ingame stats
score = 0
player_speed = 12
weapon = 'laser'
rock_speed = 6
heat = 0
science = 0
probes = 0
up_cost = 5
vents = 6
weapon_heat = 10

# timers
spawn_time = 1200
rock_timer = pygame.USEREVENT + 1
pygame.time.set_timer(rock_timer, spawn_time)

vent_time = 500
vent_timer = pygame.USEREVENT + 2
pygame.time.set_timer(vent_timer, vent_time)

# ingame objs
ship = pygame.sprite.GroupSingle()
ship.add(Player(heat, player_speed))
lasers = pygame.sprite.Group()
rocks = pygame.sprite.Group()

while True: # run the game
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            game_quit()

        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                game_state = 'main_menu'

        if event.type == vent_timer and game_state == 'play':
            heat_sink(vents)

        if event.type == rock_timer and game_state == 'play':
            obstacle = choice([1, 1, 1, 1, 1, 1, 2, 2, 2, 3])
            if obstacle == 1:
                rocks.add(Rock(rock_speed)) # why putting obj here creates problems?
            elif obstacle == 2:
                rocks.add(Asteroid(rock_speed))
            elif obstacle == 3:
                rocks.add(Comet(rock_speed))


    screen.fill((20,20,20)) # make background
    if game_state == 'main_menu': # check game state
        game_menu()
    elif game_state == 'controls':
        game_controls()
    elif game_state == 'upgrades':
        ship_upgrades()
    elif game_state == 'play':
        run_game()
    pygame.display.update()
    clock.tick(60)

# no main, selfcontainig file