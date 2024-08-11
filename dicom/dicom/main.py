import pydicom
from PIL import Image
import numpy as np
from pathlib import Path


def dicom_to_image(dicom_file):
    # Read the DICOM file
    ds = pydicom.dcmread(dicom_file)

    # Get the pixel array from the DICOM file
    pixel_array = ds.pixel_array

    # Normalize the pixel array if needed
    # This is to handle the data type, scaling it to 8-bit if required
    if pixel_array.max() > 255:
        pixel_array = (np.maximum(pixel_array, 0) / pixel_array.max()) * 255
        pixel_array = np.uint8(pixel_array)
    elif pixel_array.max() <= 255 and pixel_array.dtype != np.uint8:
        pixel_array = np.uint8(pixel_array)

    # Convert to PIL image
    image = Image.fromarray(pixel_array)

    return image


def create_destiny_folder(prefix, path_to_file):
    destiny_path = Path(prefix) / path_to_file
    if not destiny_path.exists():
        destiny_path.mkdir(parents=True)
    return destiny_path


def save_jpg(destiny_path: Path, image_name: str, converted_image: Image):

    dst_jpg = destiny_path / Path(image_name + ".jpg")
    converted_image.save(dst_jpg, "JPEG", quality=100)


def save_png(destiny_path: Path, image_name: str, converted_image: Image):
    dst_png = destiny_path / Path(image_name + ".png")
    converted_image.save(dst_png)


def convert_all_dcm_images(data_path: Path):
    image_files = data_path.rglob("*.dcm")
    for image in image_files:
        converted_image = dicom_to_image(image)
        path_to_file = image.parent

        destiny_path = create_destiny_folder("jpg", path_to_file)
        save_jpg(destiny_path, image.name, converted_image)

        destiny_path = create_destiny_folder("png", path_to_file)
        save_png(destiny_path, image.name, converted_image)


if __name__ == "__main__":
    convert_all_dcm_images(Path("data"))
