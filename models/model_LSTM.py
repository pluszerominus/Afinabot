from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding, Dropout


def model_LSTM(token_words=25000,max_sen_len=700):
    model = Sequential()

    model.add(Embedding(token_words, 200, input_length=max_sen_len))
    model.add(Dropout(0.15))
    model.add(LSTM(64, return_sequences=True))
    model.add(LSTM(32))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model
