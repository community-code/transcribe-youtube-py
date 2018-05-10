import youtube_dl
import re
import json
import tempfile
import os
import shutil

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
        'forcejson': True,
        'writeautomaticsub': True
    }

    prevDir = os.getcwd()
    # Youtube_dl stores the files in the cwd so change it to a temp dir
    dir = tempfile.mkdtemp(prefix="youtube_")
    print("Creating dir %s" % (dir))
    try:
        os.chdir(dir)
        try: 
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        finally:
            os.chdir(prevDir)

        if (len(finished_files) == 1 and 'subtitles' in logger.files):
            videoFile = os.path.join(dir, finished_files[0])
            subtitlesFile = os.path.join(dir,logger.files['subtitles'])
            return {"subtitles": subtitlesFile, "video": videoFile, "info": logger.files['jsoninfo'], "dir": dir}
        else:
            return {"dir": dir}
    except:
        #Clean up directory if an exception occurs before we return
        shutil.rmtree(dir)
        raise
