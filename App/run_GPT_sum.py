import gradio as gr
import openai


openai.api_key = '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'



def generate_Notes(whisperText,prompt = None):
    if prompt is None :
      prompt=f'''your role is to note taking,
      take notes of the following lecture text and show the most important titles and underneath it write notes follow these instructions:
      1-right the titles in numerical order and underneath them write the notes
      2-be organized and keep the notes very short 
      3-if you can, give examples from the same lecture text underneath the titles
      4-be organized and importantly leave space between each title point  , in the end just show the notes.:\n\n {whisperText}'''
    else:
      prompt = f'"{whisperText}"\n'+prompt
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "take notes for the given licture"},
                  {"role": "user", "content": prompt}]
    )

    Notes = response.choices[0].message['content']
    tokens_used = response['usage']['total_tokens']
    return f" {Notes}\nTokens Used: {tokens_used}"
def summarize_gpt(input):
    output = generate_Notes(input, prompt = "summarize the lecture into max of 1024 words")
    return output