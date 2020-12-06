import unittest
from ilist import Ilist

class TestIlist(unittest.TestCase):
    def setUp(self):
        self.list1 = Ilist([1,2,3,4])
        self.list2 = Ilist([2,3,4,5])
        self.list3 = Ilist([7,7])        # list3 == list2
    def test_expr(self):
        self.assertEqual(self.list1 + self.list2, [3,5,7,9])
        self.assertEqual(self.list1 + self.list3, [8,9,3,4])
        self.assertEqual(self.list1 - self.list2, [-1,-1,-1,-1])
        self.assertEqual(self.list3 - self.list1, [6,5,-3,-4])
    def test_bool(self):
        self.assertGreater(self.list2, self.list1)
        self.assertLess(self.list1, self.list3)
        self.assertEqual(self.list3, self.list2)
        self.assertNotEqual(self.list1, self.list2)

