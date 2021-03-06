from webvtt import WebVTT
import datetime

def strToTime(str):
    return datetime.datetime.strptime(str, "%H:%M:%S.%f")

def read(fileName):
    return [{"start": strToTime(x.start), "end": strToTime(x.end), "text": x.text} for x in WebVTT().read(fileName)]

def subtitlesAtTime(captions, time):
    return list(filter(lambda x: x['start'] <= time and x['end'] >= time, captions))

def lastSubtitleAtTime(captions, time):
    captions = subtitlesAtTime(captions, time)
    if (len(captions) == 0):
        return None
    else:
        return captions[len(captions) - 1]

def subtitlesAfter(captions, start):
    between = filter(lambda x: x['start'] > start, captions)
    return list(map(lambda x : x['text'], between))

def subtitlesBetween(captions, start, end):
    between = filter(lambda x: x['start'] <= end and x['end'] >= start, captions)
    rest = filter(lambda x: x['start'] > end, captions)
    return (list(map(lambda x : x['text'], between)), list(rest))