class StartupInfo:

    money_taken_local = ""
    money_taken_USD = ""
    planned_money_local = ""
    planned_money_USD = ""
    backers = ""
    updates = ""
    comments = 0
    has_video = False
    author_created_number = ""
    author_backed_number = ""
    author_registration_date = ""
    rewards_num = 0
    lowest_reward = 0
    highest_reward = 0

    def __str__(self):
        
        startup_str = ""
        startup_str += self.money_taken_local + ";"
        startup_str += self.money_taken_USD + ";"
        startup_str += self.planned_money_local + ";"
        startup_str += self.planned_money_USD + ";"
        startup_str += self.backers + ";"
        startup_str += self.updates + ";"
        startup_str += str(self.comments) + ";"
        startup_str += str(int(self.has_video)) + ";"
        startup_str += self.author_created_number + ";"
        startup_str += self.author_backed_number + ";"
        startup_str += self.author_registration_date + ";"
        startup_str += str(self.rewards_num) + ";"
        startup_str += str(self.lowest_reward) + ";"
        startup_str += str(self.highest_reward)

        return startup_str