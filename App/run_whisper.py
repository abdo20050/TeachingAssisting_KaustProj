import whisper
def speetch_to_txt(input):

    model = whisper.load_model("medium")

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(input)
    # audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options, fp16 = False)
    # print the recognized text
    output = result.text
    return output