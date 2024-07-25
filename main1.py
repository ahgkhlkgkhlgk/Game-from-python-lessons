import time
from sprites import *
is_running = True
c=True

def dialogue_mode(sprite, text):
    sprite.update()
    screen.blit(space, (0, 0))
    screen.blit(sprite.image, sprite.rect)
    text1 = f1.render(text[text_number], True, pg.Color("White"))
    screen.blit(text1, (250, 450))
    if text_number < len(text) - 1:
        text2 = f1.render(text[text_number + 1], True, pg.Color("White"))
        screen.blit(text2, (250, 470))
def dialogue_mode2(sprite, text):
    global is_running
    global c
    sprite.update()
    screen.blit(space, (0, 0))
    screen.blit(sprite.image, sprite.rect)
    if text_number < len(text):
        text1 = f1.render(text[text_number], True, pg.Color("White"))
        screen.blit(text1, (250, 450))
    else:
        is_running = False
        c=False

    if text_number < len(text) - 1:
        text2 = f1.render(text[text_number + 1], True, pg.Color("White"))
        screen.blit(text2, (250, 470))
    else:
        is_running = False
        c=False


pg.init()
pg.mixer.init()
pg.mixer.music.load("tense_intro.wav")
pg.mixer.music.set_volume(0.3)
pg.mixer.music.play()

laser_snd=pg.mixer.Sound("shot_laser.wav")
victory=pg.mixer.Sound("victory.wav")



size = (800, 600)
screen = pg.display.set_mode(size)
pg.display.set_caption("Космические коты")

FPS = 120
clock = pg.time.Clock()


mode = "start_scene"

meteorites = pg.sprite.Group()
mice = pg.sprite.Group()
lasers = pg.sprite.Group()

space = pg.image.load("cap.png")
space = pg.transform.scale(space, size)

heart = pg.image.load("imag.png")
heart = pg.transform.scale(heart, (30, 30))
heart_count = 3

cap = Captain()
alien = Alien()

ship = Starship()

start_text = ["Мы засекли сигнал с планеты Мур.",
              "",
              "Наши друзья, инопланетные коты,",
              "нуждаются в помощи.",
              "Космические мыши хотят съесть их луну,",
              "потому что она похожа на сыр.",
              "Как долго наш народ страдал от них, ",
              "теперь и муряне в беде...",
              "Мы должны помочь им.",
              "Вылетаем прямо сейчас.",
              "Спасибо, что починил звездолёт, штурман. ",
              "Наконец-то функция автопилота работает.",
              "Поехали!"]

alien_text = ["СПАСИТЕ! МЫ ЕЛЕ ДЕРЖИМСЯ!",
              "",
              "Мыши уже начали грызть луну...",
              "Скоро куски луны будут падать на нас.",
              "Спасите муриан!", ]

final_text = ["Огромное вам спасибо,",
              "друзья с планеты Мяу!",
              "Как вас называть? Мяуанцы? Мяуриане?",
              "В любом случае, ",
              "теперь наша планета спасена!",
              "Мы хотим отблагодарить вас.",
              "Капитан Василий и его штурман получают",
              "орден SKYSMART.",
              "А также несколько бутылок нашей",
              "лучшей валерьянки.",
              "",
              ""]

text_number = 0
f1 = pg.font.Font("font.otf", 25)
start = time.time()

while is_running:

    # СОБЫТИЯ
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False
        if event.type == pg.KEYDOWN:
            if mode == "start_scene":
                text_number += 2
                if text_number > len(start_text):
                    text_number = 0
                    mode = "meteorites"

            if mode == "meteorites":
                pass
            if mode == "alien_scene":
                text_number += 2
                if text_number > len(alien_text):
                    text_number = 0
                    mode = "moon"
                    start=time.time()
                    ship.switch_mode()

            if mode == "moon":
                if event.key == pg.K_SPACE:
                    lasers.add(Laser(ship.rect.midtop))
                    laser_snd.play()

            if mode == "final_scene":
                text_number += 2
                if text_number > len(final_text):
                    text_number = 0
                    is_running=False

    # ОБНОВЛЕНИЯ
    if mode == "start_scene":
        dialogue_mode(cap, start_text)

    if mode == "meteorites":
        if time.time() - start > 10:
            mode = "alien_scene"
            text_number = 0

        if random.randint(1, 100) == 1:
            n = Meteorite()
            meteorites.add(n)
        ship.update()
        meteorites.update()

        hits = pg.sprite.spritecollide(ship, meteorites, True)
        for hit in hits:
            heart_count -= 1
            if heart_count <= 0:
                is_running = False

        screen.blit(space, (0, 0))
        screen.blit(ship.image, ship.rect)
        meteorites.draw(screen)
        for i in range(heart_count):
            screen.blit(heart, (i * 40, 0))

    if mode == "alien_scene":
        dialogue_mode(alien, alien_text)

    if mode == "moon":
        if time.time() - start > 10:
            mode = "final_scene"
            text_number = 0
            victory.play()
            pg.mixer.music.fadeout(4)

        if random.randint(1, 100) == 1:
            n = Mouse_starship()
            mice.add(n)
        ship.update()
        mice.update()
        lasers.update()

        hits = pg.sprite.spritecollide(ship, mice, True)
        for hit in hits:
            heart_count -= 1
            if heart_count <= 0:
                is_running = False

        hits = pg.sprite.groupcollide(lasers, mice, True, True)

        screen.blit(space, (0, 0))
        screen.blit(ship.image, ship.rect)
        mice.draw(screen)
        lasers.draw(screen)
        for i in range(heart_count):
            screen.blit(heart, (i * 40, 0))

    if mode == "final_scene":
        if c:
            dialogue_mode2(alien, final_text)
        else:
            pg.quit()

    pg.display.flip()
    clock.tick(FPS)
