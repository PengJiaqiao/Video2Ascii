import os
from PIL import Image, ImageFont, ImageDraw

def main():
    txts = os.listdir()
    txts = list(filter(lambda x: x.endswith('txt'), txts))
    for each_txt in txts:
        txt2image(each_txt)

def txt2image(file_name):
    im = Image.open(file_name)
    #gif拆分后的图像，需要转换，否则报错，由于gif分割后保存的是索引颜色
    raw_width = im.width
    raw_height = im.height
    width = int(raw_width/6)
    height = int(raw_height/15)
    im = im.resize((width,height),Image.NEAREST)

    txt=""
    colors = []
    for i in range(height):
        for j in range(width):
            pixel = im.getpixel((j,i))
            colors.append((pixel[0],pixel[1],pixel[2]))
            if(len(pixel) == 4):
                txt += get_char(pixel[0],pixel[1],pixel[2],pixel[3])
            else:
                txt += get_char(pixel[0],pixel[1],pixel[2])
        txt += '\n'
        colors.append((255,255,255))

    im_txt = Image.new("RGB",(raw_width,raw_height),(255,255,255))
    dr = ImageDraw.Draw(im_txt)
    #font = ImageFont.truetype(os.path.join("fonts","汉仪楷体简.ttf"),18)
    font=ImageFont.load_default().font

    x=y=0
    #获取字体的宽高
    font_w,font_h=font.getsize(txt[1])
    font_h *= 1.37 #调整后更佳
    #ImageDraw为每个ascii码进行上色
    for i in range(len(txt)):
        if(txt[i]=='\n'):
            x+=font_h
            y=-font_w
        dr.text((y,x),txt[i],font = font, fill = colors[i])
        y+=font_w

    name = file_name
    print(name+' changed')
    im_txt.save(name)

if __name__ == '__main__':
    main()
