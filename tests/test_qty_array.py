import unittest

import numpy as np

from tp_quantity.quantity import Qty
from tp_quantity.quantity_array import QtyArray
from tp_quantity.uom import USD, SCALAR, MWH, MT


class QtyArrayTestCase(unittest.TestCase):

    def test_str(self):
        self.assertEqual(
            '[1.00, 1.00 (0.00), 1.00] USD', str(QtyArray(1, USD))
        )
        self.assertEqual(
            '[1.00, 2.00 (0.82), 3.00] USD',
            str(QtyArray([1, 2, 3], USD)),
        )
        self.assertEqual(
            '[1.00, 2.00 (0.82), 3.00]',
            str(QtyArray([1, 2, 3], SCALAR)),
        )

    def _check_close(self, q1: QtyArray, q2: QtyArray):
        self.assertTrue(q1.almost_equals(q2))

    def test_construction(self):
        self._check_close(
            QtyArray(1, USD),
            QtyArray([1], USD)
        )
        self._check_close(
            QtyArray(1, USD),
            QtyArray(np.asarray([1]), USD)
        )
        self.assertNotEqual(
            QtyArray(1, USD),
            QtyArray(1, MWH),
        )

    def test_multiplication(self):
        self._check_close(
            QtyArray(2, USD / MWH) * QtyArray(3, MWH),
            QtyArray(6, USD)
        )
        self._check_close(
            QtyArray(2, USD / MWH) * Qty(3, MWH),
            QtyArray(6, USD)
        )
        self._check_close(
            QtyArray(2, MWH.inverse) * QtyArray(3, MWH),
            QtyArray(6, SCALAR)
        )
        self._check_close(
            QtyArray([6, 12], MWH) / Qty(3, MWH),
            QtyArray([2.0, 4.0], SCALAR)
        )
        self._check_close(
            QtyArray([6, 12], MWH) / QtyArray([3, 6], MWH),
            QtyArray([2.0, 2.0], SCALAR)
        )

    def test_addition(self):
        self._check_close(
            QtyArray(3, USD) + Qty(2, USD),
            QtyArray(5, USD)
        )
        self._check_close(
            QtyArray([3, 4], USD) + QtyArray([2, 1], USD),
            QtyArray([5, 5], USD)
        )
        self._check_close(
            QtyArray([3, 4], USD) - QtyArray([2, 1], USD),
            QtyArray([1, 3], USD)
        )

    def test_negation(self):
        self._check_close(
            -QtyArray(3, USD),
            QtyArray(-3, USD)
        )
