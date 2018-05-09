from getVideo import getVideo
from interpretVideo import interpretVideo
import cv2
import math
import datetime
import os.path

url = "https://www.youtube.com/watch?v=XJGiS83eQLk"

files = getVideo(url)

frames = interpretVideo(files['video'], files['subtitles'])

cwd = os.getcwd()

for i in range(0, len(frames)):
    cv2.imwrite(os.path.join("out", str(i) + ".png"), frames[i]['frame'])
    with open(os.path.join(cwd, "out", str(i) + ".txt"), "w") as text_file:
        text_file.write(frames[i]['text'])
    
cv2.destroyAllWindows()