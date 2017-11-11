# download youtube files as .wav

from subprocess import call

wav_dir = "../../data/"

youtube_links = [{
    "link": "https://www.youtube.com/watch?v=LRP8d7hhpoQ",
    "name": "A#-hallelujah-pentatonix",
    "downloaded": True
}, {
    "link": "https://www.youtube.com/watch?v=XvVmZmMLojc",
    "name": "Em-Somebody_That_I_Used_To_Know_vocals",
    "downloaded": True
}, {
    "link": "https://www.youtube.com/watch?v=byXb3KT1-3A",
    "name": "D-ThinkingOutLoud_vocals",
    "downloaded": True
}, {
    "link": "https://www.youtube.com/watch?v=XMqEFuGA2cE",
    "name": "G#-Perfect_vocals",
    "downloaded": True
},  {
    "link": "https://www.youtube.com/watch?v=yxaA94HGo9A",
    "name": "G-pengyou",
    "downloaded": True
},
    {
    "link": "https://www.youtube.com/watch?v=VuA86Lv-bx0",
    "name": "C-xiaowei",
    "downloaded": True
}, {
    "link": "https://www.youtube.com/watch?v=UprcpdwuwCg",
    "name": "G-heathens_original",
    "downloaded": False
}, {
    "link": "https://www.youtube.com/watch?v=Y7XWElxq0Io",
    "name": "G-heathens_vocals_original",
    "downloaded": False
}, {
    "link": "https://www.youtube.com/watch?v=EFEmTsfFL5A",
    "name": "E-aint_it_fun_original",
    "downloaded": False
}, {
    "link": "https://www.youtube.com/watch?v=k4V3Mo61fJM",
    "name": "D#-fix_you_original",
    "downloaded": False
}, {
    "link": "https://www.youtube.com/watch?v=7Bz2E8KxedM",
    "name": "D#-fix_you_vocals_original",
    "downloaded": False
}, {
    "link": "https://www.youtube.com/watch?v=Ho32Oh6b4jc",
    "name": "D-perfect_one_direction_original",
    "downloaded": False
}, {
    "link": "https://www.youtube.com/watch?v=3aLjoFzM7IU",
    "name": "A-Wonderwall_vocals_original",
    "downloaded": False
}, {
    "link": "https://www.youtube.com/watch?v=bx1Bh8ZvH84",
    "name": "A-wonderwall_original",
    "downloaded" : False
}]

for youtube_link in youtube_links:
    if not youtube_link["downloaded"]:
        print "downloading " + youtube_link["link"]
        call(["youtube-dl", youtube_link["link"],
              "-o",
              "".join((wav_dir, "{}.%(ext)s".format(youtube_link["name"]))),
              "--extract-audio",
              "--audio-format",
              "wav"])
