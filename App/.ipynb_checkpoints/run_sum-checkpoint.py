from transformers import PegasusForConditionalGeneration,PegasusTokenizerFast , PegasusTokenizer, Trainer , TrainingArguments
import torch
# from tqdm import tqdm

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model_name = './Pegasus_finetuned_model/'
# model_name = 'google/pegasus-large'

batch_size = 1

tokenizer = PegasusTokenizerFast.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)

def summerize(input_txt):
    batch = tokenizer(input_txt, truncation=True, padding="longest", return_tensors="pt",max_length = 1024).to(device)
    torch.cuda.empty_cache()
    model.eval()
    translated = model.generate(**batch, max_length= 1024)
    output_txt = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
    return output_txt