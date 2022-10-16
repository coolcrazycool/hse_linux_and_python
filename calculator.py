from argparse import ArgumentParser


class Calculator:
    def __init__(self, definition: str):
        self.symbols = ["(", ")", "+", "-", "/", "*"]
        self.priority_dict = {
            "(": 0,
            "+": 1,
            "-": 1,
            "/": 2,
            "*": 2
        }
        self.definition = self.renotation(self.precompile_definition(definition))

    def renotation(self, definition: list):
        end_notation = []
        stack = []
        for i in definition:
            if i == "(":
                stack.append(i)
            elif i in self.priority_dict.keys():
                while len(stack) > 0 and self.priority_dict[stack[-1]] >= self.priority_dict[i]:
                    end_notation.append(stack.pop())
                stack.append(i)
            elif i == ")":
                try:
                    while stack[-1] != "(":
                        end_notation.append(stack.pop())
                except IndexError as e:
                    raise IndexError("Открывающая скобка не найдена")
                stack.pop()
            elif i not in self.priority_dict.keys():
                end_notation.append(i)
        while len(stack) != 0:
            end_notation.append(stack.pop())
        return end_notation

    def precompile_definition(self, definition: str):
        tokens = []
        last_token = ""
        for i in definition.strip():
            if i == " ":
                pass
            elif i in self.symbols:
                if i == "-" and (len(tokens) == 0 or last_token == "("):
                    tokens.append("0")
                if last_token != "":
                    tokens.append(last_token)
                last_token = i
            elif last_token in self.symbols:
                tokens.append(last_token)
                last_token = i
            else:
                last_token += i
        tokens.append(last_token)
        return tokens

    def calculate(self):
        stack = []
        for i in self.definition:
            if i not in self.symbols:
                stack.append(i)
            else:
                if i == "+":
                    right = stack.pop()
                    left = stack.pop()
                    stack.append(float(left) + float(right))
                elif i == "-":
                    right = stack.pop()
                    left = stack.pop()
                    stack.append(float(left) - float(right))
                elif i == "*":
                    right = stack.pop()
                    left = stack.pop()
                    stack.append(float(left) * float(right))
                elif i == "/":
                    right = stack.pop()
                    left = stack.pop()
                    try:
                        stack.append(float(left) / float(right))
                    except ZeroDivisionError as e:
                        raise ZeroDivisionError(f"Деление на 0 в выражении между числами {left} и {right}")
        return stack[0]


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-df", "--definition", dest="definition", type=str)

    args = parser.parse_args()
    calc = Calculator(args.definition)
    print("Calculate result:", calc.calculate())
    print("Absolute result:", eval(args.definition))
    assert eval(args.definition) == calc.calculate()
    # for value in [
    #     "-2+(-10+5)-5+15.14*(10.5-5)-5",
    #     "( ( 9 - ( 5 + 2 ) ) * 3 ) * ( 1 + 7 )",
    #     "15/(7-(1+1))*3-(2+(1+1))+15/(7-(1+1))*3-(2+(1+1))"
    # ]:
    #     calc = Calculator(value)
    #     print(calc.calculate())
    #     assert eval(value) == calc.calculate()
    #
    # try:
    #     calc = Calculator("-2+(-10+5)-5+15.14*(10.5-5)-5/0")
    #     calc.calculate()
    # except ZeroDivisionError as e:
    #     print(e)
    #
    # try:
    #     calc = Calculator("-2+(-10+5)-5+15.14*10.5-5)-5/0")
    #     calc.calculate()
    # except IndexError as e:
    #     print(e)
