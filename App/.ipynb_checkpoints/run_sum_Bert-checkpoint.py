# Load model directly
from transformers import AutoTokenizer, BartForConditionalGeneration
import torch
device = 'cuda' if torch.cuda.is_available() else 'cpu'

mode_dir =  'abdo25/modawwen_bert_model'
tokenizer = AutoTokenizer.from_pretrained(mode_dir)
model = BartForConditionalGeneration.from_pretrained(mode_dir).to(device)

def summerize(input):
    # input = input[:max_input]
    # use different length sentences to test batching
    inputs = tokenizer([input], return_tensors="pt", truncation = True, padding=True, max_length = 1024).to(device)
    torch.cuda.empty_cache()
    model.eval()
    output_sequences = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        do_sample=False,  # disable sampling to test if batching affects output
        max_length = 256,
        min_length = 0,
    )
    output = tokenizer.batch_decode(output_sequences, skip_special_tokens=True)[0]
    return output
