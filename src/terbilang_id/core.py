"""Terbilang bilangan bulat berbahasa Indonesia."""

from __future__ import annotations

import argparse
import re
import sys
from typing import Iterable


MAX_NUMBER = 999_999_999_999_999_999
_UNITS = ("", "satu", "dua", "tiga", "empat", "lima", "enam", "tujuh", "delapan", "sembilan")
_SCALES = ("", "ribu", "juta", "miliar", "triliun", "kuadriliun")
_PLAIN_INTEGER = re.compile(r"[+-]?[0-9]+\Z")
_GROUPED_INTEGER = re.compile(r"[+-]?(?:[0-9]{1,3}(?:\.[0-9]{3})+|[0-9]{1,3}(?: [0-9]{3})+)\Z")


def _under_hundred(number: int) -> str:
    if number < 10:
        return _UNITS[number]
    if number == 10:
        return "sepuluh"
    if number == 11:
        return "sebelas"
    if number < 20:
        return f"{_UNITS[number - 10]} belas"
    tens, remainder = divmod(number, 10)
    words = f"{_UNITS[tens]} puluh"
    if remainder:
        words += f" {_UNITS[remainder]}"
    return words


def _under_thousand(number: int) -> str:
    if number < 100:
        return _under_hundred(number)
    hundreds, remainder = divmod(number, 100)
    if hundreds == 1:
        words = "seratus"
    else:
        words = f"{_UNITS[hundreds]} ratus"
    if remainder:
        words += f" {_under_hundred(remainder)}"
    return words


def terbilang(number: int) -> str:
    """Ubah integer menjadi kata Bahasa Indonesia.

    Menerima rentang -999.999.999.999.999.999 sampai +999.999.999.999.999.999.
    """
    if isinstance(number, bool) or not isinstance(number, int):
        raise TypeError("number harus berupa integer")
    if abs(number) > MAX_NUMBER:
        raise ValueError(f"angka di luar rentang ±{MAX_NUMBER}")
    if number == 0:
        return "nol"

    negative = number < 0
    remaining = abs(number)
    parts: list[str] = []
    scale_index = 0

    while remaining:
        group = remaining % 1000
        if group:
            if scale_index == 1 and group == 1:
                part = "seribu"
            else:
                part = _under_thousand(group)
                if scale_index:
                    part += f" {_SCALES[scale_index]}"
            parts.append(part)
        remaining //= 1000
        scale_index += 1

    result = " ".join(reversed(parts))
    return f"minus {result}" if negative else result


def terbilang_rupiah(number: int) -> str:
    """Ubah integer menjadi nominal rupiah dalam kata."""
    return f"{terbilang(number)} rupiah"


def parse_integer(text: str) -> int:
    """Baca bilangan bulat polos, atau format ribuan Indonesia bertitik/berspasi."""
    value = text.strip()
    if _PLAIN_INTEGER.fullmatch(value):
        number = int(value)
    elif _GROUPED_INTEGER.fullmatch(value):
        number = int(value.replace(".", "").replace(" ", ""))
    else:
        raise ValueError("format angka tidak valid")
    if abs(number) > MAX_NUMBER:
        raise ValueError("angka di luar rentang")
    return number


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="terbilang-id",
        description="Ubah angka bulat menjadi kata Bahasa Indonesia.",
    )
    parser.add_argument("angka", help="angka bulat; contoh: 1250000 atau 1.250.000")
    parser.add_argument("--rupiah", action="store_true", help="tambahkan kata 'rupiah'")
    args = parser.parse_args(argv)

    try:
        number = parse_integer(args.angka)
        result = terbilang_rupiah(number) if args.rupiah else terbilang(number)
    except (TypeError, ValueError):
        print(
            f"terbilang-id: gunakan angka bulat dalam rentang ±{MAX_NUMBER}; "
            "pemisah ribuan boleh berupa titik atau spasi.",
            file=sys.stderr,
        )
        return 2

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
