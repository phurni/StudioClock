#!/usr/bin/env python
# Studio Clock by Pascal Hurni, May 2015, made for Olive

import sys, pygame, time, math, os
from pygame.locals import *
from pygame import gfxdraw

# Customize the values here at will
CHECK_DELAY = 50 # in milliseconds
BACKGROUND_COLOR = (0,0,0)

WINDOW_CAPTION = "StudioClock"
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

TIME_FONT_NAME = "scoreboard.ttf" #"LCDMN___.TTF"
TIME_FONT_SIZE = 200
TIME_FORMAT = "%H:%M"
TIME_COLOR = (255,0,0)
TIME_HUE_STEP = 1

HOUR_TICK_RADIUS = 360
HOUR_TICK_SIZE = 8
HOUR_TICK_COLOR = (255,0,0)
HOUR_TICK_HUE_STEP = 1

SECOND_TICK_RADIUS = 320
SECOND_TICK_SIZE = 8
SECOND_TICK_COLOR = (255,0,0)
SECOND_TICK_DIMMED_COLOR = (255,0,0,48)
SECOND_TICK_HUE_STEP = 1

# Some globals
window_center_x = int(WINDOW_WIDTH / 2)
window_center_y = int(WINDOW_HEIGHT / 2)

time_color = pygame.Color(*TIME_COLOR)
hour_tick_color = pygame.Color(*HOUR_TICK_COLOR)
second_tick_color = pygame.Color(*SECOND_TICK_COLOR)
second_tick_dimmed_color = pygame.Color(*SECOND_TICK_DIMMED_COLOR)

# Init pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_CAPTION)
pygame.mouse.set_visible(False)
time_font = pygame.font.Font(TIME_FONT_NAME, TIME_FONT_SIZE)

# Main loop
while True:
    # erase screen
    screen.fill(BACKGROUND_COLOR)

    # get the current time
    now = time.localtime()
    current_second = now.tm_sec
    
    # handle color animation
    color = time_color.hsva
    time_color.hsva = ((color[0]+TIME_HUE_STEP) % 360, color[1], color[2], color[3])
    color = hour_tick_color.hsva
    hour_tick_color.hsva = ((color[0]+HOUR_TICK_HUE_STEP) % 360, color[1], color[2], color[3])
    color = second_tick_color.hsva
    second_tick_color.hsva = ((color[0]+SECOND_TICK_HUE_STEP) % 360, color[1], color[2], color[3])
    color = second_tick_dimmed_color.hsva
    second_tick_dimmed_color.hsva = ((color[0]+SECOND_TICK_HUE_STEP) % 360, color[1], color[2], color[3])

    # Draw the static hour ticks
    for i in range(0, 60, 5):
        x = int((math.sin(2 * math.pi * (i / 60.0))) * HOUR_TICK_RADIUS)
        y = int((-1 * math.cos(2 * math.pi * (i / 60.0))) * HOUR_TICK_RADIUS)
        pygame.gfxdraw.aacircle(screen, (x + window_center_x), (y + window_center_y), HOUR_TICK_SIZE, hour_tick_color)
        pygame.gfxdraw.filled_circle(screen, (x + window_center_x), (y + window_center_y), HOUR_TICK_SIZE, hour_tick_color)

    # Draw the elapsed ticks
    for i in range(current_second+1):
        x = int((math.sin(2 * math.pi * (i / 60.0))) * SECOND_TICK_RADIUS)
        y = int((-1 * math.cos(2 * math.pi * (i / 60.0))) * SECOND_TICK_RADIUS)
        pygame.gfxdraw.aacircle(screen, (x + window_center_x), (y + window_center_y), SECOND_TICK_SIZE, second_tick_color)
        pygame.gfxdraw.filled_circle(screen, (x + window_center_x), (y + window_center_y), SECOND_TICK_SIZE, second_tick_color)

    # Draw the remaining ticks
    for i in range(current_second+1, 60):
        x = int((math.sin(2 * math.pi * (i / 60.0))) * SECOND_TICK_RADIUS)
        y = int((-1 * math.cos(2 * math.pi * (i / 60.0))) * SECOND_TICK_RADIUS)
        pygame.gfxdraw.filled_circle(screen, (x + window_center_x), (y + window_center_y), SECOND_TICK_SIZE, second_tick_dimmed_color)

    # Write the time
    text = time_font.render(time.strftime(TIME_FORMAT, now), True, time_color)
    text_pos = text.get_rect()
    text_pos.centerx = window_center_x
    text_pos.centery = window_center_y
    screen.blit(text, text_pos)

    pygame.display.update()

    previous_second = current_second

    # Wait for the next second while handling events for exiting
    while previous_second == current_second:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        now = time.localtime()
        current_second = now.tm_sec
        pygame.time.wait(CHECK_DELAY)
