import tkinter as tk
import pytesseract
import cv2
import numpy as np

from PIL import ImageTk


def align_captcha():
    img = cv2.imread("current.jpeg", cv2.IMREAD_GRAYSCALE)
    # ret, img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY_INV)

    Contours = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    # Contours.sort(key=lambda x: cv2.boundingRect(x)[0])
    Contours = sorted(Contours, key=lambda x: cv2.boundingRect(x)[0])

    newImg = np.zeros(img.shape, dtype=np.uint8)
    bb = cv2.boundingRect(Contours[0])
    newY = (bb[1] + bb[3])
    for Contour in Contours:
        [x, y, w, h] = cv2.boundingRect(Contour)

        newImg[newY - h + 1:newY + 1, x:x + w] = img[y:y + h, x:x + w].copy()

    cv2.imshow("img", img)
    cv2.imshow("newImg", newImg)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_value(ocr_image):
    global captcha_val

    def submit(event=None):
        global captcha_val
        input_value = entry.get().replace('\n','').upper()
        captcha_val = input_value
        print(f"Catpcha Value sent: {captcha_val}")
        root.destroy()

    root = tk.Tk()
    root.title("Gareeb OCR")

    label = tk.Label(root, text="Resolution:")
    label.pack()

    # align_captcha()

    g_scale = ocr_image.convert('L')
    helper_text = str(pytesseract.image_to_string(g_scale).replace(" ", "")).upper()

    entry = tk.Entry(root)
    entry.bind('<Return>', submit)
    entry.insert(0, helper_text)
    entry.pack()

    img = ImageTk.PhotoImage(ocr_image)

    # Add image to a Label widget
    img_label = tk.Label(root, image=img)
    img_label.image = img  # Keep a reference to the image
    img_label.pack()

    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.pack()

    root.mainloop()
    return captcha_val
