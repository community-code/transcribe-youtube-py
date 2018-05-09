import youtube_dl
import re
import json

class MyLogger(object):
    def __init__(self):
        self.files = {}

    def info(self, msg):
        self.parse(msg)

    def debug(self, msg):
        self.parse(msg)

    def warning(self, msg):
        self.parse(msg)

    def error(self, msg):
        self.parse(msg)

    def parse(self, msg):
        print(msg)
        subtitleRe = re.compile("\[info\] Writing video subtitles to: (.*)")
        match = subtitleRe.match(msg)
        if (match):
            self.files['subtitles'] = match.group(1)
        if (msg[0] == '{'):
            self.files['jsoninfo'] = msg


def getVideo(url):
    finished_files = []
    logger = MyLogger()

    def my_hook(d):
        if d['status'] == 'finished':
            finished_files.append(d['filename'])

    ydl_opts = {
        'writesubtitles': True,
        'outtmpl': 'vid.webm',
        'progress_hooks': [my_hook],
        'logger': logger,
        'subtitlesformat':'vtt',
        'format': 'webm',
        'forcejson': True
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    if (len(finished_files) == 1 and logger.files['subtitles'] != None):
        return {"subtitles": logger.files['subtitles'], "video": finished_files[0], "info": logger.files['jsoninfo']}
    else:
        return {}