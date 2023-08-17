import gradio as gr
import os
from run_whisper import speetch_to_txt
from run_translation import translate_text
from run_sum import summerize
from run_GPT_sum import summarize_gpt
import time

blocks = gr.Blocks()

with blocks as demo:
    drop = gr.Audio(source="upload", type="filepath", label="Drop your audio file here!")

    with gr.Row():
        btn1 = gr.Button("Use Uploaded Audio")
        btn2 = gr.Button("Use Recorded Audio.")

    def generate(input):
        print(input)
        output = speetch_to_txt(input) #Use whisper here\
        #print(f"original text: {output}")
        output_1 = summerize(output) #summarize here
        #print("-----------------------------------")
        #print(f"summarized text by ours: {output_1}")
        #print("-----------------------------------")
        output_2 = summarize_gpt(output)
        #print(f"summarized text by GPT: {output_2}")
        #print("-----------------------------------")
        output_1 = translate_text(output_1) #Microsoft translation here
        #print(f"Translated of our summarization: {output_1}")
        output_2 = translate_text(output_2) #Microsoft translation here
        #print("-----------------------------------")
        #print(f"Translated of GPT summarization: {output_2}")
        #print("-----------------------------------")
        return output_1, output_2
    
    output_1 = gr.Textbox(label="Our summarization")
    output_2 = gr.Textbox(label="GPT summarization")
    btn1.click(fn = generate, inputs = drop, outputs=[output_1, output_2])
# demo.queue(concurrency_count=5,max_size = 20)
demo.launch(share=True)
