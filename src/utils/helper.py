from PIL import ImageTk


def rotate_image(image, angle):
    rotated_image = image.rotate(angle)
    return ImageTk.PhotoImage(rotated_image)
