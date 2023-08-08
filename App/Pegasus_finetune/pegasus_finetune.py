

from transformers import PegasusForConditionalGeneration, PegasusTokenizer, Trainer , TrainingArguments
import torch

import atexit
import os

device = 'cuda' if torch.cuda.is_available() else 'cpu'
batch_size = 1
try:
    model_name = './model/'
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)
    print("model loaded from local")
except:
    model_name = 'google/pegasus-large'
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)
    print("model loaded from online")
model.to(device)




class PegasusDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels
    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels['input_ids'][idx])  # torch.tensor(self.labels[idx])
        return item
    def __len__(self):
        return len(self.labels['input_ids'])  # len(self.labels)

    
    


def prepare_data(model_name, 
                 train_texts, train_labels, 
                 val_texts=None, val_labels=None, 
                 test_texts=None, test_labels=None):
  """
  Prepare input data for model fine-tuning
  """
  tokenizer = PegasusTokenizer.from_pretrained(model_name)
  
  prepare_val = False if val_texts is None or val_labels is None else True
  prepare_test = False if test_texts is None or test_labels is None else True

  def tokenize_data(texts, labels):
    encodings = tokenizer(texts, truncation=True, padding=True)
    decodings = tokenizer(labels, truncation=True, padding=True)
    dataset_tokenized = PegasusDataset(encodings, decodings)
    return dataset_tokenized

  train_dataset = tokenize_data(train_texts, train_labels)
  val_dataset = tokenize_data(val_texts, val_labels) if prepare_val else None
  test_dataset = tokenize_data(test_texts, test_labels) if prepare_test else None

  return train_dataset, val_dataset, test_dataset, tokenizer


def prepare_fine_tuning(model_name, tokenizer, train_dataset, val_dataset=None, freeze_encoder=False, output_dir='./results',train_layer = 0):
  """
  Prepare configurations and base model for fine-tuning
  """
  torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
  model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)
  if train_layer > 0:
    for param in model.model.encoder.parameters():
      param.requires_grad = False
    for param in model.model.encoder.parameters():
      param.requires_grad = False
    for i in range(0,train_layer,-1):
        for param in model.model.encoder.block[i].parameters():
            param.requires_grad = True
    for i in range(0,train_layer,-1):
        for param in model.model.decoder.block[i].parameters():
            param.requires_grad = True
            
  if freeze_encoder:
    for param in model.model.encoder.parameters():
      param.requires_grad = False
    
  
  if val_dataset is not None:
    training_args = TrainingArguments(
      output_dir=output_dir,           # output directory
      num_train_epochs=2000,           # total number of training epochs
      per_device_train_batch_size=batch_size,   # batch size per device during training, can increase if memory allows
      per_device_eval_batch_size=batch_size,    # batch size for evaluation, can increase if memory allows
      save_steps=500,                  # number of updates steps before checkpoint saves
      save_total_limit=5,              # limit the total amount of checkpoints and deletes the older checkpoints
      evaluation_strategy='steps',     # evaluation strategy to adopt during training
      eval_steps=100,                  # number of update steps before evaluation
      warmup_steps=500,                # number of warmup steps for learning rate scheduler
      weight_decay=0.01,               # strength of weight decay
      logging_dir='./logs',            # directory for storing logs
      logging_steps=10,
    )

    trainer = Trainer(
      model=model,                         # the instantiated 🤗 Transformers model to be trained
      args=training_args,                  # training arguments, defined above
      train_dataset=train_dataset,         # training dataset
      eval_dataset=val_dataset,            # evaluation dataset
      tokenizer=tokenizer
    )

  else:
    training_args = TrainingArguments(
      output_dir=output_dir,           # output directory
      num_train_epochs=10,           # total number of training epochs
      per_device_train_batch_size=batch_size,   # batch size per device during training, can increase if memory allows
      save_steps=500,                  # number of updates steps before checkpoint saves
      save_total_limit=5,              # limit the total amount of checkpoints and deletes the older checkpoints
      warmup_steps=500,                # number of warmup steps for learning rate scheduler
      weight_decay=1e-3,               # strength of weight decay
      logging_dir='./logs',            # directory for storing logs
      logging_steps=10,
    )

    trainer = Trainer(
      model=model,                         # the instantiated 🤗 Transformers model to be trained
      args=training_args,                  # training arguments, defined above
      train_dataset=train_dataset,         # training dataset
      tokenizer=tokenizer
    )

  return trainer

    

def save_model():
    try: 
        model_dir = './'
        trainer.save_model(model_dir + 'model')
        print("saved successfully")
    except:
        print("error while saving!")
    


if __name__=='__main__':
  from datasets import load_dataset
  dataset = load_dataset("TanveerAman/AMI-Corpus-Text-Summarization")
  train_texts, train_labels = dataset['train']['Dialogue'], dataset['train']['Summaries']
  
  val_texts, val_labels = dataset['validation']['Dialogue'], dataset['validation']['Summaries']

  test_texts, test_labels = dataset['test']['Dialogue'], dataset['test']['Summaries']
  # use Pegasus Large model as base for fine-tuning
  try:
    model_name = './model/'
    train_dataset, val_dataset, test_dataset, tokenizer = prepare_data(model_name, train_texts, train_labels,val_texts,val_labels,test_texts,test_labels)
    print(len(test_texts))
    # print(test_dataset[4])
    print("load model localy!")
  except:
    model_name = 'google/pegasus-large'
    train_dataset, val_dataset, test_dataset, tokenizer = prepare_data(model_name, train_texts, train_labels,val_texts,val_labels,test_texts,test_labels)

  trainer = prepare_fine_tuning(model_name, tokenizer, train_dataset,val_dataset, freeze_encoder = False, train_layer = 2)
  trainer_org = prepare_fine_tuning(model_name, tokenizer, train_dataset, freeze_encoder = False, train_layer = 2)
  if model_name == './mode/':
        model_name = 'google/pegasus-large'
        trainer_org = prepare_fine_tuning('google/pegasus-large', tokenizer, train_dataset, freeze_encoder = False, train_layer = 2)
  print(f"seq len: {tokenizer.max_len_single_sentence}")
  torch.cuda.empty_cache()
  user_input = input("train/test?")
  if user_input == 'train':
      try:
        trainer.train()
      finally:
        print('')
        print ('My application is ending!')
        save_model()
  elif user_input == 'test':
      try:
        test_metrics = trainer.predict(test_dataset).metrics
        print("fine tuned model test results:")
        print(test_metrics)
        
        test_org_metrics = trainer_org.predict(test_dataset).metrics
        print("original model test results:")
        print(test_org_metrics)
      except Exception as exc:
        print(exc)
        print("error while testing")