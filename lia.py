from lark import Lark
from interp import LiaInterpreter

with open("grammar.lark", "r", encoding="utf8") as grammar:
    parser = Lark(grammar, parser="earley", maybe_placeholders=True)
