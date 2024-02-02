from lia import parser, LiaInterpreter


if __name__ == '__main__':
    import argparse


    argparser = argparse.ArgumentParser(
        prog="liasis",
        description='sum the integers at the command line')
    argparser.add_argument(
        'input', type=argparse.FileType('r'),
        help='liasis source file')
    args = argparser.parse_args()

    tree = parser.parse(args.input.read())
    print("### AST ###")
    print(tree.pretty())
    
    print("### OUTPUT ###")
    interpreter = LiaInterpreter()
    interpreter.visit(tree)
