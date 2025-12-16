import unittest

from tp_quantity.quantity import Qty
from tp_quantity.uom import USD, SCALAR, MWH, MT


class QtyTestCase(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(Qty(1, USD)), '1 USD')
        self.assertEqual(str(Qty(1.5, SCALAR)), '1.5')
        self.assertEqual(str(Qty(1, SCALAR / USD)), '1 USD^-1')
        self.assertEqual(str(Qty(1, USD.inverse)), '1 USD^-1')
        self.assertEqual(str(Qty(1, USD / MWH)), '1 USD / MWH')
        self.assertEqual(str(Qty(1, USD * MT / MWH)), '1 MT USD / MWH')
        self.assertEqual(str(Qty(1.2344, USD * MT / MWH)), '1.234 MT USD / MWH')
        self.assertEqual(str(Qty(1.2346, USD * MT / MWH)), '1.235 MT USD / MWH')

    def test_fmt(self):
        self.assertEqual('1.123 USD', Qty(1.1234, USD).fmt(n_dp=3))
        self.assertEqual('1.12 USD', Qty(1.1234, USD).fmt(n_dp=2))
        self.assertEqual('1.1 USD', Qty(1.1, USD).fmt(n_dp=2))

    def test_multiply(self):
        self.assertEqual(
            Qty(2, USD / MWH) * Qty(3, MWH),
            Qty(6, USD)
        )
        self.assertEqual(
            Qty(2, USD / MWH) * 3,
            Qty(6, USD / MWH)
        )
        self.assertEqual(
            Qty(2, MWH.inverse) * Qty(3, MWH),
            Qty(6, SCALAR)
        )

    def test_divide(self):
        self.assertEqual(
            Qty(6, USD * MWH) / Qty(3, MWH),
            Qty(2, USD)
        )
        self.assertEqual(
            Qty(6, USD * MWH) / 3,
            Qty(2, USD * MWH)
        )
        self.assertEqual(
            Qty(6, SCALAR) / Qty(3, MWH),
            Qty(2, MWH.inverse)
        )

    def test_add(self):
        self.assertEqual(
            Qty(3, USD) + Qty(2, USD),
            Qty(5, USD)
        )

    def test_minus(self):
        self.assertEqual(
            Qty(3, USD) - Qty(2, USD),
            Qty(1, USD)
        )

    # noinspection PyTypeChecker
    def test_ordering(self):
        self.assertLess(Qty(1, USD), Qty(2, USD))
        self.assertLessEqual(Qty(1, USD), Qty(2, USD))
        self.assertLessEqual(Qty(2, USD), Qty(2, USD))
        self.assertGreater(Qty(2, USD), Qty(1, USD))
        self.assertGreaterEqual(Qty(2, USD), Qty(1, USD))

        self.assertEqual(Qty(20, USD), max(Qty(20, USD), Qty(10, USD)))
        self.assertEqual(Qty(20, USD), max(Qty(10, USD), Qty(20, USD)))

    def test_abs(self):
        self.assertEqual(Qty(-3, USD).abs, Qty(3, USD))
        self.assertEqual(Qty(3, USD).abs, Qty(3, USD))

    def test_to_qty(self):
        self.assertEqual(Qty(3, SCALAR), Qty.to_qty(3))

    def test_negate(self):
        self.assertEqual(-Qty(3, SCALAR), Qty(-3, SCALAR))
        self.assertEqual(-Qty(-3, SCALAR), Qty(3, SCALAR))
        self.assertEqual(-Qty(0, SCALAR), Qty(0, SCALAR))
