import pytest

from .. import Evaler, NotSafeExpression

import _ast


class NoBinaryEvaler(Evaler):
    ALLOWED_NODES = (
        _ast.Module,
        # math
        _ast.Add,
        _ast.UAdd,
        _ast.Sub,
        _ast.USub,
        _ast.Mult,
        _ast.Div,
        _ast.FloorDiv,
        _ast.Pow,
        _ast.Mod,
        # conditions
        _ast.Not,
        _ast.IfExp,
        # base expressions
        _ast.Expr,
        _ast.BinOp,
        _ast.UnaryOp,
        # structures
        _ast.Tuple,
        _ast.List,
        _ast.Dict,
        # system
        _ast.Num,
        _ast.Str,
        _ast.Name,
        _ast.Load,
        _ast.Call,  # visit_Call makes the rest
    )

    @staticmethod
    def get_allowed_nodes():
        return NoBinaryEvaler.ALLOWED_NODES

    bad_code = (
        "x ^ y",
        "~y",
        "x | y",
    )


class ListComprehensionEvaler(Evaler):
    @staticmethod
    def get_allowed_nodes():
        return (Evaler.get_allowed_nodes() +
                (_ast.comprehension, _ast.ListComp, _ast.Store,)
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
