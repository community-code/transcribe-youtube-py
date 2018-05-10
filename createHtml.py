import cv2
import os
import cv2

FRAME_HTML = """
<tr>
<td>
<img src="%d.png" style="height:240; float: left;padding-right: 15px"/>
</td>
<td>
<p>%s</p>
</td>
</tr>
"""
HTML = """
<html>
<body>
<table>
%s
</table>
</body>
</html>
"""

def createHtml(frames, id):
    # Write frames
    for i in range(0, len(frames)):
        cv2.imwrite(os.path.join("out", str(i) + ".png"), frames[i]['frame'])

    htmlBody = ""
    #Write Html
    for i in range(0, len(frames)):
        htmlBody += FRAME_HTML % (i, frames[i]['text'])

    html = HTML % (htmlBody)
    with open(os.path.join("out",  "index.html"), "w") as text_file:
         text_file.write(html)