# -*- coding: utf-8 -*-
"""Chinese Tokenizer CKIP

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fZAZAXQfRWYPj5m9aQ0ZjSQCz30yjuJ7

# CKIP transformers
[ckip台灣中央研究院](https://pypi.org/project/ckip-transformers/)

## 1 . Installation
"""

pip install -U ckip-transformers

"""## 2 . Import module"""

from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger, CkipNerChunker

"""## 3 . Load models

* We provide three levels (1–3) of drivers. Level 1 is the fastest, and level 3 (default) is the most accurate.
* 我們的工具分為三個等級（1—3）。等級一最快，等級三（預設值）最精準。
"""

# Initialize drivers
ws_driver  = CkipWordSegmenter(level=3)
pos_driver = CkipPosTagger(level=3)
ner_driver = CkipNerChunker(level=3)

"""* One may also load their own checkpoints using our drivers.
* 也可以運用我們的工具於自己訓練的模型上。
"""

# Initialize drivers with custom checkpoints
ws_driver  = CkipWordSegmenter(model_name='path_to_your_model')
pos_driver = CkipPosTagger(model_name='path_to_your_model')
ner_driver = CkipNerChunker(model_name='path_to_your_model')

# Use CPU
ws_driver = CkipWordSegmenter(device=-1)

"""## 4 . Run pipeline"""

# Input text
text = [
   '我是從韓國首爾來的韓文老師。',
   '在首爾,最多外國人聚集的地方大概就是梨泰院了,說到來韓國的外國人的話,一定多少都曾聽過或去過梨泰院。',
   '聽說長壽村的老人們喜歡吃大醬湯和水煮豬肉。'
]

# Run pipeline
ws  = ws_driver(text)
pos = pos_driver(ws)
ner = ner_driver(text)

# Enable sentence segmentation
ws  = ws_driver(text, use_delim=True)
ner = ner_driver(text, use_delim=True)

# Disable sentence segmentation
pos = pos_driver(ws, use_delim=False)

# Use new line characters and tabs for sentence segmentation
pos = pos_driver(ws, delim_set='\n\t')

"""You may specify batch_size and max_length to better utilize you machine resources."""

# Sets the batch size and maximum sentence length
ws = ws_driver(text, batch_size=256, max_length=500)

"""## 5 . Show results"""

# Pack word segmentation and part-of-speech results
def pack_ws_pos_sentece(sentence_ws, sentence_pos):
   assert len(sentence_ws) == len(sentence_pos)
   res = []
   for word_ws, word_pos in zip(sentence_ws, sentence_pos):
      res.append(f'{word_ws}({word_pos})')
   return '\u3000'.join(res)

# Show results
for sentence, sentence_ws, sentence_pos, sentence_ner in zip(text, ws, pos, ner):
   print(sentence)
   print(pack_ws_pos_sentece(sentence_ws, sentence_pos))
   for entity in sentence_ner:
      print(entity)
   print()