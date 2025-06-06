# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Linear combination represented as mapping of things to coefficients."""

from __future__ import annotations

from typing import (
    AbstractSet,
    Any,
    Callable,
    Generic,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    Mapping,
    MutableMapping,
    overload,
    TYPE_CHECKING,
    TypeVar,
    ValuesView,
)

import numpy as np
import sympy
from typing_extensions import Self

from cirq import protocols

if TYPE_CHECKING:
    import cirq

Scalar = complex | np.number
TVector = TypeVar('TVector')

TDefault = TypeVar('TDefault')


class _SympyPrinter(sympy.printing.str.StrPrinter):
    def __init__(self, format_spec: str):
        super().__init__()
        self._format_spec = format_spec

    def _print(self, expr, **kwargs):
        if expr.is_complex:
            coefficient = complex(expr)
            s = _format_coefficient(self._format_spec, coefficient)
            return s[1:-1] if s.startswith('(') else s
        return super()._print(expr, **kwargs)


def _format_coefficient(format_spec: str, coefficient: cirq.TParamValComplex) -> str:
    if isinstance(coefficient, sympy.Basic):
        printer = _SympyPrinter(format_spec)
        return printer.doprint(coefficient)
    coefficient = complex(coefficient)
    real_str = f'{coefficient.real:{format_spec}}'
    imag_str = f'{coefficient.imag:{format_spec}}'
    if float(real_str) == 0 and float(imag_str) == 0:
        return ''
    if float(imag_str) == 0:
        return real_str
    if float(real_str) == 0:
        return imag_str + 'j'
    if real_str[0] == '-' and imag_str[0] == '-':
        return f'-({real_str[1:]}+{imag_str[1:]}j)'
    if imag_str[0] in ['+', '-']:
        return f'({real_str}{imag_str}j)'
    return f'({real_str}+{imag_str}j)'


def _format_term(format_spec: str, vector: TVector, coefficient: cirq.TParamValComplex) -> str:
    coefficient_str = _format_coefficient(format_spec, coefficient)
    if not coefficient_str:
        return coefficient_str
    result = f'{coefficient_str}*{vector!s}'
    if result[0] in ['+', '-']:
        return result
    return '+' + result


def _format_terms(terms: Iterable[tuple[TVector, cirq.TParamValComplex]], format_spec: str):
    formatted_terms = [_format_term(format_spec, vector, coeff) for vector, coeff in terms]
    s = ''.join(formatted_terms)
    if not s:
        return f'{0:{format_spec}}'
    if s[0] == '+':
        return s[1:]
    return s


