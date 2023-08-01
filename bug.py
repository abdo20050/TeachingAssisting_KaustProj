from subprocess import run
cmd = [
        "ffmpeg",
        "-nostdin",
        "-threads", "0",
        "-i", "./samples/audio.mp3",
        "-f", "s16le",
        "-ac", "1",
        "-acodec", "pcm_s16le",
        "-ar", "1000",
        "-"
    ]
out = run(cmd, capture_output=True, check=True).stdout
print(out)