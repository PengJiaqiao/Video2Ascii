import argparse#argparse for command analysis
import sys
sys.path.append('src/')
from Video import Video
from Image import Image

def main():
    # set command argument
    parser = argparse.ArgumentParser(description = "Convertion between Video,\
     Image and Ascii")
    parser.add_argument('--file', dest = 'file', required = True, help = \
    "Default path in Video2Ascii/files")
    parser.add_argument('--mode', dest = 'mode', required = True, help = \
    "Video2Image or Video2Ascii or Image2Ascii")
    parser.add_argument('--output', dest = 'outFile', required = False, help = \
    "Default path in Video2Ascii/output", default = 'output')
    parser.add_argument('--cols', dest = 'cols', required = False, help = \
    "Numbers of Ascii column", default = 200)
    parser.add_argument('--scale', dest = 'scale', required = False, help = \
    "vertical scaling factor - higher leads a longer face", default = 0.5)
    # parser.add_argument('--morelevels', dest='moreLevels', action='store_true')#default:False(less levels)

    # get command argument
    args = parser.parse_args()

    if args.mode == 'Video2Image':
        video = Video(args.file, args.outFile, args.cols, args.scale)
        video.Video2Image()
    elif args.mode == 'Video2Ascii':
        video = Video(args.file, args.outFile, args.cols, args.scale)
        video.Video2Ascii()
    elif args.mode == 'Image2Ascii':
        image = Image(args.file, args.outFile, args.cols, args.scale)
        image.Image2Ascii()
    else:
        print("Arguments not found!")

if __name__ == '__main__':
    main()
