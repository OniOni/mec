from subparser import Prog


prog = Prog(
    name='example',
    description='An example command.'
)


@prog.command(help="Command help.", param="Param help.", flag="Activate flag.")
def test(param: str = None, flag: bool = True):
    print("Invoked command test")

    if param:
        print(f"with param: {param}")
    if flag:
        print("Flag activated.")


@prog.command
def test2():
    print("Invoked command test2.")


@prog.command(
    help="Add both args.",
    a="First number to add", b="Second number to add"
)
def add(a: int, b: int):
    print(a + b)

if __name__ == "__main__":
    prog.main()
