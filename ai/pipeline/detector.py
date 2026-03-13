# pipeline/detector.py
import numpy as np
from PIL import Image
from facenet_pytorch import MTCNN
import torch


class FaceDetector:
    """
    MTCNN face detector via facenet-pytorch.
    Pure PyTorch — no TensorFlow or Keras required.
    Returns bounding boxes, confidence scores, and 5 facial landmarks.
    """

    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.mtcnn = MTCNN(
            keep_all=True,          # detect all faces (we validate count after)
            device=self.device,
            min_face_size=40,       # ignore faces smaller than 40px
        )

    def detect(self, img_path: str) -> tuple:
        """
        Args:
            img_path : path to image file (JPEG / PNG / WebP)
        Returns:
            boxes  : numpy array of shape (N, 4)  — bounding boxes
            probs  : numpy array of shape (N,)    — confidence scores
            points : numpy array of shape (N, 5, 2) — landmarks
            Returns (None, None, None) if no face is detected.
        """
        img = Image.open(img_path).convert('RGB')
        boxes, probs, points = self.mtcnn.detect(img, landmarks=True)
        return boxes, probs, points

    def get_landmarks_array(self, points, face_idx: int = 0) -> np.ndarray:
        """
        Extracts 5 landmarks for a single face as a numpy array.

        Order: left_eye, right_eye, nose, mouth_left, mouth_right
        This matches exactly the AdaFace dst_landmarks template order.

        Args:
            points   : full points array from detect() — shape (N, 5, 2)
            face_idx : index of the face to extract (default 0 = first face)
        Returns:
            numpy array of shape (5, 2)
        """
        return points[face_idx].astype(np.float32)
