import collections
import random
import statistics
import time

from opengaze import OpenGazeTracker
from trial_data import trial_data

import numpy as np
import pygame
import pygame.freetype
from enum import Enum
from pygame.sprite import Sprite
from pygame.rect import Rect

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)
fps = 60


def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

class Participant:
    """ Stores information about a participant """

    def __init__(self, score=0, lives=3, current_level=1):
        self.score = score
        self.lives = lives
        self.current_level = current_level


class myApp():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1920, 1080))
        self.clock = pygame.time.Clock()
        self.game_state = GameState.TITLE
        self.td = trial_data()

        # Open the connection to the tracker.
        self.tracker = OpenGazeTracker(ip="130.63.209.52", logfile="hi", debug=False)



        self.groupOrder = [["Touch", "Eye Tracking without Bounding Box", "Eye Tracking with Bounding Box"],
                      ["Touch", "Eye Tracking with Bounding Box", "Eye Tracking without Bounding Box"],
                      ["Eye Tracking without Bounding Box", "Touch", "Eye Tracking with Bounding Box"],
                      ["Eye Tracking without Bounding Box", "Eye Tracking with Bounding Box" ,"Touch"],
                      [ "Eye Tracking with Bounding Box", "Touch", "Eye Tracking without Bounding Box",],
                      [ "Eye Tracking with Bounding Box", "Eye Tracking without Bounding Box", "Touch"]]


    def main(self):

        while True:
            if self.game_state == GameState.TITLE:
                print("ENTERING")
                name, group, self.game_state = self.game_loop()
                print("HERE", name, group, self.game_state)

            if self.game_state == GameState.NEWGAME:
               # self.performCalibration()
                print("CALIBRATION FINISHES")
                for methodNum in range(3):
                    if(group >= 1):
                        method = self.groupOrder[group - 1][methodNum]
                        scenes = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                        #scenes = [2]
                        random.shuffle(scenes)
                    else:
                        method = self.groupOrder[0][methodNum]
                        scenes = [11,12]

                    self.game_state = self.displayText(method, delay=10)

                    for sceneNum in scenes:
                        self.performExperiment(sceneNum, method)
                    print("EXITING NEW GAME")

                self.preference, self.easeOfUse, _= self.get_preference()
                self.game_state = GameState.QUIT

            if self.game_state == GameState.NEXT_LEVEL:
                print("ENTERING NEXT LEVEL")

                self.game_state = GameState.NEWGAME
                print("EXITING NEXT LEVEL")


            if self.game_state == GameState.QUIT:
                filename = f"{name}_{group}_{self.preference}_{self.easeOfUse}_{time.time_ns()}.csv"
                self.td.trial_data_out(filename)
                pygame.quit()
                return





    def game_loop(self):
        """ Handles game loop until an action is return by a button in the
            buttons sprite renderer.
        """

        font = pygame.font.SysFont(None, 100)
        text = ""
        text_surf = font.render(text, True, (255, 255, 255))
        name = ""
        group = ""
        nameAcquired = False
        groupAcquired = False
        while not nameAcquired or not groupAcquired:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if not nameAcquired:
                            name = text
                            text = ""
                            nameAcquired = True
                        else:
                            group = int(text)
                            if(group <= 6 and group >= 0):
                                groupAcquired = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
            if not nameAcquired:
                text_surf = font.render("Enter Name: {}".format(text), True, (255, 255, 255))
            else:
                text_surf = font.render("Enter Group: {}".format(text), True, (255, 255, 255))
            self.screen.fill(BLUE)


            self.screen.blit(text_surf, text_surf.get_rect(center=self.screen.get_rect().center))

            pygame.display.flip()
        return name, group, GameState.NEWGAME

    def displayText(self, text, delay = 1):
        """ Handles game loop until an action is return by a button in the
            buttons sprite renderer.
        """
        font = pygame.font.SysFont(None, 100)

        #this is a delay of 1 sec
        for i in range (delay*fps):
            mouse_up = False
            for event in pygame.event.get():
                pass
            text_surf = font.render(text, True, (255, 255, 255))
            self.screen.fill(BLUE)


            self.screen.blit(text_surf, text_surf.get_rect(center=self.screen.get_rect().center))

            pygame.display.flip()
            self.clock.tick(fps)

    def performCalibration(self):
        # Calibrate the tracker.
        self.tracker.calibrate()


    def performExperiment(self, sceneNum, method = "Touch"):
        """ Handles game loop until an action is return by a button in the
            buttons sprite renderer.
        """
        words = ["Red House", "Rhino",  "Face", "Dinosaur", "Face", "Face", "Face",  "Minion", "Minion", "EMPTY", "Face", "Minion"]

        self.displayText(words[sceneNum-1], delay=2)
        #TOODODO
        #these are locations into the sharpness map
        gt_x_list = [1276, 358, 147,1168,198, 1195, 1130,598, 312, 0,386, 827]
        gt_y_list = [334, 440, 170,293 ,256, 260, 265,457, 463, 0, 162, 462]
        img_all = np.load(f"data/Scene{sceneNum}_images.npy")
        img_all = np.swapaxes(img_all, 1, 2)

        max_sharpness_map = np.load(f"data/Scene{sceneNum}_max_sharpness_map.npy")
        max_sharpness_map = np.swapaxes(max_sharpness_map, 0, 1)
        sharpness_map = np.load(f"data/Scene{sceneNum}_sharpness_map.npy")
        sharpness_map = np.swapaxes(sharpness_map, 1, 2)
        gt_x = gt_x_list[sceneNum-1]
        gt_y = gt_y_list[sceneNum-1]

        gt_x_m = np.clip(gt_x - 50, 0, 1500 - 100)
        gt_y_m = np.clip(gt_y - 50, 0, 843 - 100)


        gt_index = max_sharpness_map[gt_x_m, gt_y_m]
        #print("GT INDEX", gt_index, "gt_x_m", "gt_y_m", gt_x_m, gt_y_m)

        surfs = []
        for img in img_all:
            surfs.append(pygame.surfarray.make_surface(img))

        pygame.display.update()
        prev_sharpness = collections.deque(maxlen=5)
        prev_index = collections.deque(maxlen=5)


        completed = False

        pygame.mouse.set_visible(False) #hide cursor

        self.tracker.start_recording()


        #set mouse position to top left corner

        xoffset = 200
        yoffset = 100

        shutter_x = 1800
        shutter_y = 496
        raidus = 75
        #NUMS WERE LIKE 400 and 200 - 200 Im sure
        if(method == "Touch"):
            pygame.mouse.set_pos(xoffset+750,yoffset+421)
            pygame.draw.circle(self.screen, (255, 255, 255), (1800, 496), 75, 0)
        else:
            pygame.mouse.set_pos(0,0)
        current_index = max_sharpness_map[750,421]

        x = 0
        y = 0
        x_eye = 0
        y_eye = 0
        x_eye_buffer = collections.deque(maxlen=60)
        y_eye_buffer = collections.deque(maxlen=60)

        var_threshold = 1500
        dwell_steps = 80
        x_eye_dwell_buffer = collections.deque(maxlen=dwell_steps)
        y_eye_dwell_buffer = collections.deque(maxlen=dwell_steps)
        while not completed:
            for event in pygame.event.get():
                pass

            x_eye_new, y_eye_new = self.tracker.sample()

            if (x_eye_new is not None and y_eye_new is not None):
                x_eye_new = int(x_eye_new * 1920)
                y_eye_new = int(y_eye_new * 1080)
                x_eye_buffer.append(x_eye_new)
                y_eye_buffer.append(y_eye_new)

                x_eye_dwell_buffer.append(x_eye_new)
                y_eye_dwell_buffer.append(y_eye_new)

                x_eye = int(statistics.mean(x_eye_buffer))
                y_eye = int(statistics.mean(y_eye_buffer))




            if method != "Touch":
                if (x_eye_new is not None and y_eye_new is not None):
                    x = x_eye
                    y = y_eye

                if (len(x_eye_dwell_buffer) == dwell_steps):
                    x_var = statistics.variance(x_eye_dwell_buffer)
                    y_var = statistics.variance(y_eye_dwell_buffer)
                    avg_var = 0.5 * (x_var + y_var)

                    print("AVG VAR", avg_var)

                    if avg_var < var_threshold:
                        completed = True

            else:
                x_t, y_t = pygame.mouse.get_pos()
                d = (x_t-shutter_x)**2 + (y_t-shutter_y)**2
                if d < raidus**2:
                    completed=True
                else:
                    x,y = x_t,y_t

            x_m = np.clip(x - 50, xoffset, 1500 + xoffset- 100)
            y_m = np.clip(y - 50, yoffset, 843 + yoffset - 100)

            x_im = x_m - xoffset
            y_im = y_m - yoffset
            best_index = max_sharpness_map[x_im, y_im]
            best_index = best_index + random.randint(-4, 4)

            best_index = min(best_index, 49)
            best_index = max(best_index, 0)

            if (abs(current_index - best_index) > 4):
                diff = current_index - best_index
                if (diff > 0):
                    current_index -= 1
                elif (diff < 0):
                    current_index += 1
                current_index = min(current_index, 49)
                current_index = max(current_index, 0)

            current_sharpness = sharpness_map[current_index, x_im, y_im]
            prev_sharpness.append(current_sharpness)
            prev_index.append(current_index)


            self.screen.blit(surfs[current_index], (xoffset,yoffset))

            if(method != "Eye Tracking without Bounding Box"):
                pygame.draw.rect(self.screen, (255, 255, 0), (x_m, y_m, 100, 100), 5)

            font1 = pygame.font.SysFont(None, 30)
            #text = font1.render( 'Sharpness: {}, Current Index: {}, best_index: {}, x:{}, y:{}'.format(current_sharpness, current_index, best_index,x_m,y_m), True, BLUE, (255, 255, 255))
            #print(x_m, y_m)
            #self.screen.blit(text, (0, 0))
            self.td.addDataPoint(method=method, scene=sceneNum, objectword= words[sceneNum-1],
                                 x_eye = x_eye, y_eye = y_eye, x_im = x_im, y_im = y_im, best_index=best_index,
                                 current_index= current_index, best_sharpness=sharpness_map[best_index, x_im, y_im],
                                 current_sharpness=current_sharpness, gt_index=gt_index, gt_sharpness=sharpness_map[gt_index, gt_x, gt_y],
                                 gt_x=gt_x, gt_y = gt_y, completed=completed)
            pygame.display.flip()
            self.clock.tick(125)
        return GameState.NEWGAME
    def get_preference(self):
        """ Handles game loop until an action is return by a button in the
            buttons sprite renderer.
        """

        font = pygame.font.SysFont(None, 100)
        linefont = pygame.font.SysFont(None, 30)
        text = ""
        text_surf = font.render(text, True, (255, 255, 255))

        self.groupOrder = [["Touch", "Eye Tracking without Bounding Box", "Eye Tracking with Bounding Box"],
                      ["Touch", "Eye Tracking with Bounding Box", "Eye Tracking without Bounding Box"], #BCA
                      ["Eye Tracking without Bounding Box", "Touch", "Eye Tracking with Bounding Box"], #ABC
                      ["Eye Tracking without Bounding Box", "Eye Tracking with Bounding Box" ,"Touch"],
                      [ "Eye Tracking with Bounding Box", "Touch", "Eye Tracking without Bounding Box",],
                      [ "Eye Tracking with Bounding Box", "Eye Tracking without Bounding Box", "Touch"]]#CAB
        line1_surf = linefont.render("1. Touch, Eye Tracking without Bounding Box, Eye Tracking with Bounding Box", True, (255, 255, 255))
        line2_surf = linefont.render("2. Touch, Eye Tracking with Bounding Box, Eye Tracking without Bounding Box", True, (255, 255, 255))
        line3_surf = linefont.render("3. Eye Tracking without Bounding Box, Touch, Eye Tracking with Bounding Box", True, (255, 255, 255))
        line4_surf = linefont.render("4. Eye Tracking without Bounding Box, Eye Tracking with Bounding Box, Touch", True, (255, 255, 255))
        line5_surf = linefont.render("5. Eye Tracking with Bounding Box, Touch, Eye Tracking without Bounding Box", True, (255, 255, 255))
        line6_surf = linefont.render("6. Eye Tracking with Bounding Box, Eye Tracking without Bounding Box, Touch", True, (255, 255, 255))
        preference = ""
        easeOfUse = ""
        preferenceAcquired = False
        easeOfUseAcquired = False
        while not preferenceAcquired or not easeOfUseAcquired:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if not preferenceAcquired:
                            try:
                                preference = int(text)
                                if (preference <= 6 and preference >= 1):
                                    preferenceAcquired = True
                            except:
                                print("Bad input")


                        else:
                            try:
                                easeOfUse = int(text)
                                if (easeOfUse <= 6 and easeOfUse >= 1):
                                    easeOfUseAcquired = True
                            except:
                                print("Bad input")


                        text= ""
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
            if not preferenceAcquired:
                text_surf = font.render("Order the methods in terms of preference: {}".format(text), True, (255, 255, 255))
            else:
                text_surf = font.render("Order the methods in terms of ease of use: {}".format(text), True, (255, 255, 255))
            print("TEXT", text)
            self.screen.fill(BLUE)

            self.screen.blit(text_surf, text_surf.get_rect(center=self.screen.get_rect().center))

            self.screen.blit(line1_surf, (0,0))
            self.screen.blit(line2_surf, (0, 50))
            self.screen.blit(line3_surf, (0, 100))
            self.screen.blit(line4_surf, (0, 150))
            self.screen.blit(line5_surf, (0, 200))
            self.screen.blit(line6_surf, (0, 250))

            pygame.display.flip()
        return preference, easeOfUse, GameState.NEWGAME

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    NEXT_LEVEL = 2


if __name__ == "__main__":
    ma = myApp()
    ma.main()