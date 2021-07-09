class Reward:
    def __init__(self, reward_id, name, points):
        self.reward_id = reward_id
        self.name = name
        self.points = points

    def get_reward_id(self):
        return self.reward_id

    def get_name(self):
        return self.name

    def get_points(self):
        return self.points

    def set_name(self, name):
        self.name = name

    def set_points(self, points):
        self.points = points

    def set_reward_id(self, reward_id):
        self.reward_id = reward_id
