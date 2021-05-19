import os, sys, json
from subprocess import check_output
from bs4 import BeautifulSoup

# key=file name, val=video ID
kaltura_ids = {}

video_html = """
<iframe style="width: 1032px; height: 653px;" title="Lecture" src="https://canvas.wisc.edu/courses/222429/external_tools/retrieve?display=borderless&amp;url=https%3A%2F%2F1660902-6.kaf.kaltura.com%2Fbrowseandembed%2Findex%2Fmedia%2Fentryid%2F{entry_id}%2FshowDescription%2Ffalse%2FshowTitle%2Ffalse%2FshowTags%2Ffalse%2FshowDuration%2Ffalse%2FshowOwner%2Ffalse%2FshowUploadDate%2Ffalse%2FplayerSize%2F1032x653%2FplayerSkin%2F25717641%2F" width="1032" height="653" allowfullscreen="allowfullscreen" webkitallowfullscreen="webkitallowfullscreen" mozallowfullscreen="mozallowfullscreen" allow="geolocation *; microphone *; camera *; midi *; encrypted-media *; autoplay *"></iframe>
"""

def main():
    # find Kaltura's video IDs using manual dump from website
    with open("kaltura-listing.html") as f:
        doc = BeautifulSoup(f.read(), "html.parser")
    for link in doc.find_all("a"):
        txt = link.get_text().strip()
        href = link.attrs.get("href", "")
        if txt.startswith("cs220/"):
            kaltura_ids[txt.replace("cs220/", "./")] = href.split("/")[-2]

    videos = []
    for root, _, fnames in os.walk("."):
        videos.extend([os.path.join(root, fname) for fname in fnames
                       if fname.endswith(".mp4")])

    videos.sort()
    for vid in videos:
        upload_video_doc(vid)

def gen_video_doc(mp4_path):
    name = mp4_path.split("/")[-1]
    md_path = mp4_path.replace(".mp4", ".md")
    html_path = mp4_path.replace(".mp4", ".html")
    if not os.path.exists(md_path):
        with open(md_path, "w") as f:
            part = name.split("-")[0].replace("part", "Part ")
            f.write(f"# Watch ({part})\n\n")
            f.write("IFRAME\n\n")
            f.write(f"# Practice\n\n")
            f.write(f"# Questions About the Lecture?\n\nPlease ask below.\n\n")

    html = str(check_output(["pandoc", md_path]), "utf-8")

    # insert video at the end
    vhtml = video_html.format(entry_id=kaltura_ids[mp4_path])
    html = html.replace("IFRAME", vhtml)
    html = html.replace("margin: 0 auto;", "")

    with open(html_path, "w") as f:
        f.write(html)

if __name__ == '__main__':
     main()
