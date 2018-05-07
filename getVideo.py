import youtube_dl

def getVideo(url):
    finished_files = []

    def my_hook(d):
        if d['status'] == 'finished':
            finished_files.append(d['filename'])

    ydl_opts = {
        'writesubtitles': True,
        'outtmpl': 'vid.webm',
        'progress_hooks': [my_hook],
        'subtitlesformat':'vvt',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    if (len(finished_files) == 1):
        return {"subtitles": "vid.en.vtt", "video": "vid.webm"}