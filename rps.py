import random
class RPS():
    def __init__(self, user_choice: str):
        self.user_choice = user_choice
        self.bot_choices()
        self.game()
        self.winer_str()

    def bot_choices(self):
        self.bot_choice = ['سنگ','کاغذ','قیچی'][random.randint(0,2)]

    def game(self):
        self.win_status = {
            ('سنگ', 'کاغذ'): -1,
            ('سنگ', 'قیچی'): 1,
            ('سنگ', 'سنگ'): 0,
            ('کاغذ', 'کاغذ'): 0,
            ('کاغذ', 'قیچی'): -1,
            ('کاغذ', 'سنگ'): 1,
            ('قیچی','کاغذ'):1,
            ('قیچی','قیچی'): 0,
            ('قیچی', 'سنگ'):-1,
        }[(self.user_choice, self.bot_choice)]

    def winer_str(self):
        self.winer_string = {
            -1: 'من بردم. 😜',
            1: 'تو بردی. 😠',
            0: 'مساوی شدیم. 😮',
        }[self.win_status]