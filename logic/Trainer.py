from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
import keras.backend as K
import pandas as pd
from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard

class Trainer:
    def __init__(self, folder="../data/", debug_mode=False):
        print("Trainer created")
        self.folder = folder
        self.debug_mode = debug_mode
        self.__create_model()



    def train(self):
        self.__load_data()
        print("Start training")
        model_checkpoint = ModelCheckpoint("../output/weights.{epoch:02d}.hdf5", monitor='val_acc', verbose=1, save_best_only=False, mode='auto')
        tensor_board = TensorBoard(log_dir='../output/', histogram_freq=0,
                                  write_graph=True, write_images=False)#log_dir=self.folder,
        if self.debug_mode:
            self.model.fit(self.test_input, self.test_output, batch_size=16, epochs=1, verbose=1,
                           callbacks=[model_checkpoint, tensor_board], validation_split=0.05, shuffle=False)
        else:
            self.model.fit(self.train_input, self.train_output, batch_size=16, epochs=1, verbose=1,
                       callbacks=[model_checkpoint, tensor_board], validation_data=(self.test_input, self.test_output), shuffle=False)

    def predict_test_value(self, weights_path, test_number):
        self.__load_test_data()
        self.model.load_weights(weights_path)
        input_sample = self.test_input[test_number:test_number+32].reshape(32, 128, 9)
        predicted_output = self.model.predict(input_sample)
        return predicted_output, self.test_output[test_number:test_number+32]

    def predict_train_value(self, weights_path, test_number):
        self.__load_train_data()
        self.model.load_weights(weights_path)
        input_sample = self.train_input[test_number:test_number+32].reshape(32, 128, 9)
        predicted_output = self.model.predict(input_sample)
        return predicted_output, self.train_output[test_number:test_number+32]

    def evaluate_trained_model(self, weights_path):
        self.__load_test_data()
        self.model.load_weights(weights_path)
        return self.model.evaluate(self.test_input, self.test_output)

    def __load_data(self):
        print("Start loading data")
        self.__load_train_data()

        self.__load_test_data()

    def __load_train_data(self):
        print("Start loading train data")
        self.train_input = pd.read_csv(self.folder + 'EUR_USD_train_input.csv', float_precision='round_trip').values
        self.train_input = self.train_input.reshape(self.train_input.shape[0], 128, 9)
        self.train_output = pd.read_csv(self.folder + 'EUR_USD_train_output.csv', float_precision='round_trip').values

    def __load_test_data(self):
        print("Start loading test data")
        self.test_input = pd.read_csv(self.folder + 'EUR_USD_test_input.csv', float_precision='round_trip').values
        self.test_input = self.test_input.reshape(self.test_input.shape[0], 128, 9)
        self.test_output = pd.read_csv(self.folder + 'EUR_USD_test_output.csv', float_precision='round_trip').values

    def __create_model(self):
        K.clear_session()
        self.model = Sequential()

        self.model.add(LSTM(128, input_shape=(128, 9), return_sequences=True))

        self.model.add(Dropout(0.2))

        self.model.add(LSTM(128, return_sequences=True))

        self.model.add(Dropout(0.2))

        self.model.add(LSTM(128, return_sequences=False))
        #
        #
        #
        # self.model.add(Dense(100, activation='relu', kernel_initializer='normal',
        #         kernel_regularizer='l2'))
        #
        # self.model.add(Dropout(0.2))
        # self.model.add(Dense(50, activation='relu', kernel_initializer='normal',
        #         kernel_regularizer='l2'))

        self.model.add(Dense(2, activation='linear'))

        self.model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['accuracy'])

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
