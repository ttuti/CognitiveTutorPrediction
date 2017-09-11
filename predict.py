from keras.layers import Input, Dense, Activation, Flatten
from keras.models import Sequential
import numpy as np
import pandas as pd 
from keras.utils.np_utils import to_categorical


raw_data = pd.DataFrame.from_csv('format_two.tsv', sep='\t')
raw_train = raw_data.iloc[:-5, :]
raw_test = raw_data.iloc[-5:, :]

# 24, 5
x_train = raw_train.iloc[:, :-1].values
# 24, 1
y_train = raw_train.iloc[:, -1].values

x_test = raw_test.iloc[:, :-1].values
y_test = raw_test.iloc[:, -1].values

print(type(x_train))

# from class example!

# # tensors
# inputs = Input(shape=(24,5))

# # layer instance
# x = Dense(24, activation='relu')(inputs)
# x = Dense(24, activation='relu')(x)
# x = Dense(24, activation='relu')(x)

# predictions = Dense(24, activation='softmax')(x)
# model = Model(inputs=inputs, outputs=predictions)

model = Sequential()
model.add(Dense(units=64, activation='relu', input_dim=5))
model.add(Dense(units=32, activation='relu'))
model.add(Dense(units=64, activation='softmax'))
model.add(Dense(units=1, activation='sigmoid'))

# model.add(Dense(units=5))
# model.add(Activation('softmax'))

model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=100, batch_size=10)

model.summary()

loss_and_metrics = model.evaluate(x_test, y_test)

print('Loss and Metrics: ', loss_and_metrics)
print('Accuracy: ', loss_and_metrics[1]*100, "%")

classes = model.predict(x_test)

print('Test Class predictions: ', classes)

predictions = [1 if entry > 0.5 else 0 for entry in model.predict(raw_data.iloc[:, :-1].values).flatten()]
results = pd.DataFrame(data={'Anon Student Id': raw_data.index, 'r5': predictions})
results.to_csv('predictions.tsv', sep='\t', index=0)