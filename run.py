from interpretVtt import read, subtitlesBetween
from getVideo import getVideo
import cv2
import math
import datetime

url = "https://www.youtube.com/watch?v=XJGiS83eQLk"

files = getVideo(url)

subtitleFile = 'vid.en.vtt' #files['subtitles']
videoFile = 'vid.webm' #files['video']

captions = read(subtitleFile)

cap = cv2.VideoCapture(videoFile)

if not cap.isOpened(): 
    print("could not open")

length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps    = cap.get(cv2.CAP_PROP_FPS)

def createDatetime(ms):
   base_datetime = datetime.datetime( 1970, 1, 1 )
   delta = datetime.timedelta( 0, 0, 0, ms)
   return base_datetime + delta

duration = float(length) / float(fps) # seconds
minutes = math.floor(duration / 60)
every = math.floor(length/minutes)

i = 0
capturedFrames = []
while True:
    ret, frame = cap.read()
    if not ret:
        break
    if (i % every):
        capturedFrames.append({'frame': frame, 'frameNumber': i})
    i += 1


length = i
duration = float(length) / float(fps) # seconds

timeslots = math.ceil(duration / 60.0)

combined = []

i = 0
for i in range(0, timeslots):
    time = math.ceil(x*60*fps)
    frame = frames[x]
    start = createDateTime(time*1000)
    end = createDateTime((time + 60)*1000)
    text = subtitlesBetween(captions, start, end)
    combined.append({'frame': frame, 'text': text})
    