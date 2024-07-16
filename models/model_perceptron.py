from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Embedding, Dropout


def model_LSTM(token_words=25000,max_sen_len=700):
    model = Sequential()

    model.add(Embedding(token_words, 2, input_length=max_sen_len))

    model.add(Flatten())

    model.add(Dropout(0.3))
    model.add(Dense(750, activation="relu"))
    model.add(Dropout(0.3))
    model.add(Dense(500, activation="relu"))
    model.add(Dropout(0.3))
    model.add(Dense(250, activation="relu"))
    model.add(Dense(1, activation="sigmoid"))

    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

    return model