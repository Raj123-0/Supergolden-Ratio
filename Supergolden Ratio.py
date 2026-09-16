#!/usr/bin/env python3
'''
Supergolden Ratio Calculator (OEIS Edition)
Calculates Supergolden Ratio to exactly N digits using high-precision arithmetic.
'''

import sys
import time
import argparse
import os

os.environ['MPMATH_GMPY2'] = '1'
import gmpy2
import mpmath

sys.set_int_max_str_digits(0)

def save_oeis_files(constant_name: str, digits_str: str, target_digits: int) -> None:
    '''
    Save the digits to a raw file and an OEIS b-file.

    Args:
        constant_name: Name of the constant (used in filenames).
        digits_str: String of digits (without decimal point).
        target_digits: Number of digits to write.
    '''
    clean_digits = digits_str.replace(".", "")[:target_digits]

    raw_filename = f'{constant_name}_{target_digits}_digits.txt'
    with open(raw_filename, 'w', encoding='utf-8') as f:
        f.write(clean_digits)
    print(f'Saved raw digit output to {raw_filename}')

    b_filename = f'b_file_{constant_name}_{target_digits}.txt'
    with open(b_filename, 'w', encoding='utf-8') as f:
        for idx, digit in enumerate(clean_digits, start=1):
            f.write(f'{idx} {digit}\n')
    print(f'Saved OEIS b-file output to {b_filename}')

def compute_supergolden_ratio(target_digits: int) -> str:
    '''
    Compute the Supergolden Ratio to the specified number of digits.

    Args:
        target_digits: Number of digits to compute (including integer part).

    Returns:
        String of the first target_digits digits of the constant.
    '''
    dps_working = target_digits + 50
    mpmath.mp.dps = dps_working

    # Closed-form expression: root of x^3 = x + 1
    sqrt93 = mpmath.sqrt(93)
    term1 = (mpmath.mpf(29) - 3 * sqrt93) / 2
    term2 = (mpmath.mpf(29) + 3 * sqrt93) / 2
    val = (1 + term1 ** (mpmath.mpf(1) / 3) + term2 ** (mpmath.mpf(1) / 3)) / 3

    val_str = mpmath.nstr(val, dps_working)
    clean_digits = val_str.replace(".", "")[:target_digits]

    save_oeis_files('Supergolden_Ratio', clean_digits, target_digits)
    return clean_digits

def main() -> None:
    parser = argparse.ArgumentParser(description='Supergolden Ratio OEIS Calculator')
    parser.add_argument('-n', '--digits', type=int, default=1000, help='Target digits (default: 1000)')
    args = parser.parse_args()

    t0 = time.time()
    digits = compute_supergolden_ratio(args.digits)
    t1 = time.time()

    print(f'Execution finished in {t1 - t0:.4f} seconds.')

if __name__ == '__main__':
    main()