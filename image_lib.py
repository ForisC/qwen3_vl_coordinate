
from pathlib import Path
import base64
import cv2



def draw_bbox(image_path, bbox, ratio=0.7):

    image = cv2.imread(image_path)
    image = cv2.resize(image, (0, 0), fx=ratio, fy=ratio)
    bbox_resized = [int(coord * ratio) for coord in bbox]
    x1, y1, x2, y2 = bbox_resized
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.imshow("Image with BBox", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def save_bbox_image(image_path, bbox, ratio=0.7):
    new_file_name = Path(image_path).stem + "_with_bbox" + Path(image_path).suffix
    save_path = Path(image_path).parent / new_file_name
    image = cv2.imread(image_path)
    image = cv2.resize(image, (0, 0), fx=ratio, fy=ratio)
    bbox_resized = [int(coord * ratio) for coord in bbox]
    x1, y1, x2, y2 = bbox_resized
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.imwrite(save_path, image)



def image_to_base64(image_path):
    return base64.b64encode(Path(image_path).read_bytes()).decode()