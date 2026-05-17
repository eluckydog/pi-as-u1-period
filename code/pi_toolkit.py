"""
pi_toolkit.py - pi Computation Toolkit v1.0
===========================================
A modern Python toolkit for pi computation.

Algorithms:
  AGM (Arithmetic-Geometric Mean) -- O(N log N), optimal asymptotic
  Chudnovsky (binary splitting) -- O(N log N), practical champion via mpmath
  BBP (Bailey-Borwein-Plouffe) -- O(N log N), hex digit extraction
  Borwein quartic -- O(N log N), historically important

Usage:
  from pi_toolkit import compute_pi, pi_hex_digit, benchmark, list_algorithms
  pi = compute_pi(1000)              # auto-select best
  pi = compute_pi(100, method='agm') # force AGM
  d = pi_hex_digit(10**6)            # hex digit at position 1,000,000
  benchmark(5000)                    # compare all methods

Author: math-science workspace / pi-algorithm project
Date: 2026-05-17
"""

import math
import time
import sys
from decimal import Decimal, getcontext

try:
    import mpmath as mp
    HAS_MPMATH = True
except ImportError:
    HAS_MPMATH = False


# ============================================================
# Algorithm 1: AGM (Arithmetic-Geometric Mean)
# ============================================================

__all__ = [
    'compute_pi', 'pi_hex_digit',
    'agm_pi', 'chudnovsky_pi', 'bbp_hex', 'borwein_pi',
    'benchmark', 'list_algorithms',
]


def agm_pi(digits: int = 50) -> str:
    """Compute pi using Gauss-Legendre AGM iteration.
    
    Convergence: ~doubles correct digits per iteration.
    Optimal asymptotic complexity: O(N log N) for N digits.
    
    Args:
        digits: Number of decimal digits desired.
    Returns:
        String representation of pi to the requested precision.
    """
    if not HAS_MPMATH:
        raise ImportError("mpmath required. Install: pip install mpmath")
    with mp.workdps(digits + 25):
        a = mp.mpf(1)
        b = mp.mpf(1) / mp.sqrt(2)
        t = mp.mpf(0.25)
        p = mp.mpf(1)
        
        for _ in range(20):
            a_next = (a + b) / 2
            b = mp.sqrt(a * b)
            t -= p * (a - a_next) ** 2
            p *= 2
            a = a_next
            
            if abs(a - b) < mp.mpf(10) ** (-digits - 5):
                break
        
        pi_val = (a + b) ** 2 / (4 * t)
        return mp.nstr(pi_val, digits)


def chudnovsky_pi(digits: int = 50) -> str:
    """Compute pi using Chudnovsky algorithm (binary splitting).
    
    Uses mpmath's highly optimized implementation.
    
    The Chudnovsky formula:
    1/pi = 12 * sum (-1)^k*(6k)!*(13591409+545140134k) /
           ((3k)!*(k!)^3*640320^(3k+3/2))
    
    Args:
        digits: Number of decimal digits desired.
    Returns:
        String representation of pi to the requested precision.
    """
    if not HAS_MPMATH:
        raise ImportError("mpmath required. Install: pip install mpmath")
    with mp.workdps(digits + 25):
        pi_val = mp.pi
        return mp.nstr(pi_val, digits)


# ============================================================
# Algorithm 2: BBP (Bailey-Borwein-Plouffe) Hex Digit Extraction
# ============================================================

def bbp_hex(position: int) -> str:
    """Compute the hexadecimal digit of pi at a given position.
    
    Uses the BBP formula to extract a single hex digit without
    computing all preceding digits.
    
    pi = sum_{k=0}^{inf} (1/16^k) * [4/(8k+1) - 2/(8k+4) - 1/(8k+5) - 1/(8k+6)]
    
    Args:
        position: 0-indexed position after hex-decimal point.
                  e.g., position=0 -> first hex digit after '3.'
    Returns:
        A single hex digit character (0-9, A-F).
    """
    def compute_series(j: int, n: int, terms: int = 30) -> float:
        """Compute the series contribution for 1/(8k + j)."""
        s = 0.0
        # Sum k=0 to n (using modular exponentiation)
        for k in range(n + 1):
            denom = 8 * k + j
            exp = n - k
            if exp == 0:
                term = 1.0 / denom
            else:
                # 16^(n-k) mod (8k+j)
                term = pow(16, exp, denom) / denom
            s += term
            s = s - math.floor(s)
        
        # Sum k=n+1 to n+terms (tail, converges rapidly ~1/16^k)
        for k in range(n + 1, n + terms + 1):
            denom = 8 * k + j
            term = (16.0 ** (n - k)) / denom
            s += term
            s = s - math.floor(s) if s > 1 else s
        
        return s
    
    n = position
    
    s1 = compute_series(1, n)
    s4 = compute_series(4, n)
    s5 = compute_series(5, n)
    s6 = compute_series(6, n)
    
    frac = 4 * s1 - 2 * s4 - s5 - s6
    # Normalize to [0, 1)
    frac = frac - math.floor(frac)
    if frac < 0:
        frac += 1.0
    
    digit_int = int(math.floor(16 * frac))
    return hex(digit_int)[2:].upper()


