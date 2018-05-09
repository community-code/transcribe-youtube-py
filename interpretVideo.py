import interpretVtt
import cv2
import math
import datetime

def createDateTime(ms):
   base_datetime = datetime.datetime( 1900, 1, 1 )
   delta = datetime.timedelta(0, 0, 0, ms)
   return base_datetime + delta

def frameNumberToDateTime(frameNumber, fps):
    time = float(frameNumber)/float(fps) # seconds
    return createDateTime(time*1000)

def readFrames(videoFile):
    cap = cv2.VideoCapture(videoFile)
    try:
        if not cap.isOpened(): 
            print("could not open")
        lengthEstimate = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps    = cap.get(cv2.CAP_PROP_FPS)

        # Youtube videos sometimes report an incorrect frame rate
        # rescale to 30
        if (fps == 1000):
            scale = 1000 / 30
            fps /= scale
            lengthEstimate /= scale

        durationEstimate = float(lengthEstimate) / float(fps) # seconds
        minutesEstimate = math.floor(durationEstimate / 60)
        sampleEvery = math.floor(lengthEstimate/minutesEstimate)
        sampleNumber = minutesEstimate


        capturedFrames = []
        for i in range(0,sampleNumber):
            frameNumber = i * sampleEvery
            cap.set(cv2.CAP_PROP_POS_FRAMES, frameNumber)
            ret, frame = cap.read()

            if not ret:
                break
            capturedFrames.append({'frame': frame, 'frameNumber': frameNumber, 'time': frameNumberToDateTime(frameNumber, fps)})
        
        return capturedFrames

    finally:
        cap.release()
    return []

def getSubtitlesForFrame(captions, currentFrame, nextFrame):
    frame = currentFrame['frame']
    start = currentFrame['time']
    test = []
    if (nextFrame):
        end = nextFrame['time']
        text = interpretVtt.subtitlesBetween(captions, start, end)    
    else:
        text = interpretVtt.subtitlesAfter(captions, start)
    fullText = "\n".join(text)
    return fullText

def interpretVideo(videoFile, subtitleFile):
    captions = interpretVtt.read(subtitleFile)

    capturedFrames = readFrames(videoFile)

    frames = []

    for i in range(0, len(capturedFrames)):
        currentFrame = capturedFrames[i]
        nextFrame = capturedFrames[i + 1] if i + 1 < len(capturedFrames) else None
        fullText = getSubtitlesForFrame(captions, currentFrame, nextFrame)
        frames.append({'frame': currentFrame['frame'], 'text': fullText})

    return frames