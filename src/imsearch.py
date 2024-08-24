import torch
import faiss
from transformers import AutoImageProcessor, AutoModel
from PIL import Image
import numpy as np

local_directory = "./test/dino"


class ImageSimilarity:
    def __init__(self, model_name, img_arr):
        self.model_name = model_name
        self.images = img_arr
        self.image_paths = []

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = AutoImageProcessor.from_pretrained(local_directory)
        self.model = AutoModel.from_pretrained(local_directory).to(self.device)
        self.index = faiss.IndexFlatL2(384)

    def add_vector_to_index(self, embedding):
        vector = embedding.detach().cpu().numpy()
        vector = np.float32(vector)
        faiss.normalize_L2(vector)
        self.index.add(vector)

    def creating_index(self):
        for image_path in self.images:
            img = Image.open(image_path)
            with torch.no_grad():
                inputs = self.processor(images=img, return_tensors="pt").to(self.device)
                outputs = self.model(**inputs)
            features = outputs.last_hidden_state
            self.add_vector_to_index(features.mean(dim=1))
            self.image_paths.append(image_path)

    def get_image_embedding(self, image_path):
        img = Image.open(image_path)
        with torch.no_grad():
            inputs = self.processor(images=img, return_tensors="pt").to(self.device)
            outputs = self.model(**inputs)
        features = outputs.last_hidden_state.mean(dim=1)
        return features

    def find_similar_images(self, query_image_path, k=5):
        self.creating_index()

        query_embedding = self.get_image_embedding(query_image_path)

        query_vector = query_embedding.detach().cpu().numpy()
        query_vector = np.float32(query_vector)
        faiss.normalize_L2(query_vector)

        distances, indices = self.index.search(query_vector, k)

        similar_image_paths = [self.image_paths[i] for i in indices[0]]

        sorted_results = sorted(
            zip(distances[0], indices[0], similar_image_paths), key=lambda x: x[0]
        )

        sorted_distances, sorted_indices, sorted_paths = zip(*sorted_results)

        return list(sorted_distances), list(sorted_indices), list(sorted_paths)


if __name__ == "__main__":

    model_name = "dino"

    img_arr = [
        "C:\\Users\\User\\Desktop\\MEME\\wallpapers\\arch.png",
        "C:\\Users\\User\\Desktop\\MEME\\wallpapers\\circuit-waifu.png",
        "C:\\Users\\User\\Desktop\\MEME\\wallpapers\\code.png",
        "C:\\Users\\User\\Desktop\\MEME\\wallpapers\\desert.png",
        "C:\\Users\\User\\Desktop\\MEME\\wallpapers\\gruvbox-moon.png",
        "C:\\Users\\User\\Desktop\\MEME\\wallpapers\\ign_unsplash17.png",
        "C:\\Users\\User\\Desktop\\MEME\\wallpapers\\ign_unsplash4.png",
        "C:\\Users\\User\\Desktop\\MEME\\wallpapers\\ign_unsplash5.png",
        "C:\\Users\\User\\Desktop\\bSeGgLCkVQR1Kx82_Badshah-Namdar.jpg",
    ]

    img_sim = ImageSimilarity(model_name, img_arr)

    # Search for similar images
    distances, indices, paths = img_sim.find_similar_images(
        "C:\\Users\\User\\Desktop\\bSeGgLCkVQR1Kx82_Badshah-Namdar.jpg", k=5
    )

    print("Top 5 similar images (from most to least similar):")
    for i, (d, idx, path) in enumerate(zip(distances, indices, paths)):
        print(f"{i+1}. Image index: {idx}, Distance: {d}, Path: {path}")
