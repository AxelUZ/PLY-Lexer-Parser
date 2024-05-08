import lexer

def test_lexer(input_string):
    lexer.lexer.input(input_string)
    print(f"Tokens for: '{input_string}'")
    for tok in lexer.lexer:
        print(f"{tok.type}({tok.value})", end=' ')
    print("\n")

def main():
    tests = [
        "var prueba1: int;",
        "while (x > 0) do { x = x - 1; }",
        "if (y == 10) { print(y); } else { y = 10; }",
        "var result: float = 3.14 * 2.0;",
        "var x, y, z: int; x = 100; y = x + 10; z = x * (y - 100);",
        "var distance: float = 0.0; distance = 3.14159 * 2.5;",
        "if (x > 100) { print(\"Condición cumplida\"); }",
        "while (x > 0) { x = x - 1; print(x); }",
        "void calculate(int a, float b) { var result: float; result = a * b + 10; print(result); } calculate(10, 3.14);",
    ]

    for test in tests:
        test_lexer(test)

if __name__ == "__main__":
    main()

