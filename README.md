# Video2Ascii
Just for fun after work……original goal is to make a Jiang Zemin's Ascii video screensaver for "toad worship"
## Usage
### Prerequisites
(tested on) Ubuntu 16.04, python 3.5.2 with:
```
pip3 install Pillow  
pip3 install opencv-python
```
### Demo
```
python main.py --help
```
command required：
```  
--file test.mp4 or test.jpg (default path in Video2Ascii/files)  
--mode Video2Image or Video2Ascii or Image2Ascii
```
selective：  
```
--output video_name/video_split.jpg or output.txt (default path in Video2Ascii/output)  
--cols 100  
--scale 0.5 (vertical scaling factor - higher leads a longer face)  
```
## Result
<img src="https://user-images.githubusercontent.com/26578566/44344356-1e603680-a4c3-11e8-8893-372fd4162880.png" width="500">

<img src="https://user-images.githubusercontent.com/26578566/44344470-59626a00-a4c3-11e8-9f34-f4639396edf2.gif" width="500">
## TODO
* Try to optimize it, making the Ascii video real-time
* Implement an Ascii dynamic wallpaper or screensaver
* Image2AsciiImage, Video2AsciiVideo, AsciiCamera...
