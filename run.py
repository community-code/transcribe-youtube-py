import youtube_dl
from io import StringIO
import sys

url = "https://www.youtube.com/watch?v=XJGiS83eQLk"

finished_files = []

def my_hook(d):
    if d['status'] == 'finished':
        finished_files.append(d['filename'])

ydl_opts = {
    'writesubtitles': True,
    'outtmpl': 'vid.webm',
    'progress_hooks': [my_hook],
    'subtitlesformat':'vvt',
    'subtitleslangs':'en',
    'listsubtitles':True,
    'forcejson':True,
}

old_stdout = sys.stdout
result = StringIO()

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

sys.stdout = old_stdout

result_string = result.getvalue()
 
print(result_string)