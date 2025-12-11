import unittest

from tp_quantity.uom import USD, MWH, SCALAR


class UOMTestCase(unittest.TestCase):
    def test_numerator_and_denominator(self):
        self.assertEqual(USD, (USD / MWH).numerator)
        self.assertEqual(MWH, (USD / MWH).denominator)
        self.assertEqual(SCALAR, USD.denominator)
        self.assertEqual(SCALAR, USD.inverse.numerator)
        self.assertEqual(USD, USD.inverse.denominator)
