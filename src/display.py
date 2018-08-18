import cv2
import sys
from PIL import Image
import numpy as np
import os

videos_src_path = '/home/jiaqiao/Video2Ascii'

videos = os.listdir(videos_src_path)
videos = list(filter(lambda x: x.endswith('mp4'), videos))

'''
model = [{'`': 0.0707070707070707}, {'_': 0.07317073170731707}, {'.': 0.09090909090909091}, {"'": 0.11019283746556474}, {'-': 0.1111111111111111}, {'~': 0.12121212121212122}, {'"': 0.12759170653907495}, {'^': 0.12828282828282828}, {',': 0.13909774436090225}, {'+': 0.16161616161616163}, {':': 0.18181818181818182}, {'=': 0.18585858585858586}, {';': 0.21804511278195488}, {'>': 0.22828282828282828}, {'<': 0.22828282828282828}, {'*': 0.2551834130781499}, {'!': 0.26136363636363635}, {'|': 0.2701688555347092}, {'}': 0.27514792899408286}, {'{': 0.27514792899408286}, {'L': 0.29117259552042163}, {'r': 0.29797979797979796}, {'T': 0.29818181818181816}, {'1': 0.3054545454545455}, {'?': 0.31024531024531027}, {'\\': 0.316008316008316}, {'/': 0.316008316008316}, {'7': 0.32242424242424245}, {'F': 0.3284848484848485}, {'u': 0.3356643356643357}, {'Y': 0.3356643356643357}, {'n': 0.337995337995338}, {'c': 0.3463203463203463}, {'m': 0.35645933014354064}, {'v': 0.35968379446640314}, {'y': 0.3616118769883351}, {'I': 0.36363636363636365}, {'q': 0.36397748592870544}, {'p': 0.36397748592870544}, {'%': 0.3653198653198653}, {')': 0.3684210526315789},
         {'(': 0.3684210526315789}, {'#': 0.3686868686868687}, {'H': 0.37575757575757573}, {'i': 0.3787878787878788}, {']': 0.3815789473684211}, {'[': 0.3815789473684211}, {'C': 0.3822843822843823}, {'U': 0.3824451410658307}, {'h': 0.38694638694638694}, {'@': 0.3924501424501424}, {'4': 0.3939393939393939}, {'x': 0.39920948616600793}, {'z': 0.40115440115440115}, {'o': 0.4024242424242424}, {'t': 0.4028520499108734}, {'k': 0.4036363636363636}, {'J': 0.40576923076923077}, {'e': 0.4065656565656566}, {'w': 0.40771349862258954}, {'V': 0.408008658008658}, {'s': 0.4083694083694084}, {'l': 0.4090909090909091}, {'a': 0.41035353535353536}, {'$': 0.41368421052631577}, {'P': 0.4160839160839161}, {'E': 0.4193939393939394}, {'Q': 0.42105263157894735}, {'g': 0.42120075046904315}, {'2': 0.42303030303030303}, {'M': 0.42424242424242425}, {'f': 0.42803030303030304}, {'j': 0.42886178861788615}, {'3': 0.4290909090909091}, {'G': 0.4292929292929293}, {'K': 0.43573667711598746}, {'5': 0.43636363636363634}, {'O': 0.4389051808406647}, {'N': 0.4393939393939394}, {'X': 0.44372294372294374}, {'D': 0.4444444444444444}, {'d': 0.44522144522144524}, {'b': 0.44522144522144524}, {'Z': 0.44871794871794873}, {'R': 0.4491341991341991}, {'A': 0.4512987012987013}, {'S': 0.4557109557109557}, {'W': 0.4628787878787879}, {'&': 0.4633431085043988}, {'0': 0.4824242424242424}, {'9': 0.4993939393939394}, {'6': 0.4993939393939394}, {'B': 0.5196408529741863}, {'8': 0.5321212121212121}]
'''

#model = '@%#+=:. '

model = '%+++===:::~~~---...   '

def clear_screen():
    os.system("clear")

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

def play(url):
    cap = cv2.VideoCapture(url)
    while cap.isOpened():
        ret, frame = cap.read()
        pi = Image.fromarray(np.uint8(frame))
        size = get_current_size(pi.size)
        clear_screen()
        print (show_ascii(pi, size))

def main():
    for each_video in videos:

        # get the name of each video, and make the directory to save frames
        each_video_name, _ = each_video.split('.')

        # get the full path of each video, which will open the video tp extract frames
        each_video_full_path = os.path.join(videos_src_path, each_video)

        cap  = cv2.VideoCapture(each_video_full_path)
        while cap.isOpened():
            ret, frame = cap.read()
            pi = Image.fromarray(np.uint8(frame))
            size = get_current_size(pi.size)
            #clear_screen()
            print (show_ascii(pi, size))

    cap.release()

if __name__ == '__main__':
    main()
