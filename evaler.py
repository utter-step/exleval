import ast
import _ast


class NotSafeExpression(Exception):
    pass


class UnsafeNode(Exception):
    pass


class Evaler(object):
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
        # binary math
        _ast.LShift,
        _ast.RShift,
        _ast.BitAnd,
        _ast.BitOr,
        _ast.BitXor,
        _ast.Invert,
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

    def __init__(self, safe_funcs):
        # to preserve ordering. OrderedDict is overkill here, I think
        self.safe_func_names = [func.__name__ for func in safe_funcs]
        self.checker = Evaler.IsExprSafe(self.safe_func_names)

        self.safe_funcs = {func.__name__: func for func in safe_funcs}

    def eval(self, expr, variables=None):
        if variables is None:
            variables = {}
        ast_tree = ast.parse(expr)

        try:
            self.checker.visit(ast_tree)
            return eval(expr, {'__builtins__': self.safe_funcs}, variables)
        except UnsafeNode as e:
            raise NotSafeExpression(expr, e)

    def __str__(self):
        return "Evaler((%s))" % ", ".join(self.safe_func_names)

    @staticmethod
    def get_allowed_nodes():
        return Evaler.ALLOWED_NODES

    class IsExprSafe(ast.NodeVisitor):
        def __init__(self, safe_func_names):
            self.safe_func_names = safe_func_names

        def visit_Module(self, node):
            self.generic_visit(node)
            return True

        def visit_Call(self, node):
            func = node.func

            if "id" in func.__dict__:
                if func.id not in self.safe_func_names:
                    raise UnsafeNode(ast.dump(node))
            else:
                raise UnsafeNode(ast.dump(node))

            self.generic_visit(node)

        def visit_Compare(self, node):
            pass

        def visit_BoolOp(self, node):
            pass

        def generic_visit(self, node):
            if type(node) not in Evaler.get_allowed_nodes():
                raise UnsafeNode(ast.dump(node))
            ast.NodeVisitor.generic_visit(self, node)
