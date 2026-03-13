# pipeline/aligner.py  — no changes needed from the original version
import numpy as np
import cv2
from skimage.transform import SimilarityTransform


# AdaFace fixed reference landmarks (112x112 template) — do NOT modify
ADAFACE_DST = np.array([
    [30.2946, 51.6963],   # Left Eye
    [65.5318, 51.5014],   # Right Eye
    [48.0252, 71.7366],   # Nose Tip
    [33.5493, 92.3655],   # Left Mouth Corner
    [62.7299, 92.2041],   # Right Mouth Corner
], dtype=np.float32)


class FaceAligner:
    """
    Aligns a face to 112x112 using Similarity Transform.
    Reference coordinates from the official AdaFace alignment code.
    """

    def align(self, img_bgr: np.ndarray, src_landmarks: np.ndarray) -> np.ndarray:
        """
        Args:
            img_bgr       : full BGR image loaded by OpenCV
            src_landmarks : numpy array of shape (5, 2) from MTCNN
        Returns:
            aligned_bgr   : aligned BGR face image, size 112x112
        """
        tform = SimilarityTransform()
        tform.estimate(src_landmarks, ADAFACE_DST)

        aligned = cv2.warpAffine(
            img_bgr,
            tform.params[0:2],
            (112, 112),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_REPLICATE,
        )
        return aligned
