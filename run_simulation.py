from supermarket import Supermarket
from datetime import datetime
import numpy as np
import cv2

from supermarket_variable import MARKET_LAYOUT, LOCATIONS_DIC, PROBS, NEW_MEAN, NEW_STDDEV
STATE_LIST = list(PROBS.keys())

CANVAS = np.zeros((608, 640, 3), np.uint8)

sup_test = Supermarket(datetime.now(), 10, PROBS, NEW_MEAN, NEW_STDDEV, LOCATIONS_DIC, MARKET_LAYOUT, CANVAS)
sup_test.run_simulation()
