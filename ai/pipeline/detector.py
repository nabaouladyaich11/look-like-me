# pipeline/detector.py
import numpy as np
from PIL import Image
from facenet_pytorch import MTCNN
import torch
 
class FaceDetector:
    """
    MTCNN face detector via facenet-pytorch.
    Used for detection + validation only.
    Alignment is handled by DeepFace downstream.
    """
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.mtcnn  = MTCNN(keep_all=True, device=self.device, min_face_size=40)
 
    def detect(self, img_path: str) -> tuple:
        img = Image.open(img_path).convert("RGB")
        return self.mtcnn.detect(img, landmarks=True)
 
    def get_landmarks_array(self, points, face_idx=0) -> np.ndarray:
        return points[face_idx].astype(np.float32)