class LinearDict(Generic[TVector], MutableMapping[TVector, 'cirq.TParamValComplex']):
    """Represents linear combination of things.

    LinearDict implements the basic linear algebraic operations of vector
    addition and scalar multiplication for linear combinations of abstract
    vectors. Keys represent the vectors, values represent their coefficients.
    The only requirement on the keys is that they be hashable (i.e. are
    immutable and implement __hash__ and __eq__ with equal objects hashing
    to equal values).

    A consequence of treating keys as opaque is that all relationships between
    the keys other than equality are ignored. In particular, keys are allowed
    to be linearly dependent.
    """

    def __init__(
        self,
        terms: Mapping[TVector, cirq.TParamValComplex] | None = None,
        validator: Callable[[TVector], bool] | None = None,
    ) -> None:
        """Initializes linear combination from a collection of terms.

        Args:
            terms: Mapping of abstract vectors to coefficients in the linear
                combination being initialized.
            validator: Optional predicate that determines whether a vector is
                valid or not. Dictionary and linear algebra operations that
                would lead to the inclusion of an invalid vector into the
                combination raise ValueError exception. By default all vectors
                are valid.
        """
        self._has_validator = validator is not None
        self._is_valid = validator or (lambda x: True)
        self._terms: dict[TVector, cirq.TParamValComplex] = {}
        if terms is not None:
            self.update(terms)

    @classmethod
    def fromkeys(cls, vectors, coefficient=0):
        return LinearDict(
            dict.fromkeys(
                vectors,
                coefficient if isinstance(coefficient, sympy.Basic) else complex(coefficient),
            )
        )

    def _check_vector_valid(self, vector: TVector) -> None:
        if not self._is_valid(vector):
            raise ValueError(f'{vector} is not compatible with linear combination {self}')

    def clean(self, *, atol: float = 1e-9) -> Self:
        """Remove terms with coefficients of absolute value atol or less."""
        negligible = [
            v
            for v, c in self._terms.items()
            if not isinstance(c, sympy.Basic) and abs(complex(c)) <= atol
        ]
        for v in negligible:
            del self._terms[v]
        return self

    def copy(self) -> Self:
        factory = type(self)
        return factory(self._terms.copy())

    def keys(self) -> KeysView[TVector]:
        snapshot = self.copy().clean(atol=0)
        return snapshot._terms.keys()

    def values(self) -> ValuesView[cirq.TParamValComplex]:
        snapshot = self.copy().clean(atol=0)
        return snapshot._terms.values()

    def items(self) -> ItemsView[TVector, cirq.TParamValComplex]:
        snapshot = self.copy().clean(atol=0)
        return snapshot._terms.items()

    @overload
    def update(
        self, other: Mapping[TVector, cirq.TParamValComplex], **kwargs: cirq.TParamValComplex
    ) -> None:
        pass

    @overload
    def update(
        self,
        other: Iterable[tuple[TVector, cirq.TParamValComplex]],
        **kwargs: cirq.TParamValComplex,
    ) -> None:
        pass

    @overload
    def update(self, *args: Any, **kwargs: cirq.TParamValComplex) -> None:
        pass

    def update(self, *args, **kwargs):
        terms = dict()
        terms.update(*args, **kwargs)
        for vector, coefficient in terms.items():
            if isinstance(coefficient, sympy.Basic):
                coefficient = sympy.simplify(coefficient)
                if coefficient.is_complex:
                    coefficient = complex(coefficient)
            self[vector] = coefficient
        self.clean(atol=0)

    @overload
    def get(self, vector: TVector) -> cirq.TParamValComplex:
        pass

    @overload
    def get(self, vector: TVector, default: TDefault) -> cirq.TParamValComplex | TDefault:
        pass

    def get(self, vector, default=0):
        if self._terms.get(vector, 0) == 0:
            return default
        return self._terms.get(vector)

    def __contains__(self, vector: Any) -> bool:
        return vector in self._terms and self._terms[vector] != 0

    def __getitem__(self, vector: TVector) -> cirq.TParamValComplex:
        return self._terms.get(vector, 0)

    def __setitem__(self, vector: TVector, coefficient: cirq.TParamValComplex) -> None:
        self._check_vector_valid(vector)
        if coefficient != 0:
            self._terms[vector] = coefficient
            return
        if vector in self._terms:
            del self._terms[vector]

    def __delitem__(self, vector: TVector) -> None:
        if vector in self._terms:
            del self._terms[vector]

    def __iter__(self) -> Iterator[TVector]:
        snapshot = self.copy().clean(atol=0)
        return snapshot._terms.__iter__()

    def __len__(self) -> int:
        return len([v for v, c in self._terms.items() if c != 0])

    def __iadd__(self, other: Self) -> Self:
        for vector, other_coefficient in other.items():
            old_coefficient = self._terms.get(vector, 0)
            new_coefficient = old_coefficient + other_coefficient
            self[vector] = new_coefficient
        return self.clean(atol=0)

    def __add__(self, other: Self) -> Self:
        result = self.copy()
        result += other
        return result

    def __isub__(self, other: Self) -> Self:
        for vector, other_coefficient in other.items():
            old_coefficient = self._terms.get(vector, 0)
            new_coefficient = old_coefficient - other_coefficient
            self[vector] = new_coefficient
        self.clean(atol=0)
        return self

    def __sub__(self, other: Self) -> Self:
        result = self.copy()
        result -= other
        return result

    def __neg__(self) -> Self:
        factory = type(self)
        return factory({v: -c for v, c in self.items()})

    def __imul__(self, a: cirq.TParamValComplex) -> Self:
        for vector in self:
            self._terms[vector] *= a
        self.clean(atol=0)
        return self

    def __mul__(self, a: cirq.TParamValComplex) -> Self:
        result = self.copy()
        result *= a
        return result.copy()

    def __rmul__(self, a: cirq.TParamValComplex) -> Self:
        return self.__mul__(a)

    def __truediv__(self, a: cirq.TParamValComplex) -> Self:
        return self.__mul__(1 / a)

    def __bool__(self) -> bool:
        return not all(c == 0 for c in self._terms.values())

    def __eq__(self, other: Any) -> bool:
        """Checks whether two linear combinations are exactly equal.

        Presence or absence of terms with coefficients exactly equal to
        zero does not affect outcome.

        Not appropriate for most practical purposes due to sensitivity to
        numerical error in floating point coefficients. Use cirq.approx_eq()
        instead.
        """
        if not isinstance(other, LinearDict):
            return NotImplemented

        all_vs = set(self.keys()) | set(other.keys())
        return all(self[v] == other[v] for v in all_vs)

    def __ne__(self, other: Any) -> bool:
        """Checks whether two linear combinations are not exactly equal.

        See __eq__().
        """
        if not isinstance(other, LinearDict):
            return NotImplemented

        return not self == other

    def _approx_eq_(self, other: Any, atol: float) -> bool:
        """Checks whether two linear combinations are approximately equal."""
        if not isinstance(other, LinearDict):
            return NotImplemented

        all_vs = set(self.keys()) | set(other.keys())
        return all(abs(self[v] - other[v]) < atol for v in all_vs)

    def __format__(self, format_spec: str) -> str:
        terms = [(v, self[v]) for v in sorted(self.keys(), key=str)]
        return _format_terms(terms=terms, format_spec=format_spec)

    def __repr__(self) -> str:
        coefficients = dict(self)
        class_name = self.__class__.__name__
        return f'cirq.{class_name}({coefficients!r})'

    def __str__(self) -> str:
        return self.__format__('.3f')

    def _repr_pretty_(self, p: Any, cycle: bool) -> None:
        if cycle:
            class_name = self.__class__.__name__
            p.text(f'{class_name}(...)')
        else:
            p.text(str(self))

    def _json_dict_(self) -> dict[Any, Any]:
        if self._has_validator:
            raise ValueError('LinearDict with a validator is not json serializable.')
        return {
            'keys': [k for k in self._terms.keys()],
            'values': [v for v in self._terms.values()],
        }

    @classmethod
    def _from_json_dict_(cls, keys, values, **kwargs):
        return cls(terms=dict(zip(keys, values)))

    def _is_parameterized_(self) -> bool:
        return any(protocols.is_parameterized(v) for v in self._terms.values())

    def _parameter_names_(self) -> AbstractSet[str]:
        return set(name for v in self._terms.values() for name in protocols.parameter_names(v))

    def _resolve_parameters_(self, resolver: cirq.ParamResolver, recursive: bool) -> LinearDict:
        result = self.copy()
        result.update(
            {
                k: protocols.resolve_parameters(v, resolver, recursive)
                for k, v in self._terms.items()
            }
        )
        return result
