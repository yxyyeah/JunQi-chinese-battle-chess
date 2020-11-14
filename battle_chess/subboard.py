from board import Board

class LoseBoard(Board):
    def __init__(self,settings,screen):
        super().__init__(settings,screen)

        self.settings = settings

        msg='Not all pieces are unveiled. Are you sure to proceed?'
        self.prep_text(msg)

    def action(self):
        self.settings.game_lose = True
        self.settings.win_music_play = True
        self.settings.game_end = True

class TieBoard(Board):
    def __init__(self,settings,screen):
        super().__init__(settings,screen)

        self.settings = settings

        msg='Do you agree to make a tie?'
        self.no_text = 'No'
        self.prep_text(msg)
    
    def action(self):
        self.settings.game_tie = True
        self.settings.game_end = True