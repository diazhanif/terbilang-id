import subprocess
import sys
import unittest

from terbilang_id import MAX_NUMBER, parse_integer, terbilang, terbilang_rupiah


class TerbilangTests(unittest.TestCase):
    def test_basic_numbers_and_indonesian_special_forms(self):
        cases = {
            0: "nol",
            1: "satu",
            10: "sepuluh",
            11: "sebelas",
            12: "dua belas",
            19: "sembilan belas",
            20: "dua puluh",
            21: "dua puluh satu",
            100: "seratus",
            101: "seratus satu",
            111: "seratus sebelas",
            200: "dua ratus",
            999: "sembilan ratus sembilan puluh sembilan",
        }
        for number, expected in cases.items():
            with self.subTest(number=number):
                self.assertEqual(terbilang(number), expected)

    def test_thousand_and_large_scales(self):
        cases = {
            1_000: "seribu",
            1_001: "seribu satu",
            11_000: "sebelas ribu",
            1_000_000: "satu juta",
            1_001_001: "satu juta seribu satu",
            1_000_000_000: "satu miliar",
            1_000_000_000_000: "satu triliun",
            1_000_000_000_000_000: "satu kuadriliun",
        }
        for number, expected in cases.items():
            with self.subTest(number=number):
                self.assertEqual(terbilang(number), expected)

    def test_negative_currency_and_maximum(self):
        self.assertEqual(terbilang(-42), "minus empat puluh dua")
        self.assertEqual(terbilang_rupiah(125_000), "seratus dua puluh lima ribu rupiah")
        self.assertTrue(terbilang(MAX_NUMBER).startswith("sembilan ratus sembilan puluh sembilan kuadriliun"))

    def test_rejects_invalid_types_and_out_of_range_values(self):
        for value in (True, 1.5, "12"):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    terbilang(value)
        for value in (MAX_NUMBER + 1, -(MAX_NUMBER + 1)):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    terbilang(value)

    def test_parses_plain_and_indonesian_grouped_integers(self):
        self.assertEqual(parse_integer("1250000"), 1_250_000)
        self.assertEqual(parse_integer("1.250.000"), 1_250_000)
        self.assertEqual(parse_integer("1 250 000"), 1_250_000)
        self.assertEqual(parse_integer("-1.250.000"), -1_250_000)
        for value in ("1,250,000", "12.00", "1.250 000", "1,5", ""):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    parse_integer(value)

    def test_cli_rupiah_and_invalid_input(self):
        process = subprocess.run(
            [sys.executable, "-m", "terbilang_id", "1.250.000", "--rupiah"],
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual(process.stdout, "satu juta dua ratus lima puluh ribu rupiah\n")
        invalid = subprocess.run(
            [sys.executable, "-m", "terbilang_id", "12,50"],
            text=True,
            capture_output=True,
        )
        self.assertEqual(invalid.returncode, 2)
        self.assertEqual(invalid.stdout, "")


if __name__ == "__main__":
    unittest.main()
