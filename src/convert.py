import os

from Image2Ascii import Image2Ascii

images_src_path = 'output/frames/怒斥'
images_save_path = 'output/frames/怒斥_Ascii'

images = os.listdir(images_src_path)
images = list(filter(lambda x: x.endswith('jpg'), images))

for each_image in images:

    each_image_full_path = os.path.join(images_src_path, each_image)

    Ascii = Image2Ascii(each_image_full_path, 320, 0.5)
    each_image_name, _ = each_image.split('.')
    outFile = images_save_path + '/' + each_image_name + ".txt"

    file = open(outFile, 'w')
    for row in Ascii:
        file.write(row + '\n')
    file.close()
