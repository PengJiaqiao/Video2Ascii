import sys, random, argparse#argparse for command analysis
import numpy as np          #numpy for matrix computation
import math

from PIL import Image       #PIL: standard python module for image processing

# Cut grey scale image into several small block and different character for different scale
# reference：http://paulbourke.net/dataformats/asciiart/

# 10 levels
gscale = '@%#+=:. '
# 70 levels (works worse than less levels)
# gscale_more = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def main():
    # set command argument
    parser = argparse.ArgumentParser(description="Convert Image to Ascii")
    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='scale', required=False)
    parser.add_argument('--output', dest='outFile', required=False)
    parser.add_argument('--cols', dest='cols', required=False)
    # parser.add_argument('--morelevels', dest='moreLevels', action='store_true')#default:False(less levels)

    # get command argument
    args = parser.parse_args()

    outFile = 'output/output.txt'
    if args.outFile:
        outFile = args.outFile

    scale = 0.43
    if args.scale:
        scale = float(args.scale)

    cols = 200
    if args.cols:
        cols = int(args.cols)


    Ascii = Image2Ascii(args.imgFile, cols, scale)

    file = open(outFile, 'w')
    for row in Ascii:
        file.write(row + '\n')
        print(row)
    file.close()

# Compute average lightness
def AvgLightness(block):
    # image block to array
    im = np.array(block)
    width, height = im.shape
    return np.average(im.reshape(width * height))

# allocate ASCII character by grey scale
def Image2Ascii(fileName, cols, scale):
    global gscale_more, gscale
    image = Image.open(fileName).convert('L')#打开图片并转换成灰度图
    W, H = image.size[0], image.size[1]#保存图像宽高
    print("图像宽高: %dx%d" % (W, H))
    w = W / cols#计算小块宽度
    h = w / scale#计算小块高度，此处除垂直比例系数用于减少图像违和感，经测试scale为0.43时效果较好
    rows = int(H / h)#计算行数
    print("共有%d行 %d列小块" % (rows,cols))
    print("每一小块宽高: %dx%d" % (w, h))

    #图像太小则退出
    if cols > W or rows > H:
        print("图像太小不足分割！（提高图像分辨率或降低精细度）")
        exit(0)

    Ascii = []
    #逐个小块匹配ASCII
    for j in range(rows):
        y1 = int(j * h)#小块开始的y坐标
        y2 = int((j + 1) * h)#小块结束的y坐标
        if j == rows - 1:
            y2 = H#最后一个小格不够大，结束y坐标用图像高度H表示

        # in case of "list index out of range"
        Ascii.append("")
        for i in range(cols):
            x1 = int(i * w)#小块开始的x坐标
            x2 = int((i + 1) * w)#小块结束的x坐标
            if i == cols - 1:
                x2 = W#最后一个小格不够大，结束x坐标用图像宽度W表示
            block = image.crop((x1, y1, x2, y2))#提取小块
            avg = int(AvgLightness(block))#计算平均亮度
            # if moreLevels:
            #     gsval = gscale_more[int((((avg + 1)* 70) >> 8) )]
            # else:
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
    return Ascii


if __name__ == '__main__':
    main()

# command
# required：--file test.jpg
# selective：--cols 100
#            --output output.txt
#            --scale 1 (vertical scaling factor)
#            --morelevels
