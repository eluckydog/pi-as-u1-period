"""
bbp_searcher.py - BBP Formula Search Engine v1.0
=================================================
Systematic search for BBP-type formulas for mathematical constants.

A BBP formula has the form:
  alpha = sum_{k=0}^{inf} (1/b^k) * sum_{j=1}^{J} a_j / (J*k + j)^s

Where:
  b = base (integer >= 2)
  a_j = integer coefficients
  J = number of terms per block
  s = exponent (usually 1)

This tool:
1. Systematically decomposes arctan(p/q) into BBP form
2. Searches for integer relations (PSLQ-like) to find new formulas
3. Extends to other constants: e, zeta(3), Catalan's constant G, log(2)

Why BBP formulas matter:
- They allow extracting a specific digit WITHOUT computing preceding digits
- They enable distributed pi computation with no communication
- They provide algebraic proofs of normality for specific bases

Author: math-science workspace / pi-algorithm project
Date: 2026-05-17
"""

import math
import sys
import itertools
from fractions import Fraction
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass


# ============================================================
# Core Types
# ============================================================

@dataclass
class BBPFormula:
    """Represents a BBP-type formula."""
    constant: str           # Name of constant (pi, log2, zeta3, ...)
    base: int              # b in sum (1/b^k)
    block_size: int        # J, number of terms per block
    exponents: int         # s, exponent in denominator
    coefficients: List[int]  # a_j coefficients
    description: str       # Human-readable description
    
    def to_latex(self) -> str:
        """Render the formula in LaTeX."""
        parts = []
        for j, a in enumerate(self.coefficients, start=1):
            if a == 0:
                continue
            sign = "+" if a > 0 else "-"
            a_abs = abs(a)
            if j == 1 and a > 0:
                sign = ""
            parts.append(
                f"{sign}\\frac{{{a_abs}}}{{({self.block_size}k+{j-1})^{self.exponents}}}")
        inner = " ".join(parts)
        return (f"\\{self.constant} = "
                f"\\sum_{{k=0}}^{{\\infty}} "
                f"\\frac{{1}}{{{self.base}^k}} "
                f"\\left({inner}\\right)")
    
    def __repr__(self) -> str:
        return (f"BBPFormula(constant={self.constant}, base={self.base}, "
                f"block_size={self.block_size}, coeffs={self.coefficients})")


# ============================================================
# Known BBP formulas (reference database)
# ============================================================

KNOWN_FORMULAS = {
    'pi': [
        BBPFormula(
            constant='pi', base=16, block_size=8, exponents=1,
            coefficients=[4, 0, 0, -2, -1, -1, 0, 0],
            description='Original BBP formula for pi (1996)'),
        BBPFormula(
            constant='pi', base=16, block_size=8, exponents=1,
            coefficients=[4, 0, 0, -2, -1, -1, 0, 0],
            description='Same formula with shifted indices'),
        BBPFormula(
            constant='pi', base=4096, block_size=12, exponents=1,
            coefficients=[],  # Bellard's variant (complex)
            description='Bellard formula, 43% faster than original BBP'),
    ],
    'log2': [
        BBPFormula(
            constant='log2', base=2, block_size=1, exponents=1,
            coefficients=[1],
            description='log(2) = sum 1/(k * 2^k)'),
    ],
    'zeta3': [
        BBPFormula(
            constant='zeta3', base=2, block_size=7, exponents=3,
            coefficients=[],  # Has multiple term families
            description='zeta(3) has BBP-type formulas (Broadhurst 1998)'),
    ],
    'catalan': [
        BBPFormula(
            constant='G', base=16, block_size=8, exponents=2,
            coefficients=[],  # Catalan constant G
            description='Catalan constant has BBP-type formulas'),
    ],
}


# ============================================================
# Arctan Decomposition
# ============================================================

