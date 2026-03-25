# pipeline/phase1.py
from dataclasses import dataclass
from typing import Optional
import numpy as np, cv2
from .detector  import FaceDetector
from .validator import FaceValidator
# FaceAligner import removed
 
@dataclass
class Phase1Result:
    success:    bool
    message:    str
    face_crop:  Optional[np.ndarray] = None  # RGB 224x224
    landmarks:  Optional[np.ndarray] = None  # shape (5, 2)
    confidence: Optional[float]      = None
    bbox:       Optional[tuple]      = None  # (x1, y1, x2, y2)
 
class Phase1Pipeline:
    """
    Phase 1: Input -> Detection -> Validation -> Crop & Resize.
    Output: 224x224 RGB face crop for VGG-Face via DeepFace.
    No explicit landmark alignment — DeepFace aligns internally.
    """
    CROP_PADDING = 0.10  # 10% padding around detected bbox
    OUTPUT_SIZE  = 224   # VGG-Face input resolution
 
    def __init__(self):
        self.detector  = FaceDetector()
        self.validator = FaceValidator()
 
    def _crop_face(self, img_bgr, bbox):
        h, w = img_bgr.shape[:2]
        x1, y1, x2, y2 = bbox
        bw, bh   = x2-x1, y2-y1
        px, py   = int(bw*self.CROP_PADDING), int(bh*self.CROP_PADDING)
        x1 = max(0, int(x1)-px);  y1 = max(0, int(y1)-py)
        x2 = min(w, int(x2)+px);  y2 = min(h, int(y2)+py)
        crop = cv2.resize(img_bgr[y1:y2, x1:x2],
                          (self.OUTPUT_SIZE, self.OUTPUT_SIZE),
                          interpolation=cv2.INTER_LINEAR)
        return cv2.cvtColor(crop, cv2.COLOR_BGR2RGB), (x1,y1,x2,y2)
 
    def run(self, img_path: str) -> Phase1Result:
        boxes, probs, points = self.detector.detect(img_path)
        val = self.validator.validate(boxes, probs)
        if not val.accepted:
            return Phase1Result(success=False, message=val.message)
        landmarks = self.detector.get_landmarks_array(points, val.face_idx)
        img_bgr   = cv2.imread(img_path)
        if img_bgr is None:
            return Phase1Result(success=False, message="Failed to load image.")
        face_crop, bbox = self._crop_face(img_bgr, boxes[val.face_idx])
        return Phase1Result(
            success=True, message="Phase 1 completed.",
            face_crop=face_crop, landmarks=landmarks,
            confidence=val.confidence, bbox=bbox,
        )
