import argparse
from inspect import signature


class Prog:

    def __init__(self, name: str, description: str):
        self._parser = argparse.ArgumentParser(
            prog=name,
            description=description
        )

        self._subparsers = self._parser.add_subparsers()

    def main(self):
        args = self._parser.parse_args()

        if hasattr(args, 'func'):
            a = vars(args).copy()
            del(a['func'])
            args.func(**a)
        else:
            self._parser.print_usage()

    def command(self, *args, **kwargs):
        def inner(f):
            parser = self._subparsers.add_parser(f.__name__, help=kwargs.get('help', None))

            for name, param in signature(f).parameters.items():
                # import ipdb; ipdb.set_trace()

                k = {
                    "default": param.default,
                    "help": kwargs.get(name, None)
                }

                k["action"] = "store"
                if param.annotation is bool:
                    k["default"] = not k["default"]
                    if param.default:
                        k["action"] = "store_true"
                    else:
                        k["action"] = "store_false"
                else:
                    k["type"] = param.annotation

                parser.add_argument(
                    f"--{name}"
                    if param.default is not param.empty
                    else name,
                    **k,
                )

            parser.set_defaults(func=f)

            return f

        if len(args) == 1 and callable(args[0]):
            return inner(args[0])

        return inner