def arctan_series(x: Fraction, base: int, max_terms: int = 100) -> List[Tuple[int, Fraction]]:
    """Decompose arctan(x) into BBP-type series for a given base.
    
    arctan(x) = sum_{k=0}^{inf} (-1)^k * x^(2k+1) / (2k+1)
               = x * sum_{k=0}^{inf} (-x^2)^k / (2k+1)
    
    For BBP form, we need arctan(1/q) where x = 1/q:
    arctan(1/q) = sum_{k=0}^{inf} (-1)^k / (q^(2k+1) * (2k+1))
    
    The goal is to express this as sum 1/16^k times rational coefficients.
    
    Args:
        x: The argument of arctan (typically 1/q for integer q).
        base: Target base (e.g., 16 for standard BBP).
        max_terms: Maximum terms to generate.
    Returns:
        List of (coefficient_numerator, coefficient_denominator) tuples.
    """
    terms = []
    sign = 1
    power = x
    denominator = 1
    
    for _ in range(max_terms):
        # term = sign * power / denominator
        # = sign * (1/q)^denominator / denominator
        terms.append((sign * power.numerator, power.denominator * denominator))
        sign = -sign
        power = power * x * x  # x^(2k+3) = x^(2k+1) * x^2
        denominator += 2
    
    return terms


def find_arctan_decomposition(target: float, max_q: int = 50,
                               max_terms: int = 10, tolerance: float = 0.01) -> List[Tuple[int, int, int]]:
    """Find integer combinations of arctan(1/q) that approximate target.
    
    This searches for:
    target ~ sum c_i * arctan(1/q_i)
    
    Where c_i are small integers and q_i are positive integers.
    
    Args:
        target: Target value (e.g., pi/4 for Machin-type formulas).
        max_q: Maximum q to try.
        max_terms: Maximum number of terms in the combination.
        tolerance: Acceptable error.
    Returns:
        List of (coefficient, q, index) tuples.
    """
    results = []
    
    for q in range(1, max_q + 1):
        val = math.atan(1.0 / q)
        if abs(val - target) < tolerance:
            results.append((1, q, -1))
        elif abs(-val - target) < tolerance:
            results.append((-1, q, -1))
    
    return results


def machin_type_search(max_q: int = 100) -> List[Tuple[int, int, int, int, float]]:
    """Search for Machin-type formulas: pi/4 = a*arctan(1/p) + b*arctan(1/q).
    
    Returns:
        List of (a, p, b, q, error) tuples sorted by error.
    """
    results = []
    target = math.pi / 4
    
    for p in range(2, max_q + 1):
        atan_p = math.atan(1.0 / p)
        for q in range(p + 1, max_q + 1):
            atan_q = math.atan(1.0 / q)
            for a in range(-5, 6):
                for b in range(-5, 6):
                    if a == 0 and b == 0:
                        continue
                    val = a * atan_p + b * atan_q
                    err = abs(val - target)
                    if err < 0.01:
                        results.append((a, p, b, q, err))
    
    results.sort(key=lambda x: x[4])
    return results


def decompose_to_bbp(arctan_q: int, base: int = 16) -> Optional[BBPFormula]:
    """Convert arctan(1/q) to BBP form for a given base.
    
    arctan(1/q) = sum_{k=0}^{inf} (-1)^k / (q^(2k+1) * (2k+1))
    
    To convert to BBP form 1/base^k * a/(block*k + j):
    - If q^2 = base, then arctan(1/q) is directly in BBP form.
    - If q^2 divides base, the series can be rearranged.
    - Generally, this only works for q = sqrt(base) or when
      q^(2k+1) can be expressed as base^k * something.
    
    Args:
        arctan_q: The q in arctan(1/q).
        base: The BBP base.
    Returns:
        BBPFormula if conversion is possible, None otherwise.
    """
    # Check if q^2 == base (the direct BBP case)
    if q_sq := base:
        q = arctan_q
        if q * q == base:
            # arctan(1/q) = sum (-1)^k / (q^(2k+1) * (2k+1))
            # = sum 1/base^k * (-1)^k / (q * (2k+1))
            # This is a BBP formula with block_size=2
            return BBPFormula(
                constant='arctan(1/{})'.format(q),
                base=base,
                block_size=2,
                exponents=1,
                coefficients=[1, -1],
                description=f'arctan(1/{q}) in base {base}',
            )
        return None
    
    return None