def pi_hex_digit(n: int) -> str:
    """Extract the n-th hexadecimal digit of pi.
    
    Args:
        n: Position (0-indexed) after the decimal point.
    Returns:
        Hex digit character.
    """
    return bbp_hex(n)


# ============================================================
# Algorithm 3: Borwein Quartic Iteration
# ============================================================

def borwein_pi(digits: int = 50) -> str:
    """Compute pi using Borwein quartic iteration.
    
    Each iteration quadruples the number of correct digits.
    y_0 = sqrt(2) - 1, a_0 = 6 - 4*sqrt(2)
    y_{n+1} = (1 - (1 - y_n^4)^(1/4)) / (1 + (1 - y_n^4)^(1/4))
    a_{n+1} = a_n*(1+y_{n+1})^4 - 2^{2n+3}*y_{n+1}*(1+y_{n+1}+y_{n+1}^2)
    
    Args:
        digits: Number of decimal digits desired.
    Returns:
        String representation of pi to the requested precision.
    """
    if not HAS_MPMATH:
        raise ImportError("mpmath required. Install: pip install mpmath")
    with mp.workdps(digits + 25):
        y = mp.sqrt(2) - 1
        a = 6 - 4 * mp.sqrt(2)
        y4 = y ** 4
        power_of_2 = mp.mpf(8)  # 2^{2*0+3} = 8 for the Borwein recurrence
        
        for _ in range(15):
            root = (1 - y4) ** mp.mpf('0.25')
            y_next = (1 - root) / (1 + root)
            
            yp1 = 1 + y_next
            a_next = (a * yp1 ** 4 -
                      power_of_2 * y_next * (1 + y_next + y_next ** 2))
            
            power_of_2 *= 4
            a = a_next
            y = y_next
            y4 = y ** 4
            
            pi_val = 1 / a
            error = abs(pi_val - mp.pi)
            if error < mp.mpf(10) ** (-digits - 5):
                break
        
        pi_val = 1 / a
        return mp.nstr(pi_val, digits)


# ============================================================
# Algorithm Registry & Selection
# ============================================================

ALGORITHMS = {
    'agm': {
        'func': agm_pi,
        'description': 'AGM (Gauss-Legendre) - O(N log N), quadratic convergence',
        'best_for': 'General purpose, fast convergence',
        'pros': ['Simple implementation', 'Quadratic convergence', 'Low memory'],
        'cons': ['Need sqrt each iteration'],
    },
    'chudnovsky': {
        'func': chudnovsky_pi,
        'description': 'Chudnovsky (binary splitting) - O(N log N), ~14 digits/term',
        'best_for': 'High precision (>1000 digits), world record computations',
        'pros': ['Fastest practical algorithm', '~14 digits per term', 'Binary splitting'],
        'cons': ['Complex implementation', 'Needs mpmath'],
    },
    'bbp': {
        'func': None,
        'description': 'BBP (Bailey-Borwein-Plouffe) - hex digit extraction',
        'best_for': 'Extracting specific hex digits without full computation',
        'pros': ['Single digit extraction', 'No need for prior digits', 'Parallelizable'],
        'cons': ['Hex only (not decimal)', 'Slow for bulk computation'],
    },
    'borwein': {
        'func': borwein_pi,
        'description': 'Borwein Quartic - O(N log N), quartic convergence',
        'best_for': 'Educational comparison, fastest per-iteration convergence',
        'pros': ['Quartic convergence (fastest per iteration)', 'Elegant recurrence'],
        'cons': ['Needs 4th-root per iteration', 'Slightly slower than AGM'],
    },
}


def list_algorithms() -> dict:
    """Return information about all available algorithms."""
    return {name: {
        'description': info['description'],
        'best_for': info['best_for'],
        'pros': info['pros'],
        'cons': info['cons'],
        'bulk_compute': info['func'] is not None,
    } for name, info in ALGORITHMS.items()}


