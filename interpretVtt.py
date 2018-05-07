from webvtt import WebVTT
import datetime

def strToTime(str):
    return datetime.datetime.strptime(str, "%H:%M:%S.%f")

def read(fileName):
    return [{"start": strToTime(x.start), "end": strToTime(x.end), "text": x.text} for x in WebVTT().read(fileName)]

def subtitlesAtTime(captions, time):
    return list(filter(lambda x: x['start'] <= time and x['end'] >= time, captions))

def subtitlesBetween(captions, start, end):
    return list(filter(lambda x: x['start'] <= end and x['end'] >= start, captions))