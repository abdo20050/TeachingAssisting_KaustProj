import gradio as gr
import os
from run_whisper import speetch_to_txt
from run_translation import translate_text
from run_sum import summerize

blocks = gr.Blocks()

with blocks as demo:
    drop = gr.Audio(source="upload", type="filepath", label="Drop your audio file here!")
    record = gr.Audio(source="microphone", label="Record!")

    with gr.Row():
        btn1 = gr.Button("Use Uploaded Audio")
        btn2 = gr.Button("Use Recorded Audio.")

    def generate(input):
        
        output = speetch_to_txt(input) #Use whisper here\
        output = summerize(output) #summarize here
        output = translate_text(output) #Microsoft translation here
        return output
    
    output1 = gr.Textbox(label="Output")

    btn1.click(generate, drop, output1)
    btn2.click(generate, record, output1)

demo.launch(share=True)
