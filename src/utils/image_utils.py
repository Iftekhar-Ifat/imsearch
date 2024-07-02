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

    def get_nested_images(self):
        images = []
        for root, _, _ in os.walk(self.directory):
            for ext in self.extensions:
                images.extend(glob.glob(os.path.join(root, ext)))
        return images
