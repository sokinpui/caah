import albumentations as A
import cv2

# This variable name MUST be 'custom_transforms' for caah to find it
custom_transforms = [
    A.RandomScale(
        scale_limit=(0.0, 6.0),  # Note: screenshot says 1x-2x, but code says 0.0-6.0
        interpolation=cv2.INTER_LANCZOS4,
        mask_interpolation=cv2.INTER_NEAREST,
    ),
    A.HueSaturationValue(
        hue_shift_limit=20, sat_shift_limit=[-255, -255], val_shift_limit=20
    ),
    A.Rotate(limit=30),
    A.Affine(translate_percent={"x": 0.2, "y": 0.2}, shear={"x": 15, "y": 15}),
    A.Perspective(
        scale=(0.05, 0.1),
        keep_size=True,
        fit_output=False,
        border_mode=cv2.BORDER_CONSTANT,
    ),
    A.HorizontalFlip(p=0.5),
    A.Resize(640, 640),
]
