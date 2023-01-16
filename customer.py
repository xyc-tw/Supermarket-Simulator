import random
import numpy as np
import cv2

IMAGE_TILES = cv2.imread("tiles.png")
AVATAR_LIST = [(3,0),(3,1),(3,2),(4,0),(4,1),(4,2),(5,0),(5,1),(5,2),(6,0),(6,1),(6,2),(7,0),(7,1),(7,2),(8,1),(8,2)] 

class Customer:
    """
    This is a Customer class
    """
    def __init__(self, id, location_dic):
        """
        Class constructor
        """
        self.id = id
        self.state = 'entrance'

        # for plotting
        self.pos_row = None
        self.pos_col = None
        self.avatar = np.zeros((32, 32, 3), dtype=np.uint8)
        self.location_dic = location_dic
        self.move_to("entrance")
        self.prepare_avatar()

    def __repr__(self):
        """
        Class representation
        """
        return f'Customer {self.id} in {self.state} state.'

    def prepare_avatar(self):
        avatar_image = random.choice(AVATAR_LIST)
        row = avatar_image[0]
        col = avatar_image[1]
        x = row * 32
        y = col * 32
        self.avatar = IMAGE_TILES[x:x+32, y:y+32]

    def update_state(self, trans_matrix):
        state_list = list(trans_matrix.keys())
        next_state = random.choices(state_list, weights=trans_matrix[self.state])[0]
        self.state = next_state

    def move_to(self, location):
        positions = self.location_dic[location]
        position = random.choice(positions)
        self.pos_col = position[1]
        self.pos_row = position[0]

    def draw(self, canvas):
        x = self.pos_col * 32
        y = self.pos_row * 32
        canvas[x:x+32, y:y+32] = self.avatar
        
