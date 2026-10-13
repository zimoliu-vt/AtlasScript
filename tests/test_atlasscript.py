
import io
import unittest
from contextlib import redirect_stdout

from atlasscript.parser import parse
from atlasscript.interpreter import Interpreter


def run_atlas(source):
    output = io.StringIO()
    interpreter = Interpreter()

    with redirect_stdout(output):
        interpreter.run(parse(source))

    return output.getvalue().strip()


class TestAtlasScript(unittest.TestCase):

    def test_arithmetic(self):
        result = run_atlas("print(10 + 5 * 2);")
        self.assertEqual(result, "20")

    def test_variables(self):
        result = run_atlas("""
            let x = 10;
            let y = x + 5;
            print(y);
        """)
        self.assertEqual(result, "15")

    def test_comparisons(self):
        result = run_atlas("""
            print(5 > 3);
            print(5 == 5);
            print(2 >= 10);
        """)
        self.assertEqual(
            result, "True\nTrue\nFalse"
        )

    def test_if_else(self):
        result = run_atlas("""
            let x = 10;
            if (x > 5) {
                print("Greater");
            } else {
                print("Smaller");
            }
        """)
        self.assertEqual(result, "Greater")

    def test_while_loop(self):
        result = run_atlas("""
            let x = 0;
            while (x < 3) {
                print(x);
                x = x + 1;
            }
        """)
        self.assertEqual(result, "0\n1\n2")

    def test_undefined_variable(self):
        with self.assertRaises(NameError):
            run_atlas("print(unknown);")

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            run_atlas("print(10 / 0);")


    def test_functions(self):
        result = run_atlas("""
            fn add(a, b) {
                return a + b;
            }
            print(add(10, 20));
        """)
        self.assertEqual(result, "30")

    def test_recursion(self):
        result = run_atlas("""
            fn factorial(n) {
                if (n <= 1) {
                    return 1;
                }
                return n * factorial(n - 1);
            }
            print(factorial(5));
        """)
        self.assertEqual(result, "120")


if __name__ == "__main__":
    unittest.main()
