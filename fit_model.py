from tensorflow.keras import utils
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import matplotlib.pyplot as plt
from models import model_LSTM,model_perceptron
from pathlib import Path


def preprocessing_LSTM(data):
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

def preprocessing_perceptron(data,max_len=700):
    tokenizer_path = Path.cwd() / "Tokenizer.pickle"
    sentence = train_data['Sentence']
    mark = train_data['Class']

    with open(tokenizer_path, "rb") as r_file:
        tokenizer = pickle.load(r_file)

    # Преобразуем текст в вектор кодов
    sent_to_seq = tokenizer.texts_to_sequences(sentence)
    # Обрезаем лишние слова
    sent_to_seq = pad_sequences(sent_to_seq, maxlen=max_len)

    return mark.to_numpy(),sent_to_seq


def plot_history(history):
    plt.plot(history.history['accuracy'], label='Доля верных ответов на обучающем наборе')
    plt.plot(history.history['val_accuracy'], label='Доля верных ответов на проверочном наборе')
    plt.xlabel('Эпоха обучения')
    plt.ylabel('Доля верных ответов')
    plt.legend()
    plt.show()

def main(dataset_file="word_dataset.csv",model_type="LSTM",epoch=10,batch_size=32,val_split=0.2):
    # Путь до набора данных
    data_path = Path.cwd() / "dataset" / dataset_file
    # Путь для сохранения лучшей модели
    model_save_path = Path.cwd() / "trained_models" / f"best_{model_type}_model.h5"
    # Чтение данных
    train_data = pd.read_csv(data_path, delimiter=";", header=None, names=['Class', 'Sentence'], encoding='utf-8')

    if model_type == "LSTM":
        # Подготовка данных для обучения нейросетью
        train_data = preprocessing_LSTM(train_data.to_numpy()[0])
        # Создание модели нейросети
        model = model_LSTM.model_LSTM()
        # Компиляция модели нейросети
    elif model_type == "Perceptron":
        # Подготовка данных для обучения нейросетью
        train_data = preprocessing_perceptron(train_data)
        # Создание модели нейросети
        model = model_perceptron.model_perceptron()
    else:
        print("Выбрана неверная модель")
        return 0

    callback = ModelCheckpoint(model_save_path, monitor="val_accuracy", save_best_only=True, verbose=1)
    # Компиляция модели нейросети
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    # Обучения нейросети
    history = model.fit(train_data[1], train_data[0],
                        epochs=epoch,batch_size=batch_size,
                        validation_split=val_split,callback=callback)

    # Вывод графика успешности обучения
    plot_history(history)
    # Сохранение модели нейросети
    model.save(Path.cwd() / "trained_models" / f"last_{model_type}_model.h5")

if __name__ == '__main__':
    main()

