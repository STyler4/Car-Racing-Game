import pygame
from pygame.locals import *
import random

pygame.init()

# create the window
width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Car Game')

# colours
grey = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

# game settings
gameover = False
speed = 2
score = 0

# markers size
marker_width = 10
marker_height = 50

# road and edge markers
road = (100, 0, 300, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

# x coordinates of lanes
left_lane = 150
centre_lane = 250
right_lane = 350
lanes = [left_lane, centre_lane, right_lane]

# for animating movement of the lane markers
lane_marker_move_y = 0

class Vehicle(pygame.sprite.Sprite):

    def __init__(self, images, x, y, switch_interval=500):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.transform.scale(image, (100, 100)) for image in images]
        self.current_image = 0
        self.image = self.images[self.current_image]

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        self.switch_interval = switch_interval
        self.last_switch = pygame.time.get_ticks()


class PlayerVehicle(Vehicle):

    def __init__(self, x, y):
        image = pygame.image.load('Topdown_vehicle_sprites_pack/car.png')
        super().__init__([image], x, y)


# player's starting coordinates
player_x = 250
player_y = 400

# create the player's car
player_group = pygame.sprite.Group()
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# load the other vehicle images
image_filenames = ['truck.png', 'taxi.png', 'ambulance.png', 'mini_van.png',
                   'audi.png', 'black_viper.png', 'mini_truck.png']
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load('Topdown_vehicle_sprites_pack/' + image_filename)
    vehicle_images.append([image])

# load the police car images
police_images = [pygame.image.load('Topdown_vehicle_sprites_pack/Police_animation/1.png'),
                 pygame.image.load('Topdown_vehicle_sprites_pack/Police_animation/2.png'),
                 pygame.image.load('Topdown_vehicle_sprites_pack/Police_animation/3.png')]
vehicle_images.append(police_images)

# sprite group for vehicles
vehicle_group = pygame.sprite.Group()

# load the crash image
crash = pygame.image.load('Topdown_vehicle_sprites_pack/explosion2.png')
crash_rect = crash.get_rect()

# game loop
clock = pygame.time.Clock()
fps = 120
running = True
while running:

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # move the player's car using the left/right arrow keys
        if event.type == KEYDOWN:

            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100

            # check if there's a side swipe collision after changing lanes
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):

                    gameover = True

                    # place the player's car next to other vehicle
                    # and determine where to position the crash image
                    if event.key == K_LEFT:
                        player.rect.left = vehicle.rect.right
                        crash_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                    elif event.key == K_RIGHT:
                        player.rect.right = vehicle.rect.left
                        crash_rect.center = [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1]) / 2]

    # draw the grass
    screen.fill(green)

    # draw the road
    pygame.draw.rect(screen, grey, road)

    # draw the edge markers
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)

    # draw the lane markers
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (centre_lane + 45, y + lane_marker_move_y, marker_width, marker_height))

    # draw the player's car
    player_group.draw(screen)

    # add up to two vehicles
    if len(vehicle_group) < 2:

        # ensure there's enough gap between vehicles
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False

        if add_vehicle:

            # select a random lane
            lane = random.choice(lanes)

            # select a random vehicle image
            images = random.choice(vehicle_images)
            vehicle = Vehicle(images, lane, height / -2)
            vehicle_group.add(vehicle)

    # make the vehicles move
    for vehicle in vehicle_group:
        vehicle.rect.y += speed

        # switch image if it's time
        now = pygame.time.get_ticks()
        if now - vehicle.last_switch > vehicle.switch_interval:
            vehicle.current_image = (vehicle.current_image + 1) % len(vehicle.images)
            vehicle.image = vehicle.images[vehicle.current_image]
            vehicle.last_switch = now

        # remove the vehicle once it goes off screen
        if vehicle.rect.top >= height:
            vehicle.kill()

            # add to score
            score += 1

            # speed up the game after passing the 5 vehicles
            if score > 0 and score % 5 == 0:
                speed += 1

    # draw the vehicles
    vehicle_group.draw(screen)

    # display the score
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Score: ' + str(score), True, white)
    text_rect = text.get_rect()
    text_rect.center = (50, 450)
    screen.blit(text,text_rect)

    # check if there's a head on collision
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        crash_rect.center = [player.rect.center[0], player.rect.top]

    # display game over
    if gameover:
        screen.blit(crash, crash_rect)

        pygame.draw.rect(screen, red, (0, 50, width, 100))

        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Game over. Play again? (Enter Y or N)', True, white)
        text_rect = text.get_rect()
        text_rect.center = (width / 2, 100)
        screen.blit(text, text_rect)

    pygame.display.update()

    # check if player wants to play again
    while gameover:

        clock.tick(fps)

        for event in pygame.event.get():

            if event.type == QUIT:
                gameover = False
                running = False

            # get the player's input (y or n)
            if event.type == KEYDOWN:
                if event.key == K_y:
                    # reset the game
                    gameover = False
                    speed = 2
                    score = 0
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    # exit the loops
                    gameover = False
                    running = False

pygame.quit()
