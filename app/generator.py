from pathlib import Path

def generate_sample_test(a: int, b: int):
    """Write a parametrised pytest file that checks a+b and a-b."""
    test_code = f'''\
def test_addition():
    assert {a} + {b} == {a + b}

def test_subtraction():
    assert {a} - {b} == {a - b}
'''
    gen_path = Path(__file__).resolve().parents[1] / "generated" / "auto_test.py"
    gen_path.parent.mkdir(parents=True, exist_ok=True)
    gen_path.write_text(test_code)
    print(f"[generator] Wrote {gen_path}")
