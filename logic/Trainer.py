from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
import keras.backend as K
import pandas as pd
from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard

class Trainer:
    def __init__(self, folder="../data/"):
        print("Trainer created")
        self.folder = folder
        self.__create_model()
        self.__load_data()

    def train(self):
        print("Start training")
        model_checkpoint = ModelCheckpoint(self.folder+"weights.{epoch:02d}-{val_acc:.2f}.hdf5", monitor='val_acc', verbose=1, save_best_only=False, mode='auto')
        tensor_board = TensorBoard(log_dir=self.folder+'tensorboard', histogram_freq=0,
                                  write_graph=True, write_images=False)
        self.model.fit(self.train_input, self.train_output, batch_size=32, epochs=200, verbose=1,
                       callbacks=[model_checkpoint, tensor_board])

    def __load_data(self):
        self.train_input = pd.read_csv(self.folder+'EUR_USD_train_input.csv', float_precision='round_trip').values
        self.train_input = self.train_input.reshape(self.train_input.shape[0], 128, 9)

        self.train_output = pd.read_csv(self.folder+'EUR_USD_train_output.csv', float_precision='round_trip').values

        self.test_input = pd.read_csv(self.folder+'EUR_USD_test_input.csv', float_precision='round_trip').values
        self.test_input = self.test_input.reshape(self.test_input.shape[0], 128, 9)

        self.test_output = pd.read_csv(self.folder+'EUR_USD_test_output.csv', float_precision='round_trip').values


    def __create_model(self):
        K.clear_session()
        self.model = Sequential()

        self.model.add(LSTM(64, input_shape=(128, 9), return_sequences=True))
        self.model.add(Dropout(0.2))

        self.model.add(LSTM(128, return_sequences=False))

        self.model.add(Dense(100, activation='relu'))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(50, activation='relu'))
        self.model.add(Dense(2, activation='linear'))

        self.model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

        # model = Sequential()
        #
        # model.add(LSTM(
        #     input_dim=layers[0],
        #     output_dim=layers[1],
        #     return_sequences=True))
        # model.add(Dropout(0.2))
        #
        # model.add(LSTM(
        #     layers[2],
        #     return_sequences=False))
        # model.add(Dropout(0.2))
        #
        # model.add(Dense(
        #     output_dim=layers[3]))
        # model.add(Activation("linear"))
        #
        # start = time.time()
        # model.compile(loss="mse", optimizer="rmsprop")
