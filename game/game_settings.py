# library import block ----------------------------------------------------------------------------------------------- #
from os import path
import pygame


# library init block ------------------------------------------------------------------------------------------------- #
pygame.init
pygame.mixer.pre_init(44100, -16, 50, 4096)
pygame.mixer.init()
pygame.font.init()


# predefined colors -------------------------------------------------------------------------------------------------- #
# may delete it later if all images are transparent
RED = (255, 0, 0)


# window information ------------------------------------------------------------------------------------------------- #
WIDTH = 1200
HIGHT = 800
screen = pygame.display.set_mode((WIDTH, HIGHT))
FPS = 60
clock = pygame.time.Clock()


# save image and sound folder dir to var
img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")


# image loading block ------------------------------------------------------------------------------------------------#
# load backgrounds
backgrounds = {0: pygame.image.load(path.join(img_dir, "space_background_1200x800_nsm.png")).convert()}

# load buttons
# 0 = idle | 1 = mouseover
buttons = {"play0": pygame.image.load(path.join(img_dir, "startmenu_play_button_rgb_red.png")).convert_alpha(),
           "play1": pygame.image.load(path.join(img_dir, "startmenu_play_button_mouseover_rgb_red.png")).convert_alpha()}

# buttons set colorkey
buttons["play0"].set_colorkey(RED)
buttons["play1"].set_colorkey(RED)

# load player sprites
player_images = {0: pygame.image.load(path.join(img_dir, "arwing_idle.png")).convert_alpha(),
                 1: pygame.image.load(path.join(img_dir, "arwing_left.png")).convert_alpha(),
                 2: pygame.image.load(path.join(img_dir, "arwing_right.png")).convert_alpha()}

# transform player sprites to right size
# ...until I get my shit done making it in the right size as png
for counter in range(3):
    player_images[counter] = pygame.transform.scale(player_images[counter], (96, 96))


# create groups ------------------------------------------------------------------------------------------------------ #
all_buttons = pygame.sprite.Group()
all_mouses = pygame.sprite.Group()

# create the all sprites group from here, to use all classes
all_sprites = pygame.sprite.LayeredDirty()
# set first clear image and the surface
all_sprites.clear(screen, backgrounds[0])


# layer predefinition block ------------------------------------------------------------------------------------------ #
# create layer for an object
#   self._layer = layers[classname]
layers = {"Buttons": 1,
          "Mouse": 2}

# sound loading block ------------------------------------------------------------------------------------------------ #
sounds = {"Buttons": pygame.mixer.Sound(path.join(snd_dir, "menu_mouseover_sfx.ogg"))}


# class block -------------------------------------------------------------------------------------------------------- #
# used to create buttons
class Buttons(pygame.sprite.DirtySprite):
    def __init__(self, buttontype, x, y):
        # asign sprite to groups
        pygame.sprite.DirtySprite.__init__(self)

        # safe classname for events and handling
        self.classname = "Buttons"

        # needed for redrawing
        self.dirty = 1

        # set layer for draw order
        self._layer = layers[self.classname]

        # add to group after setting layer
        all_sprites.add(self)
        all_buttons.add(self)

        # set idle button image at first and get its rectangle
        self.buttontype = buttontype

        # set vars for collision handling
        self.collision = 0
        self.collision_detector = 0

        # load image and get its rect and mask
        self.image = buttons[self.buttontype + str(self.collision)]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # set rectangle to given position
        self.rect.x = x
        self.rect.y = y


    def update(self):
        # keep mask updated
        self.mask = pygame.mask.from_surface(self.image)

        # check for collision
        self.check_collision()

    # change self.image depending on collision
    # also used to play mouseover sound
    def change_image(self, hits):
        # if there is a collision ...
        if hits:
            # ... check if image is already changed
            if self.image != buttons[self.buttontype + str(1)]:
                # if not, change it and set dirty
                self.image = buttons[self.buttontype + str(1)]
                sounds[self.classname].play()
                self.dirty = 1
        # if there is no collision
        else:
            # ... check if image is already changed
            if self.image != buttons[self.buttontype + str(0)]:
                # if not, change it and set dirty
                self.image = buttons[self.buttontype + str(0)]
                self.dirty = 1

    def check_collision(self):
        # check if sprite rects collide
        hits = pygame.sprite.groupcollide(all_mouses, all_buttons, False, False)

        # if True, start a pixel perfect collision detection
        if hits:
            hits = pygame.sprite.groupcollide(all_mouses, all_buttons, False, False, pygame.sprite.collide_mask)

        # set image changes if needed
        self.change_image(hits)


# test environment
if __name__ == "__main__":
    pass
