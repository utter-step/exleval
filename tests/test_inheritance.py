import _ast

import pytest

from exleval import Evaler, NotSafeExpression

class NoBinaryEvaler(Evaler):
    def get_allowed_nodes(self):
        return super(type(self), self).get_allowed_nodes() - set(
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
    def get_allowed_nodes(self):
        return super(type(self), self).get_allowed_nodes() | set(
            (_ast.comprehension, _ast.ListComp, _ast.Store,)
        )

    good_code = (
        "[x for x in range(10)]",
        "[x ** 2 for x in xrange(10)]",
        "[10 - x for x in some_iterable]",
    )


class OnlyNamesAndAdditionEvaler(Evaler):
    ALLOWED_NODES = set((
        _ast.Module,
        _ast.Expr,

        _ast.BinOp,
        _ast.Add,

        _ast.Num,
        _ast.Name,
        _ast.Load,
    ))

    def get_allowed_nodes(self):
        return self.ALLOWED_NODES

    test_code = (
        ("4 + 3", True),
        ("x + 2", True),
        ("5 + x", True),
        ("4 - 3", False),
        ("x - 5", False),
        ("x / 4", False),
    )


nb_evaler = NoBinaryEvaler()
lc_evaler = ListComprehensionEvaler((range, xrange))
ona_evaler = OnlyNamesAndAdditionEvaler()


@pytest.mark.parametrize('expr', NoBinaryEvaler.bad_code)
def test_NoBinary(expr):
    with pytest.raises(NotSafeExpression):
        nb_evaler.eval(expr,
                       {"x": 5,
                        "y": 6}
                       )


@pytest.mark.parametrize('expr', ListComprehensionEvaler.good_code)
def test_ListComprehencion(expr):
    lc_evaler.eval(expr, {"some_iterable": (x ** 0.5 for x in xrange(10))})


@pytest.mark.parametrize('expr,good', OnlyNamesAndAdditionEvaler.test_code)
def test_addition_only(expr, good):
    if good:
        ona_evaler.eval(expr, {"x": 5})
    else:
        with pytest.raises(NotSafeExpression):
            ona_evaler.eval(expr, {"x": 5})
