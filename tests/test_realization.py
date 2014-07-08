from .. import Evaler


def test_preserving_variables_clean():
    evaler = Evaler()

    variables = {"x": 3, "y": 4}

    evaler.eval("2 + x", variables)
    assert "True" not in variables


def test_preserving_builtins_clean():
    evaler = Evaler()

    variables = {"x": 3, "y": 4}
    old_boolean = evaler.boolean_builtins

    evaler.eval("2 + x", variables)
    assert old_boolean == evaler.boolean_builtins
