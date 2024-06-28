import os
import glob


class GetImages:
    def __init__(self, directory, extensions=("*.jpg", "*.jpeg", "*.png")):
        self.directory = directory
        self.extensions = extensions

    def get_images(self):
        images = []
        for ext in self.extensions:
            images.extend(glob.glob(os.path.join(self.directory, ext)))
        return images
