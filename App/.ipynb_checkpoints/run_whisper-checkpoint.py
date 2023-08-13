import whisper
def speetch_to_txt(input):

    model = whisper.load_model("base.en")
    print(model.device)
    output = model.transcribe(input)["text"]
    return output