from main import parser
import textwrap


def run_test_parser(source):
    return parser.parse(textwrap.dedent(source))


def test_if():
    source = """\
    if 1:
        1
    """
    output = run_test_parser(source)
    print(output.pretty())
