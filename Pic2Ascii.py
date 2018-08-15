import sys, random, argparse#argparse库用于命令行解析
import numpy as np          #numpy库用于大型矩阵计算
import math

from PIL import Image       #PIL库是Python事实上的图像处理标准库

# 图片转ASCII的基本原理是将灰度图片分割成众多小网格，将小网格的平均亮度计算出来用不同亮度字符代替
# 灰度梯度对应字符可参考：http://paulbourke.net/dataformats/asciiart/
# 70级灰度梯度（越来越亮）
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
# 10级灰度梯度
gscale2 = '@%#*+=-:. '

#计算每一小块平均亮度
def getAverageL(image):
    im = np.array(image)#小块转成二维数组
    w, h = im.shape#保存小块尺寸
    return np.average(im.reshape(w * h))#将二维数组转成一维，求均值

#根据每一小块平均亮度匹配ASCII字符
def covertImageToAscii(fileName, cols, scale, moreLevels):
    global gscale1, gscale2#灰度梯度
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

    aimg = []#文本图形存储到列表中
    #逐个小块匹配ASCII
    for j in range(rows):
        y1 = int(j * h)#小块开始的y坐标
        y2 = int((j + 1) * h)#小块结束的y坐标
        if j == rows - 1:
            y2 = H#最后一个小格不够大，结束y坐标用图像高度H表示
        aimg.append("")#先插入空串
        for i in range(cols):
            x1 = int(i * w)#小块开始的x坐标
            x2 = int((i + 1) * w)#小块结束的x坐标
            if i == cols - 1:
                x2 = W#最后一个小格不够大，结束x坐标用图像宽度W表示
            img = image.crop((x1, y1, x2, y2))#提取小块
            avg = int(getAverageL(img))#计算平均亮度
            if moreLevels:
                gsval = gscale1[int((avg * 69) / 255)]#平均亮度值[0,255]对应到十级灰度梯度[0,69]，获得对应ASCII符号
            else:
                gsval = gscale2[int((avg * 9) / 255)]#平均亮度值[0,255]对应到七十级灰度梯度[0,9]，获得对应ASCII符号
            aimg[j] += gsval#更新文本图形
    return aimg

#主函数
def main():
    descStr = "Python实现图片转ASCII图形"
    parser = argparse.ArgumentParser(description=descStr)
    #设置可能的命令行参数来运行程序
    parser.add_argument('--file', dest='imgFile', required=True)#必须设置
    parser.add_argument('--scale', dest='scale', required=False)#可缺省
    parser.add_argument('--out', dest='outFile', required=False)
    parser.add_argument('--cols', dest='cols', required=False)
    parser.add_argument('--morelevels', dest='moreLevels', action='store_true')#设置morelevels为True

    args = parser.parse_args()#参数存到args中

    imgFile = args.imgFile#输入的图片
    outFile = 'out.txt'#输出的ASCII文本图形
    if args.outFile:
        outFile = args.outFile
    scale = 0.43#垂直比例系数测试得0.43效果佳，必须用等长字体显示文本，如宋体、Courier
    if args.scale:
        scale = float(args.scale)
    cols = 200#默认分割的列数，列数越大精细度越大，但不建议过大
    if args.cols:
        cols = int(args.cols)

    print("转换中...")
    aimg = covertImageToAscii(imgFile, cols, scale, args.moreLevels)#调用匹配函数

    f = open(outFile, 'w')#保存文档图片
    for row in aimg:
        f.write(row + '\n')
        print(row)
    f.close()
    print("ASCII文本图形存储于%s" % outFile)

#main函数
if __name__ == '__main__':
    main()

#Pycharm设置命令行参数运行方法：Run→Run→Edit Configurations→Defaults→Python→右边的Parameters
#必填：输入图片路径--file test.jpg
#选填：
#（推荐）图片分割小块列数--cols 100
#输出ASCII文本图形路径--out out.txt
#垂直比例系数--scale 1
#使用70级灰度梯度--morelevels