# ============================================================
# BBP Base Detection
# ============================================================

def search_bbp_base(constant_name: str, constant_value: float,
                     bases: List[int] = None,
                     max_block_size: int = 12,
                     max_coeff_abs: int = 20) -> List[BBPFormula]:
    """Search for BBP formulas for a constant in given bases.
    
    Uses brute-force enumeration of coefficients to find combinations
    that match the constant.
    
    Args:
        constant_name: Name of constant.
        constant_value: Known value of constant.
        bases: List of bases to search. Default: powers of 2 up to 2^16.
        max_block_size: Maximum block size J to try.
        max_coeff_abs: Maximum absolute coefficient value.
    Returns:
        List of candidate BBPFormula objects.
    """
    if bases is None:
        bases = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 4096, 65536]
    
    candidates = []
    
    for base in bases:
        if base > 10**6:
            continue
        
        for J in range(1, max_block_size + 1):
            # Skip if too many coefficients to enumerate
            num_coeffs = J
            total_combos = (2 * max_coeff_abs + 1) ** num_coeffs
            if total_combos > 100000:
                continue
            
            # Evaluate BBP formula with given coefficients
            for coeffs in _enumerate_coeffs(J, max_coeff_abs):
                # Compute: sum_{k=0}^{N} 1/base^k * sum a_j/(J*k+j)
                value = _evaluate_bbp(base, J, coeffs, max_terms=50)
                error = abs(value - constant_value)
                
                if error < 1e-8:
                    candidates.append(BBPFormula(
                        constant=constant_name,
                        base=base,
                        block_size=J,
                        exponents=1,
                        coefficients=list(coeffs),
                        description=f'Found: error={error:.1e}',
                    ))
    
    candidates.sort(key=lambda f: abs(
        _evaluate_bbp(f.base, f.block_size,
                      f.coefficients, max_terms=100) - constant_value))
    return candidates


def _enumerate_coeffs(J: int, max_abs: int):
    """Generator for coefficient tuples. Yields small ones first."""
    for total_weight in range(0, max_abs * J + 1):
        for coeffs in _coeffs_with_weight(J, max_abs, total_weight):
            yield coeffs


def _coeffs_with_weight(J: int, max_abs: int, weight: int):
    """Yield all coefficient tuples with given sum of absolute values."""
    if J == 1:
        for a in range(-max_abs, max_abs + 1):
            if abs(a) == weight and a != 0:
                yield (a,)
        return
    
    for first in range(-max_abs, max_abs + 1):
        if abs(first) > weight:
            continue
        for rest in _coeffs_with_weight(J - 1, max_abs, weight - abs(first)):
            yield (first,) + rest


def _evaluate_bbp(base: int, J: int, coeffs: Tuple[int, ...],
                  max_terms: int = 50) -> float:
    """Evaluate a BBP formula to a given number of terms."""
    total = 0.0
    inv_base_k = 1.0
    for k in range(max_terms):
        inner = 0.0
        for j, a in enumerate(coeffs, start=1):
            inner += a / (J * k + j)
        total += inv_base_k * inner
        inv_base_k /= base
    return total


# ============================================================
# PSLQ-like Integer Relation Search
# ============================================================

