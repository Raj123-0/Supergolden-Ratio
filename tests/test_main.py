import importlib.util
import tempfile
import os
import mpmath

spec = importlib.util.spec_from_file_location('MODULE_FILENAME', 'MODULE_FILENAME')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_compute_supergolden_ratio():
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            for digits in [10, 20, 50]:
                result = module.compute_supergolden_ratio(digits)
                assert len(result) == digits
                # Verify against high-precision reference
                mpmath.mp.dps = digits + 100
                sqrt93 = mpmath.sqrt(93)
                term1 = (mpmath.mpf(29) - 3 * sqrt93) / 2
                term2 = (mpmath.mpf(29) + 3 * sqrt93) / 2
                val = (1 + term1 ** (mpmath.mpf(1) / 3) + term2 ** (mpmath.mpf(1) / 3)) / 3
                val_str = mpmath.nstr(val, digits + 100)
                expected = val_str.replace('.', '')[:digits]
                assert result == expected
                # Check raw file
                raw_file = f'Supergolden_Ratio_{digits}_digits.txt'
                assert os.path.exists(raw_file)
                with open(raw_file, 'r') as f:
                    raw_content = f.read().strip()
                assert raw_content == result
                # Check b-file
                b_file = f'b_file_Supergolden_Ratio_{digits}.txt'
                assert os.path.exists(b_file)
                with open(b_file, 'r') as f:
                    lines = f.readlines()
                assert len(lines) == digits
                for i, line in enumerate(lines, start=1):
                    parts = line.strip().split()
                    assert len(parts) == 2
                    assert parts[0] == str(i)
                    assert parts[1] == result[i-1]
        finally:
            os.chdir(original_cwd)