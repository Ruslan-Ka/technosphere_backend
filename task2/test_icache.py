import unittest
from icache import ICache


class TestIcache(unittest.TestCase):
    def setUp(self):
        self.cache = ICache(100)
        self.cache1 = ICache(100)

    def test_get(self):
        self.cache.set('Jesse', 'Pinkman')
        self.cache.set('Walter', 'White')
        self.assertEqual(self.cache.get('Jesse'), 'Pinkman')
        self.cache.set('Jesse', 'James')
        self.assertEqual(self.cache.get('Jesse'), 'James')
        self.cache.delete('Walter')
        self.assertEqual(self.cache.get('Walter'), '')

if __name__ == '__main__':
    unittest.main()
