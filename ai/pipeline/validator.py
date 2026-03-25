# pipeline/validator.py
from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class ValidationResult:
    accepted:   bool
    message:    str
    face_idx:   Optional[int]   = None   # index of the accepted face
    confidence: Optional[float] = None   # confidence score of accepted face


class FaceValidator:
    """
    Applies three acceptance conditions to MTCNN outputs.
    """

    CONFIDENCE_THRESHOLD = 0.90
    MIN_FACE_SIZE        = 40     # pixels

    def validate(
        self,
        boxes:  Optional[np.ndarray],
        probs:  Optional[np.ndarray],
    ) -> ValidationResult:
        """
        Args:
            boxes : output from detector.detect() — shape (N, 4) or None
            probs : output from detector.detect() — shape (N,)   or None
        Returns:
            ValidationResult with accepted=True/False and a message
        """

        # Condition 1: at least one face must be detected
        if boxes is None or len(boxes) == 0:
            return ValidationResult(
                accepted=False,
                message='No face detected. Please upload a clear photo with one face.',
            )

        # Condition 1b: exactly one face must be present
        if len(boxes) > 1:
            return ValidationResult(
                accepted=False,
                message='More than one face detected. Please upload a photo of one person.',
            )

        # Condition 2: confidence score must be >= 0.9
        score = float(probs[0])
        if score < self.CONFIDENCE_THRESHOLD:
            return ValidationResult(
                accepted=False,
                message=f'Image quality too low (Score: {score:.2f}). Please upload a clearer photo.',
            )

        # Condition 3: bounding box must be large enough
        x1, y1, x2, y2 = boxes[0]
        w = x2 - x1
        h = y2 - y1
        if w < self.MIN_FACE_SIZE or h < self.MIN_FACE_SIZE:
            return ValidationResult(
                accepted=False,
                message='Face is too small in the image. Please upload a photo where the face is larger.',
            )

        return ValidationResult(
            accepted=True,
            message='Image accepted successfully.',
            face_idx=0,
            confidence=score,
        )
