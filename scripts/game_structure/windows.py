from pygame_gui.elements import UIWindow
import pygame
import pygame_gui
from sys import exit

from scripts.game_structure.image_button import UIImageButton, UITextBoxTweaked
from scripts.utility import scale
from scripts.game_structure.game_essentials import game

class SaveCheck(UIWindow):
    def __init__(self, last_screen, isMainMenu, mm_btn):
        print("Save Check Window Opened")
        if game.is_close_menu_open:
            print("Save Check Window already open")
            return
        game.is_close_menu_open = True
        super().__init__(scale(pygame.Rect((500, 400), (600, 400))),
                         window_display_title='Save Check',
                         object_id='#save_check_window',
                         resizable=False)
        self.clan_name = str(game.clan.name + 'Clan')
        self.last_screen = last_screen
        self.isMainMenu = isMainMenu
        self.mm_btn = mm_btn
        
        if(self.isMainMenu):
            self.mm_btn.disable()
            self.main_menu_button = UIImageButton(
                scale(pygame.Rect((146, 310), (305, 60))),
                "",
                object_id="#main_menu_button",
                container=self
        )
            self.message = f"Would you like to save your game before exiting to the Main Menu? If you don't, progress may be lost!"
        else:
            self.main_menu_button = UIImageButton(
                scale(pygame.Rect((146, 310), (305, 60))),
                "",
                object_id="#smallquit_button",
                container=self
        )
            self.message = f"Would you like to save your game before exiting? If you don't, progress may be lost!"

        self.game_over_message = UITextBoxTweaked(
            self.message,
            scale(pygame.Rect((40, 40), (520, -1))),
            line_spacing=1,
            object_id="",
            container=self
        )

        self.save_button = UIImageButton(
            scale(pygame.Rect((186, 230), (228, 60))),
            "",
            object_id="#save_button",
            container=self
        )

        self.save_text = pygame_gui.elements.UITextBox("<font color=#006600>Saved!</font>",
                                                       scale(pygame.Rect((0, 170), (600, 80))),
                                                       object_id="#save_no_bg_text_box",
                                                       container=self)
        self.save_text.hide()

        self.back_button = UIImageButton(
            scale(pygame.Rect((5, 10), (50, 50))),
            "",
            object_id="#exit_window_button",
            container=self
        )

        self.back_button.enable()
        self.main_menu_button.enable()
        self.save_button.enable()


    def process_event(self, event):
        super().process_event(event)

        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.main_menu_button:
                if self.isMainMenu:
                    game.is_close_menu_open = False
                    self.mm_btn.enable()
                    game.last_screen_forupdate = game.switches['cur_screen']
                    game.switches['cur_screen'] = 'start screen'
                    game.switch_screens = True
                    self.kill()
                else:
                    game.is_close_menu_open = False
                    game.rpc.close()
                    pygame.display.quit()
                    pygame.quit()
                    exit()
            elif event.ui_element == self.save_button:
                if game.clan is not None:
                    game.save_cats()
                    game.clan.save_clan()
                    game.clan.save_pregnancy(game.clan)
                    self.save_text.show()
                    self.save_button.disable()
            elif event.ui_element == self.back_button:
                game.is_close_menu_open = False
                self.kill()
                if self.isMainMenu:
                    self.mm_btn.enable()


                # only allow one instance of this window
                
                

class GameOver(UIWindow):
    def __init__(self, last_screen):
        super().__init__(scale(pygame.Rect((500, 400), (600, 360))),
                         window_display_title='Game Over',
                         object_id='#game_over_window',
                         resizable=False)
        self.clan_name = str(game.clan.name + 'Clan')
        self.last_screen = last_screen
        self.game_over_message = UITextBoxTweaked(
            f"{self.clan_name} has died out. For now, this is where their story ends. Perhaps it's time to tell a new "
            f"tale?",
            scale(pygame.Rect((40, 40), (520, -1))),
            line_spacing=1,
            object_id="",
            container=self
        )

        self.game_over_message = UITextBoxTweaked(
            f"(leaving will not erase the save file)",
            scale(pygame.Rect((40, 310), (520, -1))),
            line_spacing=.8,
            object_id="#cat_patrol_info_box",
            container=self
        )

        self.begin_anew_button = UIImageButton(
            scale(pygame.Rect((50, 230), (222, 60))),
            "",
            object_id="#begin_anew_button",
            container=self
        )
        self.not_yet_button = UIImageButton(
            scale(pygame.Rect((318, 230), (222, 60))),
            "",
            object_id="#not_yet_button",
            container=self
        )

        self.not_yet_button.enable()
        self.begin_anew_button.enable()

    def process_event(self, event):
        super().process_event(event)

        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.begin_anew_button:
                game.last_screen_forupdate = game.switches['cur_screen']
                game.switches['cur_screen'] = 'start screen'
                game.switch_screens = True
                self.kill()
            elif event.ui_element == self.not_yet_button:

                self.kill()
