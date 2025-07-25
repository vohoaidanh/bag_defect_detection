import numpy as np
import uuid
import time

class ImageWithMeta:
    def __init__(self, image: np.ndarray):
        self.image = image
        self.timestamp = time.time()
        self.id = str(uuid.uuid4()) 
