import argparse
from inspect import Parameter, signature


class Prog:
    def __init__(self, name: str, description: str):
        self._parser = argparse.ArgumentParser(prog=name, description=description)

        self._global_args = []
        self._subparsers = self._parser.add_subparsers()

    def main(self):
        args = self._parser.parse_args()

        if hasattr(args, "__func__"):
            self.ctx = self.__main__(
                **{
                    k: a
                    for k, a in vars(args).items()
                    if not k.startswith("__") and k in self._global_args
                }
            )
            args.__func__(
                **{
                    k: a
                    for k, a in vars(args).items()
                    if not k.startswith("__") and k not in self._global_args
                }
            )
        else:
            self._parser.print_usage()

    def _get_args(self, f: callable, info: dict):
        ret = {}
        for name, param in signature(f).parameters.items():
            k = {"default": param.default, "help": info.get(name, None)}

            k["action"] = "store"
            if param.annotation is bool:
                k["default"] = not k["default"]
                if param.default:
                    k["action"] = "store_true"
                else:
                    k["action"] = "store_false"
            else:
                k["type"] = param.annotation

            arg_name = name
            if param.default is not param.empty:
                if len(name) == 1:
                    arg_name = f"-{name}"
                else:
                    arg_name = f"--{name}"

            ret[name] = (arg_name, k)

        return ret

    def command(self, *args, **kwargs):
        def inner(f):
            parser = self._subparsers.add_parser(
                f.__name__, help=kwargs.get("help", None)
            )

            for _, (name, k) in self._get_args(f, kwargs).items():
                parser.add_argument(name, **k)

            parser.set_defaults(__func__=f)

            return f

        # If we only have one argument and it's a callable, we assume the
        # decorator is being used without arguments.
        if len(args) == 1 and callable(args[0]):
            return inner(args[0])

        return inner


def cli(name: str, description: str):
    prog = Prog(name, description)

    def inner(f):
        for key, (name, k) in prog._get_args(f, {}).items():
            prog._parser.add_argument(name, **k)
            prog._global_args.append(key)
            prog.__main__ = f

        return prog

    return inner
