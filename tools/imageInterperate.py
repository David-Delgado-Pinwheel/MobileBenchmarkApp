import pytesseract
from pytesseract import pytesseract
import PIL
from PIL import Image
import cv2

pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def readBenchmarkScores(imageLocation: str, w: int, h: int) -> list:
    image = Image.open(imageLocation)
    region = image.crop((0, int(0.3125 * h), w // 2, int(0.695 * h)))
    data=pytesseract.image_to_string(region, config='digits')
    return data.split("\n")[0:4]
