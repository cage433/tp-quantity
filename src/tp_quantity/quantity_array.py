from numbers import Number

import numpy as np
from numpy import ndarray
from tp_utils.type_utils import checked_type

from tp_quantity.quantity import Qty
from tp_quantity.uom import UOM, SCALAR


class QtyArray:
    def __init__(self, values, uom: UOM):
        if isinstance(values, Number):
            self.values: ndarray = np.asarray([values])
        else:
            self.values: ndarray = np.asarray(values)
        self.uom: UOM = checked_type(uom, UOM)

    def __str__(self):
        low = self.values.min()
        high = self.values.max()
        mean = self.values.mean()
        std = self.values.std()
        text = f"[{low:1.2f}, {mean:1.2f} ({std:1.2f}), {high:1.2f}]"
        if self.uom == SCALAR:
            return text
        return f"{text} {self.uom}"

    def __repr__(self):
        return self.__str__()

    def almost_equals(self, other, tol = 1e-6) -> bool:
        return (isinstance(other, QtyArray) and self.values.shape == other.values.shape and self.uom == other.uom
                and abs(self.values - other.values).max() < tol)

    @property
    def shape(self):
        return self.values.shape

    @property
    def mean(self) -> Qty:
        return Qty(self.values.mean(), self.uom)

    @property
    def std(self) -> Qty:
        return Qty(self.values.std(), self.uom)

    @property
    def std_err(self) -> Qty:
        return Qty(self.values.std() / np.sqrt(self.values.size), self.uom)

    def __mul__(self, other) -> 'QtyArray':
        checked_type(other, (Qty, QtyArray))
        if isinstance(other, Qty):
            return QtyArray(self.values * other.value, self.uom * other.uom)
        assert self.shape == other.shape, f"Mismatching shapes {self.shape} vs {other.shape}"
        return QtyArray(self.values * other.values, self.uom * other.uom)


    def __add__(self, other) -> 'QtyArray':
        checked_type(other, (Qty, QtyArray))
        if self.uom != other.uom:
            raise ValueError(f"Cannot add Qtys with different uom, {self.uom} vs {other.uom}")
        if isinstance(other, Qty):
            return QtyArray(self.values + other.value, self.uom)
        assert self.shape == other.shape, f"Mismatching shapes {self.shape} vs {other.shape}"
        return QtyArray(self.values + other.values, self.uom)

    def negate(self) -> 'QtyArray':
        return QtyArray(self.values * -1, self.uom)

    def __sub__(self, other) -> 'QtyArray':
        checked_type(other, (Qty, QtyArray))
        return self + other.negate()

    def __truediv__(self, other) -> 'QtyArray':
        checked_type(other, (Qty, QtyArray))
        if isinstance(other, Qty):
            return QtyArray(self.values / other.value, self.uom / other.uom)
        assert self.shape == other.shape, f"Mismatching shapes {self.shape} vs {other.shape}"
        return QtyArray(self.values / other.values, self.uom / other.uom)

    @property
    def inverse(self):
        return QtyArray(1.0 / self.values, self.uom.inverse)
