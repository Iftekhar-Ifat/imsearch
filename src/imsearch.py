from PIL import Image
import numpy as np
import gc
from contextlib import contextmanager


class ImageSimilarity:
    def __init__(self, model_name, img_arr):
        self.model_name = model_name
        self.images = img_arr
        self.image_paths = []
        self.device = None
        self.embedding_size = 384 if model_name == "DINO" else 1280
        self.index = None
        self.processor = None
        self.model = None

    def __del__(self):
        self.release_memory()

    def release_memory(self):
        self.model = None
        self.processor = None
        self.index = None
        self.image_paths = []
        gc.collect()

    @contextmanager
    def memory_manager(self):
        try:
            yield self
        finally:
            self.release_memory()

    def _get_device(self):
        if self.device is None:
            import torch

            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        return self.device

    def _load_dino(self):
        from transformers import AutoImageProcessor, AutoModel

        self.processor = AutoImageProcessor.from_pretrained("./models/dino")
        self.model = AutoModel.from_pretrained("./models/dino").to(self._get_device())

    def _load_mobilenet(self):
        import torch
        from torchvision import models, transforms

        self.model = models.mobilenet_v2()
        state_dict = torch.load(
            "./models/mobilenet/mobilenet_v2-b0353104.pth",
            map_location=self._get_device(),
        )
        self.model.load_state_dict(state_dict)
        self.model.to(self._get_device())
        self.model.eval()
        self.processor = transforms.Compose(
            [
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )

    def get_model_and_processor(self):
        if self.model is None or self.processor is None:
            if self.model_name == "DINO":
                self._load_dino()
            elif self.model_name == "MOBILE_NET":
                self._load_mobilenet()
            else:
                raise ValueError(f"Unsupported model: {self.model_name}")
        return self.model, self.processor

    def add_vector_to_index(self, embedding):
        import faiss

        if self.index is None:
            self.index = faiss.IndexFlatL2(self.embedding_size)
        vector = embedding.detach().cpu().numpy()
        vector = np.float32(vector)
        if vector.ndim == 1:
            vector = vector.reshape(1, -1)
        faiss.normalize_L2(vector)
        self.index.add(vector)

    def get_image_embedding(self, img, model, processor):
        import torch

        if self.model_name == "DINO":
            with torch.no_grad():
                inputs = processor(images=img, return_tensors="pt").to(
                    self._get_device()
                )
                outputs = model(**inputs)
            features = outputs.last_hidden_state.mean(dim=1).squeeze(0)
        elif self.model_name == "MOBILE_NET":
            img_tensor = processor(img).unsqueeze(0).to(self._get_device())
            with torch.no_grad():
                features = model.features(img_tensor).mean([2, 3]).squeeze(0)
        else:
            raise ValueError(f"Unsupported model: {self.model_name}")
        return features

    def find_similar_images(self, query_image_path, k=5):
        import faiss

        if self.index is None:
            self.creating_index()

        model, processor = self.get_model_and_processor()
        query_img = Image.open(query_image_path).convert("RGB")
        query_embedding = self.get_image_embedding(query_img, model, processor)

        query_vector = query_embedding.detach().cpu().numpy()
        query_vector = np.float32(query_vector)
        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)
        faiss.normalize_L2(query_vector)

        distances, indices = self.index.search(query_vector, k)

        similar_image_paths = [self.image_paths[i] for i in indices[0]]

        sorted_results = sorted(
            zip(distances[0], indices[0], similar_image_paths), key=lambda x: x[0]
        )
        sorted_distances, sorted_indices, sorted_paths = zip(*sorted_results)

        return list(sorted_distances), list(sorted_indices), list(sorted_paths)

    def creating_index(self):
        model, processor = self.get_model_and_processor()

        for image_path in self.images:
            img = Image.open(image_path).convert("RGB")
            features = self.get_image_embedding(img, model, processor)
            self.add_vector_to_index(features)

        self.image_paths = self.images


""" if __name__ == "__main__":
    model_name = "DINO"

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
        "C:\\Users\\User\\Desktop\\bSeGgLCkVQR1Kx82_Badshah-Namdar.jpg", k=len(img_arr)
    )

    print("Top 5 similar images (from most to least similar):")
    for i, (d, idx, path) in enumerate(zip(distances, indices, paths)):
        print(f"{i+1}. Image index: {idx}, Distance: {d}, Path: {path}")
 """
