import numpy as np
import math
import os
from PIL import Image as Img

# Cut grey scale image into several small block and different character for different scale
# reference：http://paulbourke.net/dataformats/asciiart/

# 10 levels
gscale = '@%#+=:. '
# 70 levels (works worse than less levels)
# gscale_more = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

class Image(object):
    def __init__(self, File, OutputPath, cols, scale):
        self.file_path = 'files/' + File
        self.file_name, _ = str(FilePath).split('.')
        self.save_path = os.path.join(OutputPath, path) + '.txt'
        self.cols = int(cols)
        self.scale = float(scale)

    def Image2Ascii(self):
        image = Img.open(self.file_path).convert('L')# open file and convert it
        W, H = image.size[0], image.size[1]
        print("Image size: %dx%d" % (W, H))
        w = W / self.cols# caculate block width
        h = w / self.scale# caculate block height
        rows = int(H / h)
        print("Totally %d rows and %d columns" % (rows,self.cols))
        print("Each block: %dx%d" % (w, h))

        #图像太小则退出
        if self.cols > W or rows > H:
            print("Too small to split!（use large size or less accuracy）")
            exit(0)

        def AvgLightness(block):
            # image block to array
            im = np.array(block)
            width, height = im.shape
            return np.average(im.reshape(width * height))

        Ascii = []
        # choose ascii
        for j in range(rows):
            y1 = int(j * h)# y coordinate: block begins from
            y2 = int((j + 1) * h)# y coordinate: block ends at
            if j == rows - 1:
                y2 = H

            # in case of "list index out of range"
            Ascii.append("")
            for i in range(self.cols):
                x1 = int(i * w)# x coordinate: block begins from
                x2 = int((i + 1) * w)# x coordinate: block ends at
                if i == self.cols - 1:
                    x2 = W
                block = image.crop((x1, y1, x2, y2))# get blocks
                avg = int(AvgLightness(block))
                if avg < 128:
                    if avg < 64:
                        if avg < 32:
                            gsval = 0
                        else:
                            gsval = 1
                    else:
                        if avg < 96:
                            gsval = 2
                        else:
                            gsval = 3
                else:
                    if avg < 192:
                        if avg < 160:
                            gsval = 4
                        else:
                            gsval = 5
                    else:
                        if avg < 224:
                            gsval = 6
                        else:
                            gsval = 7
                Ascii[j] += gscale[gsval]
        file = open(self.save_path, 'w')
        for row in Ascii:
            file.write(row + '\n')
            print(row)
        file.close()
