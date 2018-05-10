from getVideo import getVideo
from interpretVideo import interpretVideo
from createHtml import createHtml
import cv2
import shutil

url = "https://www.youtube.com/watch?v=rlB602TNSqU"

id = "rlB602TNSqU"

files = getVideo(url)

try:
    frames = interpretVideo(files['video'], files['subtitles'])
    createHtml(frames, id)
finally:
    cv2.destroyAllWindows()
    if (files and files['dir']):
        shutil.rmtree(files['dir'])