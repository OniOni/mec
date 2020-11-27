# mec
Mat's Easy CLI

### Example
```python
from subparser import cli

@cli(
    name='example',
    description='An example command.'
)
def example(v: bool = True):
    return {'verbose': v}

@example.command(help="Command help.", param="Param help.", flag="Activate flag.")
def test(param: str = None, flag: bool = True):
    print("Invoked command test")

    if param:
        print(f"with param: {param}")
    if flag:
        print("Flag activated.")
    if example.ctx['verbose']:
        print("Verbose")


@example.command
def test2():
    print("Invoked command test2.")


@example.command(
    help="Add both args.",
    a="First number to add", b="Second number to add"
)
def add(a: int, b: int):
    print(a + b)

if __name__ == "__main__":
    example.main()
```
- Top level help:
```
$ ./venv/bin/python src/subparser/example.py -h
usage: example [-h] [-v] {test,test2,add} ...

An example command.

positional arguments:
  {test,test2,add}
    test            Command help.
    test2
    add             Add both args.

optional arguments:
  -h, --help        show this help message and exit
  -v
```

- Invoking command with args:
```
$ ./venv/bin/python src/subparser/example.py test
Invoked command test
$ ./venv/bin/python src/subparser/example.py test --flag
Invoked command test
Flag activated.
$ ./venv/bin/python src/subparser/example.py test --flag --param one
Invoked command test
with param: one
Flag activated.
$ ./venv/bin/python src/subparser/example.py -v test --flag --param one
Invoked command test
with param: one
Flag activated.
Verbose
```

- Invoking command with positionnal args:
```
$ ./venv/bin/python src/subparser/example.py add 31 11
42
$ ./venv/bin/python src/subparser/example.py add a b
usage: example add [-h] a b
example add: error: argument a: invalid int value: 'a'
```

- Subcommand help:
```
$ ./venv/bin/python src/subparser/example.py add -h
usage: example add [-h] a b

positional arguments:
  a           First number to add
  b           Second number to add

optional arguments:
  -h, --help  show this help message and exit
```