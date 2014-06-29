import pytest
from math import sqrt

from .. import Evaler, NotSafeExpression

good_code = (
    "-x",
    "x + 6",
    "x - y + 3",
    "x ** 5",
    "x << y",
    "y >> x",
    "a < 5",
    "a <= 5.4",
    "a > x",
    "a >= x",
    "a == y",
    "sqrt(x)",
    "a != sqrt(y)",
    "x ** y",
    "5 if x else y",
    "5 < a < 6",
    "a < 4 and a > 5",
    "min(1, 4, 3)",
    "max(1, 3, 2)",
    "abs(-2)",
    "min(abs(-2), max(abs(-4), sqrt(6)))",
)

bad_code = (
    'SafeEvaler((min, max)).eval("min(1, 3)")',
    's = "string"',
    's.startswith("str")',
    's.__name__',
    'eval("print 3")',
    'print 6',
    'max(eval("2"), 3)',
)

very_bad_code = ("""
(lambda fc=(
    lambda n: [
        c for c in
            ().__class__.__bases__[0].__subclasses__()
            if c.__name__ == n
        ][0]
    ):
    fc("function")(
        fc("code")(
            0,0,0,0,"KABOOM",(),(),(),"","",0,""
        ),{}
    )()
)()
""", "__import__('os').system('clear')",)

evaler = Evaler((sqrt, min, max, abs))


@pytest.mark.parametrize('expr', good_code)
def test_good(expr):
    evaler.eval(expr,
                {"x": 5,
                 "y": 6,
                 "a": 3}
                )


@pytest.mark.parametrize('expr', bad_code)
def test_bad(expr):
    with pytest.raises(NotSafeExpression):
        evaler.eval(expr,
                    {"x": 5,
                     "y": 6,
                     "a": 3}
                    )


@pytest.mark.parametrize('expr', very_bad_code)
def test_very_bad(expr):
    with pytest.raises(NotSafeExpression):
        evaler.eval(expr)
