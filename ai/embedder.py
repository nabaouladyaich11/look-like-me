# embedder.py
import numpy as np, cv2
from deepface import DeepFace
import warnings; warnings.filterwarnings("ignore")
 
class FaceEmbedder:
    """
    Extracts L2-normalized (4096,) embedding from 224x224 RGB face crop.
    Uses VGG-Face via DeepFace.
    """
    MODEL_NAME = "VGG-Face"
 
    def __init__(self):
        print(f"Loading {self.MODEL_NAME} model...")
        dummy = np.zeros((224, 224, 3), dtype=np.uint8)
        try:
            DeepFace.represent(img_path=dummy, model_name=self.MODEL_NAME,
                               enforce_detection=False, detector_backend="skip")
            print(f"{self.MODEL_NAME} model loaded.")
        except Exception as e:
            raise RuntimeError(f"Failed to load {self.MODEL_NAME}: {e}") from e
            # ↑ was: silent "except Exception: pass" — now surfaces immediately
 
    def embed(self, face_rgb: np.ndarray) -> np.ndarray:
        """
        Args:   face_rgb : 224x224 RGB array from Phase1Result.face_crop
        Returns: L2-normalized numpy array of shape (4096,)
        """
        if face_rgb.shape != (224, 224, 3):
            raise ValueError(f"Expected (224,224,3), got {face_rgb.shape}")
        result = DeepFace.represent(
            img_path=face_rgb, model_name=self.MODEL_NAME,
            enforce_detection=False, detector_backend="skip",
        )
        emb  = np.array(result[0]["embedding"], dtype=np.float32)
        norm = np.linalg.norm(emb)
        return emb / norm if norm > 0 else emb  # shape (4096,)
