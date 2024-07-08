from tensorflow.keras import utils
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import matplotlib.pyplot as plt
from models import model_LSTM


def preprocessing(data):
    for it in range(len(data[0])):
        temp = list(data[0][it])
        for i in range(len(temp)):
            w = ord(temp[i])
            if w < 1040:
                w = 0
                temp.pop(i)
                temp.insert(0, np.dtype('int32').type(w))
            else:
                temp[i] = np.dtype('int32').type(w)
        data[0][it] = temp
    data[0] = pad_sequences(data[0], 10)
    return data


def plot_history(history):
    plt.plot(history.history['accuracy'], label='Доля верных ответов на обучающем наборе')
    plt.plot(history.history['val_accuracy'], label='Доля верных ответов на проверочном наборе')
    plt.xlabel('Эпоха обучения')
    plt.ylabel('Доля верных ответов')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    data_path = Path(work, "dataset", "Word.csv")
    train_data = pd.read_csv(data_path, delimiter=";", header=None, names=['Class', 'Sentence'], encoding='utf-8')
    # Подготовка данных для обучения нейросетью
    train_data = preprocessing(train_data.to_numpy()[0])
    # Создание модели нейросети
    model = model_LSTM.model_LSTM()
    # Компиляция модели нейросети
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    # Обучения нейросети
    history = model.fit(train_data[0], train_data[1], epochs=10, batch_size=256, validation_split=0.2)
    # Вывод графика успешности обучения
    plot_history(history)
    # Сохранение модели нейросети
    model.save('LSTM_model.h5')
