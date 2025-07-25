from dataclasses import dataclass
from typing import List, Optional, Tuple

@dataclass
class Detection:
    label: str = ""
    confidence: float = 0.0
    bbox: Optional[Tuple[int, int, int, int]] = None   # (x1, y1, x2, y2)
    

@dataclass
class DetectionResult:
    detections: List[Detection]
    image_with_boxes: any  # np.ndarray
    id: str = ""


    def is_defect(self, threshold, target_labels=None) -> bool:
        if target_labels is None:
            target_labels = ["defect"]  # hoặc danh sách label lỗi

        return any(
            det.confidence > threshold and det.label in target_labels
            for det in self.detections
        )

