# download youtube files as .wav

from subprocess import call

wav_dir = "../data/"

youtube_links = [{
    "link": "https://www.youtube.com/watch?v=LRP8d7hhpoQ",
    "name" : "A#-hallelujah-pentatonix"
}, {
    "link": "https://www.youtube.com/watch?v=XvVmZmMLojc",
    "name": "Em-Somebody_That_I_Used_To_Know_vocals"
}, {
    "link": "https://www.youtube.com/watch?v=byXb3KT1-3A",
    "name": "D-ThinkingOutLoud_vocals"
},{
  "link" : "https://www.youtube.com/watch?v=XMqEFuGA2cE",
  "name" : "G#-Perfect_vocals"
}]

for youtube_link in youtube_links:
    print "downloading " + youtube_link["link"]
    call(["youtube-dl", youtube_link["link"],
          "-o",
          "".join((wav_dir, "{}.%(ext)s".format(youtube_link["name"]))),
          "--extract-audio",
          "--audio-format",
          "wav"])