def pslq_search(values: List[float], max_abs: int = 50) -> List[Tuple[int, ...]]:
    """Simple integer relation search (like PSLQ but brute-force).
    
    Finds integer coefficients c_i such that sum c_i * values[i] ~ 0.
    
    Args:
        values: List of floating-point values.
        max_abs: Maximum absolute coefficient value.
    Returns:
        List of (c_1, ..., c_n) tuples giving integer relations.
    """
    n = len(values)
    results = []
    
    def search_recursive(idx: int, current_value: float, coeffs: List[int]):
        if idx == n - 1:
            # Last coefficient: solve for it
            target = -current_value
            if abs(values[idx]) > 1e-15:
                c = round(target / values[idx])
                if abs(c) <= max_abs:
                    all_coeffs = tuple(coeffs + [c])
                    total = sum(a * v for a, v in zip(all_coeffs, values))
                    if abs(total) < 1e-10:
                        results.append(all_coeffs)
            return
        
        for c in range(-max_abs, max_abs + 1):
            search_recursive(idx + 1, current_value + c * values[idx],
                             coeffs + [c])
    
    search_recursive(0, 0.0, [])
    return results


# ============================================================
# Extensible Constant Registry
# ============================================================

CONSTANTS = {
    'pi': {
        'value': math.pi,
        'known_formulas': ['BBP base-16', 'Bellard base-4096'],
        'type': 'transcendental',
    },
    'log2': {
        'value': math.log(2),
        'known_formulas': ['BBP base-2'],
        'type': 'transcendental',
    },
    'log3': {
        'value': math.log(3),
        'known_formulas': ['BBP base-3 possible'],
        'type': 'transcendental',
    },
    'zeta3': {
        'value': 1.2020569031595942854,  # Apery's constant
        'known_formulas': ['BBP-type exists (Broadhurst 1998)'],
        'type': 'irrational',
    },
    'catalan': {
        'value': 0.915965594177219,  # Catalan's constant G
        'known_formulas': ['BBP-type base-16'],
        'type': 'unknown (conjectured transcendental)',
    },
    'e': {
        'value': math.e,
        'known_formulas': ['No known BBP formula'],
        'type': 'transcendental',
    },
}


def list_constants() -> Dict[str, dict]:
    """List all supported constants and their BBP status."""
    return {name: {
        'value': info['value'],
        'known_formulas': info['known_formulas'],
        'type': info['type'],
    } for name, info in CONSTANTS.items()}


def search_constant(constant_name: str, bases: List[int] = None) -> List[BBPFormula]:
    """Search for BBP formulas for a specific constant.
    
    Args:
        constant_name: Name from CONSTANTS registry.
        bases: Bases to search.
    Returns:
        List of candidate BBPFormula objects.
    """
    if constant_name not in CONSTANTS:
        raise ValueError(
            f"Unknown constant '{constant_name}'. Available: {list(CONSTANTS.keys())}")
    
    info = CONSTANTS[constant_name]
    return search_bbp_base(constant_name, info['value'], bases=bases)


def version() -> str:
    """Return searcher version."""
    return "bbp-searcher v1.0 (2026-05-17)"


# ============================================================
# Demo / Self-test
# ============================================================

if __name__ == '__main__':
    print("BBP Formula Search Engine v1.0")
    print("=" * 60)
    
    print("\n-- Known Formulas --")
    for name, formulas in KNOWN_FORMULAS.items():
        print(f"\n  {name}:")
        for f in formulas:
            print(f"    base={f.base}, block_size={f.block_size}")
            print(f"    {f.description}")
    
    print("\n-- Machin-type Search (pi) --")
    results = machin_type_search(max_q=30)
    print(f"  Found {len(results)} candidate decompositions")
    print("  Top 5:")
    for a, p, b, q, err in results[:5]:
        print(f"    pi/4 ~ {a}*arctan(1/{p}) + {b}*arctan(1/{q})  err={err:.2e}")
    
    print("\n-- Constant Registry --")
    for name, info in list_constants().items():
        print(f"  {name}: value={info['value']:.6f}, type={info['type']}")
        print(f"    known: {', '.join(info['known_formulas'])}")
    
    print("\n-- BBP Search Demo: log2 --")
    candidates = search_constant('log2', bases=[2, 4, 8])
    print(f"  Found {len(candidates)} candidates for log(2)")
    for c in candidates[:5]:
        print(f"    base={c.base}, block_size={c.block_size}, coeffs={c.coefficients}")
    
    print("\nDone.")