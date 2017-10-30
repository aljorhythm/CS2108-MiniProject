# download youtube files as .wav

from subprocess import call

wav_dir = "../wav-files/"

youtube_links = [{
    "link": "https://www.youtube.com/watch?v=LRP8d7hhpoQ"
}, {
    "link": "https://www.youtube.com/watch?v=lHjkix9oKIE"
}]

for youtube_link in youtube_links:
    print "downloading " + youtube_link["link"]
    call(["youtube-dl", youtube_link["link"], 
    	"-o", 
    	"".join((wav_dir, "%(title)s.%(ext)s")), 
    	"--extract-audio", 
    	"--audio-format", 
    	"wav"])
