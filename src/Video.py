import os
import cv2
from PIL import Image
import numpy as np

model = '@%#+=:. '

class Video(object):
    def __init__(self, File, OutputPath, cols, scale):
        self.file_path = 'files/' + File
        self.file_name, _ = str(File).split('.')
        self.save_path = os.path.join(OutputPath, self.file_name)
        self.cols = int(cols)
        self.scale = float(scale)
    def Video2Image(self):
        os.mkdir(self.save_path)

        cap  = cv2.VideoCapture(self.file_path)
        frame_count = 1
        success = True
        while(success):
            success, frame = cap.read()
            cv2.imwrite(self.save_path + '/' + self.file_name + "_%d.jpg" % frame_count, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            frame_count = frame_count + 1
        cap.release()
    def Video2Ascii(self):
        def get_ascii(color):
            position = (color * 1.0) / 255
            target = int(len(model) * position)
            target = target % len(model)
            return model[target]#list(model[target].keys())

        def show_ascii(im, size):
            ascii_data = ""
            im = im.resize(size)
            im = im.convert('L')
            width = im.size[0]
            height = im.size[1]
            for y in range(height):
                for x in range(width):
                    pixel = im.getpixel((x, y))
                    ascii_data += get_ascii(pixel)
                ascii_data += "\n"
            return ascii_data

        def get_termial_size():
            size = os.popen("stty size").read().split()
            size[0] = int(size[1])
            size[1] = int(size[0]) / 4
            return size

        def get_current_size(img_size):
            img_scale = img_size[0] * 1.0 / img_size[1]
            termial_size = get_termial_size()
            termial_scale = termial_size[0] * 1.0 / termial_size[1]
            if img_scale > termial_scale:
                current_size = (int(termial_size[0]), int(
                    img_size[1] * (termial_size[0] * 1.0 / img_size[0])) * 2)
            else:
                current_size = (
                    int(img_size[0] * (termial_size[1] * 1.0 / img_size[1])) * 2, int(termial_size[1]))
            return current_size

        def get_current_max_size(img_size):
            termial_size = get_termial_size()
            current_size = (termial_size[0], int(
                img_size[1] * (termial_size[0] * 1.0 / img_size[0])) / 2)
            return current_size

        while(1):
            cap  = cv2.VideoCapture(self.file_path)
            while cap.isOpened():
                ret, frame = cap.read()
                pi = Image.fromarray(np.uint8(frame))
                size = get_current_size(pi.size)
                print (show_ascii(pi, size))
            cap.release()
