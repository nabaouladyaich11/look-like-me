# pipeline/phase1.py
from dataclasses import dataclass
from typing import Optional
import numpy as np
import cv2

from .detector  import FaceDetector
from .validator import FaceValidator
from .aligner   import FaceAligner


@dataclass
class Phase1Result:
    success:      bool
    message:      str
    aligned_face: Optional[np.ndarray] = None   # BGR 112x112
    landmarks:    Optional[np.ndarray] = None   # shape (5, 2)
    confidence:   Optional[float]      = None


class Phase1Pipeline:
    """
    Complete Phase 1: Input -> Detection -> Validation -> Alignment.
    Uses MTCNN (facenet-pytorch) — pure PyTorch, no TensorFlow.
    Output: aligned BGR face at 112x112, ready for AdaFace.
    """

    def __init__(self):
        self.detector  = FaceDetector()
        self.validator = FaceValidator()
        self.aligner   = FaceAligner()

    def run(self, img_path: str) -> Phase1Result:
        """
        Runs the full Phase 1 pipeline on a single image.

        Args:
            img_path : path to the input image
        Returns:
            Phase1Result with success=True and aligned_face,
            or success=False with an error message.
        """

        # Stage 1: Face Detection
        boxes, probs, points = self.detector.detect(img_path)

        # Stage 2: Validation
        validation = self.validator.validate(boxes, probs)
        if not validation.accepted:
            return Phase1Result(success=False, message=validation.message)

        # Extract landmarks for the accepted face
        face_idx  = validation.face_idx
        landmarks = self.detector.get_landmarks_array(points, face_idx)

        # Load the image with OpenCV for alignment
        img_bgr = cv2.imread(img_path)
        if img_bgr is None:
            return Phase1Result(success=False, message='Failed to load image file.')

        # Stage 3: Face Alignment
        aligned = self.aligner.align(img_bgr, landmarks)

        return Phase1Result(
            success=True,
            message='Phase 1 completed successfully.',
            aligned_face=aligned,
            landmarks=landmarks,
            confidence=validation.confidence,
        )


# ── Quick usage example ──
if __name__ == '__main__':
    pipeline = Phase1Pipeline()
    result   = pipeline.run('test_images/valid_face.jpg')

    if result.success:
        print(f'Success! Confidence: {result.confidence:.4f}')
        cv2.imwrite('aligned_output.jpg', result.aligned_face)
        print('Aligned face saved to: aligned_output.jpg')
    else:
        print(f'Rejected: {result.message}')
