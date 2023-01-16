import numpy as np
import cv2

TILE_SIZE = 32

WHITE_TILE = np.full((32, 32, 3), 255,dtype='uint8')
GRAY_TILE = np.full((32, 32, 3), 160,dtype='uint8')
GRAY_LINE_TILE = np.full((32, 32, 3), 160,dtype='uint8')
GRAY_LINE_TILE[:,30:,:] = [80,80,80]
BLACK_TILE = np.zeros((32, 32, 3), np.uint8)

GATE_TILE = np.zeros((32, 32, 3), np.uint8)
GATE_TILE[15:18,:,:] = [255,204,153]

BLUE_TILE = np.full((32, 32, 3), [204,102,0],dtype='uint8') #BGR
# BLUE_TILE = np.full((32, 32, 3), [0,102,204],dtype='uint8') #RGB

SHELF_TILE = np.full((32, 32, 3), [255,204,153],dtype='uint8') #BGR
SHELF_LEFT_TILE = np.full((32, 32, 3), [255,204,153],dtype='uint8') #BGR
SHELF_LEFT_TILE[:,30:,:] = [204,102,0]

class SupermarketMap:
    """Visualizes the supermarket background"""

    def __init__(self, layout):
        """
        layout : a string with each character representing a tile
        tiles   : a numpy array containing all the tile images
        """
        # split the layout string into a two dimensional matrix
        self.contents = [list(row) for row in layout.split("\n")]
        self.ncols = len(self.contents[0])
        self.nrows = len(self.contents)

        # set background of image
        self.image = np.zeros(
            (self.nrows*TILE_SIZE, self.ncols*TILE_SIZE, 3), dtype=np.uint8
        )

        self.prepare_map()

    def get_color(self, char):
        """returns the array for a given tile character"""
        if char == "#":
            return SHELF_TILE
        elif char == "L":
            return SHELF_LEFT_TILE
        elif char == "G":
            return GATE_TILE
        elif char == "C":
            return GRAY_TILE
        elif char == "D":
            return GRAY_LINE_TILE
        elif char == "W":
            return BLUE_TILE
        elif char == "B":
            return BLACK_TILE
        else:
            return BLACK_TILE

    def prepare_map(self):
        """prepares the entire image as a big numpy array"""
        for row, line in enumerate(self.contents):  #two dimensional matrix
            for col, char in enumerate(line):
                bm = self.get_color(char)
                y = row*TILE_SIZE
                x = col*TILE_SIZE
                self.image[y:y+TILE_SIZE, x:x+TILE_SIZE] = bm

    def draw(self, canvas):
        """
        draws the image into a frame
        """
        canvas[0:self.image.shape[0], 0:self.image.shape[1]] = self.image

    def write_image(self, filename):
        """writes the image into a file"""
        cv2.imwrite(filename, self.image)