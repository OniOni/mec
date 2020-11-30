from typing import List

from subparser import cli


@cli(name="example", description="An example command.")
def example(v: bool = True):
    return {"verbose": v}


@example.command(help="Command help.", param="Param help.", flag="Activate flag.")
def test(param: str = None, flag: bool = True):
    print("Invoked command test")

    if param:
        print(f"with param: {param}")
    if flag:
        print("Flag activated.")
    if example.ctx["verbose"]:
        print("Verbose")


@example.command
def test2():
    print("Invoked command test2.")


@example.command(
    help="Add both args.", a="First number to add", b="Second number to add"
)
def add(a: int, b: int):
    print(a + b)


@example.command
def nargs(a: List[str]):
    print(f"Got {len(a)} args: {a}")


if __name__ == "__main__":
    example.main()
