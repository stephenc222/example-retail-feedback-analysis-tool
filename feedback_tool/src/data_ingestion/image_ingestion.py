import cv2
import numpy as np
from PIL import Image
from src.utils.logging_utils import create_logger


class ImageIngestion:
    def __init__(self):
        self.logger = create_logger(__name__)

    def preprocess_image(self, image_path, target_size=(224, 224)):
        try:
            self.logger.info(f"Reading image from path")
            self.logger.info(image_path)
            img = cv2.imread(image_path)

            if img is None:
                raise ValueError(
                    "Failed to decode image. Check the file path.")

            self.logger.info(f"Original image shape: {img.shape}")

            self.logger.info(f"Resizing image to {target_size}")
            img_resized = cv2.resize(
                img, target_size, interpolation=cv2.INTER_LINEAR)
            self.logger.info(f"Image resized to {img_resized.shape}")

            self.logger.info(f"Normalizing image")
            img_normalized = img_resized.astype(np.float32) / 255.0
            self.logger.info(
                f"Image normalized. Final shape: {img_normalized.shape}")

            # Convert normalized image back to PIL Image format
            img_pil = Image.fromarray((img_normalized * 255).astype(np.uint8))
            self.logger.info("Converted to PIL Image")

            return img_pil

        except Exception as e:
            self.logger.error(f"Error during image preprocessing: {e}")
            raise e
