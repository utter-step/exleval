import pytest

from .. import Evaler, NotSafeExpression

import _ast


class NoBinaryEvaler(Evaler):
    @staticmethod
    def get_allowed_nodes():
        return set(Evaler.get_allowed_nodes()) - set(
            (_ast.LShift,
             _ast.RShift,
             _ast.BitAnd,
             _ast.BitOr,
             _ast.BitXor,
             _ast.Invert,)
        )

    bad_code = (
        "x ^ y",
        "~y",
        "x | y",
    )


class ListComprehensionEvaler(Evaler):
    @staticmethod
    def get_allowed_nodes():
        return (Evaler.get_allowed_nodes() |
                set((_ast.comprehension, _ast.ListComp, _ast.Store,))
                )

    good_code = (
        "[x for x in range(10)]",
        "[x ** 2 for x in xrange(10)]",
        "[10 - x for x in some_iterable]",
    )

nb_evaler = NoBinaryEvaler()
lc_evaler = ListComprehensionEvaler((range, xrange))


@pytest.mark.parametrize('expr', NoBinaryEvaler.bad_code)
def test_NoBinary(expr):
    with pytest.raises(NotSafeExpression):
        nb_evaler.eval(expr,
                       {"x": 5,
                        "y": 6}
                       )


@pytest.mark.parametrize('expr', ListComprehensionEvaler.good_code)
def test_ListComprehencion(expr):
    lc_evaler.eval(expr,
                   {"some_iterable": (x ** 0.5 for x in xrange(10))}
                   )
