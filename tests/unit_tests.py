import unittest
from collections import Counter


class TestH1BCounting(unittest.TestCase):

    def test_write_top10_file(self):
        state_counter = Counter()
        occupation_counter = Counter()

        state_counter.update([])
        occupation_counter.update([])

        # out of time...

        pass

    def test_certified_application_batches(self):
        pass

    def test_read_certified_applications(self):
        pass


if __name__ == '__main__':
    unittest.main()