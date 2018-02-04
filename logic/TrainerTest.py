import unittest


import logic.Trainer as lg

class TestTrainerMethods(unittest.TestCase):

    # def test_simple(self):
    #     trainer = lg.Trainer(debug_mode=True)
    #     trainer.train()

    # def test_weights_0(self):
    #     trainer = lg.Trainer()
    #     result = trainer.evaluate_trained_model("../output/weights.00.hdf5")
    #     print("epoch 1", result)
    #
    # def test_weights_1(self):
    #     trainer = lg.Trainer()
    #     result = trainer.evaluate_trained_model("../output/weights.04.hdf5")
    #     print("epoch 2", result)

    # def test_predict_sample_value(self):
    #     trainer = lg.Trainer()
    #     result = trainer.predict_test_value("../output/weights.04.hdf5", 500)
    #     print(result)

    def test_predict_sample_value_2(self):
        trainer = lg.Trainer()
        result = trainer.predict_train_value("../output/weights.04.hdf5", 1000)
        print(result)

    # def test_large(self):
    #     data_machine = lg.DataMachine(number_of_samples=200000)
    #     data_machine.prepare_data()


if __name__ == '__main__':
    unittest.main()