import unittest


import logic.DataMachine as lg

class TestStringMethods(unittest.TestCase):

    def test_simple(self):
        data_machine = lg.DataMachine()
        data_machine.prepare_data()

    # def test_large(self):
    #     data_machine = lg.DataMachine(number_of_samples=200000)
    #     data_machine.prepare_data()


if __name__ == '__main__':
    unittest.main()