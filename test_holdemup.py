import unittest 
from holdemup import main

class TestStringMethods(unittest.TestCase):

    def test_main(self):
        main()

if __name__ == '__main__':
    unittest.main()