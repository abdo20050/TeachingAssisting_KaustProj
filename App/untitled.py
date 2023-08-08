from transformers import PegasusTokenizer, PegasusForConditionalGeneration
model_name = './model/'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


from transformers import pipeline

generator = pipeline(task="text-generation", model=model, tokenizer=tokenizer)