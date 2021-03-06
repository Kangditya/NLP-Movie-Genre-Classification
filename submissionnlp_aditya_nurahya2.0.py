# -*- coding: utf-8 -*-
"""SubmissionNLP_Aditya_Nurahya2.0

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ANRmg88sMJFHeWj5GU7QQmMXNVGR6hdj

###Import Library yang dibutuhkan
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
#split library
from sklearn.model_selection import train_test_split

#tensorflow library
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

"""###Dataset Movie Genre

#### Menggunakan dataset movie genre dari kaggle
https://www.kaggle.com/lokkagle/movie-genre-data
"""

df = pd.read_csv('/content/kaggle_movie_train.csv')
df

df['genre'].value_counts()

"""Memilih 4 Genre sebagai label"""

df = df[~df['genre'].isin(['drama','thriller','other','adventure','romance'])]
df['genre'].value_counts()

"""### Data Processing"""

df['Text'] = df['text'].map(lambda x: re.sub(r'\W+', ' ', x))
# drop kolom id dan text lama
df = df.drop(['id', 'text'], axis=1)
df.head()

genre = pd.get_dummies(df.genre)
df_genre = pd.concat([df, genre], axis=1)
df_genre = df_genre.drop(columns='genre')
df_genre.head()

text = df_genre['Text'].astype(str)
label = df_genre[['action', 'comedy','horror','sci-fi']].values

"""###Tokenizer and Modelling

split data untuk train dan test dengan 20% test_size
"""

genre_train, genre_test, label_train, label_test = train_test_split(text, label, test_size = 0.2)

tokenizer = Tokenizer(num_words=5000, oov_token='x')
tokenizer.fit_on_texts(genre_train)
tokenizer.fit_on_texts(genre_test)

seq_train = tokenizer.texts_to_sequences(genre_train)
seq_test = tokenizer.texts_to_sequences(genre_test)

pad_train = pad_sequences(seq_train)
pad_test = pad_sequences(seq_test)

"""membuat model NLP"""

from tensorflow.keras.optimizers import Adam

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=5000, output_dim=16),
    tf.keras.layers.LSTM(64),
    # tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
    # tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
    tf.keras.layers.Dense(128, activation='relu'),
    # tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(4, activation='softmax'),
])

Adam(learning_rate=0.00256, name='Adam')
model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

print(model.summary())

class myCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
      if(logs.get('accuracy')>0.925 and logs.get('val_accuracy')>0.9):
        print("\nAkurasi telah mencapai >92.5%! dan validasi akurasi >90%")
        self.model.stop_training = True
callbacks = myCallback()

num_epochs=30
history = model.fit(pad_train, label_train, epochs=num_epochs,
                    validation_data=(pad_test, label_test), verbose=2, callbacks=[callbacks])

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

plt.plot(epochs, acc,'b',label='training acc')
plt.plot(epochs, val_acc, 'r', label='validation acc')
plt.legend()
plt.show()


plt.plot(epochs, loss,'b',label='training loss')
plt.plot(epochs, val_loss, 'r', label='validation loss')
plt.legend()
plt.show()