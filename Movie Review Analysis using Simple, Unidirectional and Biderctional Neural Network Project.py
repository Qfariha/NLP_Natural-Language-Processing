

import tensorflow as tf
print(tf.__version__)

# Commented out IPython magic to ensure Python compatibility.

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
# %matplotlib inline
# Train test split
from sklearn.model_selection import train_test_split
# Text pre-processing
import tensorflow as tf
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.callbacks import EarlyStopping
# Modeling
from keras.models import Sequential
from keras.layers import LSTM, GRU, Dense, Embedding, Dropout, GlobalAveragePooling1D, Flatten, SpatialDropout1D, Bidirectional

movie_rev = pd.read_csv('/content/drive/MyDrive/NEW/IMDB Dataset.csv')
print(movie_rev['review'])

print(movie_rev.isnull().values.any())
print(movie_rev['sentiment'].value_counts())

movie_rev.describe()

movie_rev.groupby('sentiment').describe().T

X=[]
sentences=list(movie_rev['review'])
for sen in sentences:
  X.append(sen)

y=movie_rev['sentiment']
y=np.array(list(map(lambda x: 1 if x=='positive' else 0,y)))

X_train,X_test,y_train,y_test= train_test_split(X,y,test_size=.20,random_state=42)

#Word to index dictionary
#word=key and index=val

word_tokenizer=Tokenizer()
word_tokenizer.fit_on_texts(X_train)

X_train=word_tokenizer.texts_to_sequences(X_train)
X_test=word_tokenizer.texts_to_sequences(X_test)

vocab_size=len(word_tokenizer.word_index)+1
vocab_size

#padding to fix length


maxlen=256
X_train=pad_sequences(X_train,padding='post',maxlen=maxlen)
X_test=pad_sequences(X_test,padding='post',maxlen=maxlen)

y_train = y_train.reshape(-1, 1)
y_test = y_test.reshape(-1, 1)

from numpy import asarray
from numpy import zeros

embeddings_dict= dict()
glove=open('/content/drive/MyDrive/NEW/glove.6B.100d.txt',encoding='utf8')

for line in glove:
  records=line.split()
  word=records[0]
  vector_dimensions=asarray(records[1:],dtype='float32')
  embeddings_dict[word]=vector_dimensions
glove.close()

embedding_matrix=zeros((vocab_size,100))
for word,idx in word_tokenizer.word_index.items():
  embedding_vector=embeddings_dict.get(word)
  if embedding_vector is not None:
    embedding_matrix[idx]=embedding_vector

embedding_matrix.shape

snn_model = Sequential()
embedding_layer=Embedding(vocab_size,100,weights=[embedding_matrix],input_length = maxlen,trainable=False)
snn_model.add(embedding_layer)
snn_model.add(Dense(10, activation='relu'))
#snn_model.add(Flatten()) #without this, gives error
snn_model.add(Dense(1, activation='sigmoid'))


# Compile the model
snn_model.compile(loss = 'binary_crossentropy', optimizer = 'adam' , metrics = ['accuracy'])

snn_model.summary()

history = snn_model.fit(X_train,y_train,batch_size=128,epochs=20,verbose=2,validation_split=.2)

from keras.backend import clear_session
clear_session()

train_dense_results = snn_model.evaluate(X_train, np.asarray(y_train), verbose=2)
valid_dense_results = snn_model.evaluate(X_test, np.asarray(y_test), verbose=2)
print(f'Train accuracy for snn: {train_dense_results[1]*100:0.2f}')
print(f'Test accuracy for snn: {valid_dense_results[1]*100:0.2f}')

model1 = Sequential()

#Embedding layer
embedding_layer = Embedding(vocab_size, 100, input_length=maxlen)
model1.add(embedding_layer)
#Replacing the first Dense layer with a unidirectional LSTM layer
model1.add(LSTM(10))
# Output layer
model1.add(Dense(1, activation='sigmoid'))

model1.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model1.summary()

history = model1.fit(X_train,y_train,batch_size=128,epochs=20,verbose=2,validation_split=.2)

from keras.backend import clear_session
clear_session()

train_dense_results = model1.evaluate(X_train, np.asarray(y_train), verbose=2)
valid_dense_results = model1.evaluate(X_test, np.asarray(y_test), verbose=2)
print(f'Train accuracy for unidirectional LSTM: {train_dense_results[1]*100:0.2f}')
print(f'Test accuracy for unidirectional LSTM: {valid_dense_results[1]*100:0.2f}')

model2 = Sequential()

#Embedding layer
embedding_layer = Embedding(vocab_size, 100, input_length=maxlen)
model2.add(embedding_layer)
#Replacing the first Dense layer with a unidirectional LSTM layer
model2.add(Bidirectional(LSTM(10)))
# Output layer
model2.add(Dense(1, activation='sigmoid'))

model2.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model2.summary()

history = model2.fit(X_train,y_train,batch_size=128,epochs=20,verbose=2,validation_split=.2)

from keras.backend import clear_session
clear_session()

train_dense_results = model2.evaluate(X_train, np.asarray(y_train), verbose=2)
valid_dense_results = model2.evaluate(X_test, np.asarray(y_test), verbose=2)
print(f'Train accuracy for bidirectional LSTM: {train_dense_results[1]*100:0.2f}')
print(f'Test accuracy for bidirectional LSTM: {valid_dense_results[1]*100:0.2f}')