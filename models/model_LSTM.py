from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding, Dropout


def model_LSTM():
    model = Sequential()

    model.add(Embedding(2048, 2, input_length=10))
    model.add(Dropout(0.15))
    model.add(LSTM(64))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model
