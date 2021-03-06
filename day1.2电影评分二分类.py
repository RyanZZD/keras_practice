from keras import layers
from keras import models
from keras.datasets import imdb
import numpy as np

#准备数据
(train_data,train_labels), (test_data, test_labels)=imdb.load_data(num_words=10000)
def vectorize_sequences(sequences, dimension=10000):
    '''
    :param sequences:
    :param dimension:
    :return: 数据向量化
    '''
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1
    return results

x_train = vectorize_sequences(train_data)
x_test = vectorize_sequences(test_data)

y_train = np.asarray(train_labels).astype('float32')
y_test = np.asarray(test_labels).astype('float32')

models = models.Sequential()
models.add(layers.Dense(16, activation='relu', input_shape=(10000,)))
models.add(layers.Dense(16,activation='relu'))
models.add(layers.Dense(1, activation='sigmoid'))
'''
from keras import optimizers
models.compile(optimizer=optimizers.RMSprop(lr=0.001),
                loss='binary_crossentropy',
                metrics=['accuracy'])

from keras import losses
from keras import metrics

models.compile(optimizer=optimizers.RMSprop(lr=0.001),
                loss=losses.binary_crossentropy,
                metrics=[metrics.binary_accuracy])
'''
# 留出验证集
x_val = x_train[:10000]
partial_x_train = x_train[10000:]

y_val = y_train[:10000]
partial_y_train = y_train[10000:]

models.compile(optimizer='rmsprop',
                loss='binary_crossentropy',
                metrics=['accuracy'])

history = models.fit(partial_x_train,
                     partial_y_train,
                     epochs=20,
                     batch_size=512,
                     validation_data=(x_val, y_val))

history_dict = history.history
print(history_dict.keys())

import matplotlib.pyplot as plt

loss_values = history_dict['loss']
val_loss_values = history_dict['val_loss']

epochs = range(1, len(loss_values)+1)
plt.plot(epochs, loss_values, 'bo', label='Training loss')
plt.plot(epochs, val_loss_values, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()
