import pygame
import GameV2.constants as constants

class Menu():
    # If sizes are given, must provide positions as well otherwise could be overlap
    def __init__(self, screen, text, contains_title, y_pos=None, size=None, font=None, colour=None, background=None, x_pos=None):
        self.screen = screen
        self.text = text
        self.contains_title = contains_title
        self.y_pos = y_pos
        self.size = size
        self.fontFiles = font
        self.colour = colour
        self.background = background
        self.x_pos = x_pos

        if not self.size:
            self.size = [constants.DEFAULT_FONT_SIZE for i in range(len(text))]
            if self.contains_title:
                self.size[0] = constants.TITLE_FONT_SIZE
            else:
                self.size[0] = constants.SELECTED_FONT_SIZE
        if not self.y_pos:
            total_height = sum(self.size) + 10* len(self.size)
            start_text_height = constants.HEIGHT // 2 - total_height // 2 - self.size[0] // 2
            self.y_pos = [start_text_height + i * self.size[i] + 10 for i in range(len(text))]
        if not self.fontFiles:
            self.fontFiles = ["fonts/miami.ttf" for i in range(len(text))]
        if not self.colour:
            self.colour = [constants.BLACK for i in range(len(text))]
        
        self.font = [pygame.font.Font(self.fontFiles[i], self.size[i]) for i in range(len(text))]
        self.text_obj = [self.font[i].render(text[i], True, colour[i]) for i in range(len(text))]

        if not self.x_pos:
            self.x_pos = [constants.WIDTH // 2 - self.text_obj[i].get_width for i in range(len(text))]

        self.display = True
        self.selected = 0

        if self.contains_title:
            self.selected = 1

    
    def displayMenu(self):
        while self.display:
            if self.background:
                self.screen.blit(self.background, (0,0))
            else:
                self.screen.fill(constants.WHITE)
                
            for i in range(len(self.text_obj)):
                self.screen.blit(self.text_obj[i], (self.x_pos[i], self.y_pos[i]))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.text)
                        if (self.contains_title and self.selected == 0):
                            self.selected += 1
                    elif event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.text)
                        if (self.contains_title and self.selected == 0):
                            self.selected += 1
                    elif event.key == pygame.K_RETURN:
                        return self.selected
            pygame.display.flip()
        