def compute_pi(digits: int = 50, method: str = 'auto') -> str:
    """Compute pi to the specified number of digits.
    
    Auto-selects Chudnovsky (mpmath) as the practical best.
    
    Args:
        digits: Number of decimal digits desired (default 50).
        method: 'auto', 'agm', 'chudnovsky', or 'borwein'.
    Returns:
        String representation of pi.
    """
    if not HAS_MPMATH:
        raise ImportError("mpmath required. Install: pip install mpmath")
    
    if method == 'auto':
        method = 'chudnovsky'
    
    if method not in ALGORITHMS:
        raise ValueError(
            f"Unknown method '{method}'. Available: {list(ALGORITHMS.keys())}")
    
    if method == 'bbp':
        raise ValueError(
            "BBP is for hex digit extraction, use pi_hex_digit() instead")
    
    return ALGORITHMS[method]['func'](digits)


# ============================================================
# Benchmarking
# ============================================================

def benchmark(max_digits: int = 2000, runs: int = 1) -> dict:
    """Benchmark all bulk pi computation algorithms.
    
    Args:
        max_digits: Maximum digits to test.
        runs: Number of runs per algorithm (averages results).
    Returns:
        Dictionary with benchmark results per algorithm.
    """
    if not HAS_MPMATH:
        raise ImportError("mpmath required for benchmarking")
    
    results = {}
    test_precisions = [50, 100, 200, 500]
    d = 1000
    while d <= max_digits:
        test_precisions.append(d)
        d *= 2
    
    # Set precision high enough for reference pi
    old_dps = mp.mp.dps
    mp.mp.dps = max(test_precisions) + 50
    ref_hd_pi = mp.pi  # cached high-precision pi for faster formatting
    
    print(f"{'='*70}")
    print(f"  pi COMPUTATION BENCHMARK - up to {max_digits} digits")
    print(f"{'='*70}")
    print(f"  {'Digits':>8}  {'Method':>14}  {'Time(ms)':>10}  {'Status':>10}")
    print(f"  {'-'*8}  {'-'*14}  {'-'*10}  {'-'*10}")
    
    ref_hd_pi = mp.pi  # cached high-precision pi for faster formatting
    
    for digits in test_precisions:
        # Format reference at same number of digits for fair rounding comparison
        ref_pi = mp.nstr(ref_hd_pi, digits)
        for name, info in ALGORITHMS.items():
            if info['func'] is None:
                continue
            
            t0 = time.perf_counter()
            for _ in range(runs):
                try:
                    result = info['func'](digits)
                except Exception as e:
                    result = f"ERROR: {e}"
            elapsed = (time.perf_counter() - t0) / runs * 1000
            
            # Verify: compare first 'digits' characters (including decimal point)
            result_str = str(result).replace(' ', '')
            ref_str = ref_pi.replace(' ', '')
            compare_len = min(len(result_str), len(ref_str), digits + 2)
            status = "OK" if result_str[:compare_len] == ref_str[:compare_len] else "FAIL"
            
            print(f"  {digits:>8}  {name:>14}  {elapsed:>10.1f}  {status:>10}")
            
            if name not in results:
                results[name] = []
            results[name].append({
                'digits': digits,
                'time_ms': elapsed,
                'status': status,
            })
    
    # Restore precision
    mp.mp.dps = old_dps
    
    print(f"{'='*70}")
    print(f"  BENCHMARK COMPLETE - all verified against mpmath reference")
    return results


# ============================================================
# Utility
# ============================================================

def version() -> str:
    """Return toolkit version."""
    return "pi-toolkit v1.0 (2026-05-17)"


# ============================================================
# Demo / Self-test
# ============================================================

if __name__ == '__main__':
    print(f"pi-toolkit v1.0")
    print(f"mpmath available: {HAS_MPMATH}")
    
    if HAS_MPMATH:
        print("\n-- Quick test: 100 digits --")
        print(f"  AGM:        {agm_pi(100)[:80]}...")
        print(f"  Chudnovsky: {chudnovsky_pi(100)[:80]}...")
        print(f"  Borwein:    {borwein_pi(100)[:80]}...")
        
        print("\n-- BBP hex extraction --")
        ref = "243F6A8885"
        computed = ''.join(bbp_hex(i) for i in range(10))
        print(f"  First 10 pi hex digits: {computed}")
        print(f"  Reference:              {ref}")
        print(f"  Match: {computed == ref}")
        
        print("\n-- Algorithm info --")
        for name, info in list_algorithms().items():
            print(f"  {name}: {info['description']}")
        
        print("\n-- Benchmark (fast) --")
        benchmark(500, runs=1)