# integral-quantifier
A simple Quantifier class useful for inclusive ranges and qualifying integral values and sets.

## Installation

python -m pip install integral-quantifier

or

pip install integral-quantifier

or

python -m pip install https://github.com/ismaelharunid/integral-quantifier.git

or

pip install https://github.com/ismaelharunid/integral-quantifier.git


## Simple Code Usage

    >>> from quantifiers import Quantifier
    >>> q = Quantifier((1,4))  # will quantify a value to 1 to 4 (inclusive)
    >>> q
    Quantifier((1, 4))
    >>> tuple(i in q for i in range(6))
    (False, True, True, True, True, False)
    >>> q.quantify(4)
    4
    >>> q.quantify(5)
    ValueError: 1 <= 5 <= 4 does NOT quantify;
    >>> q.quantify(range(1, 4))
    range(1,4)
    >>> q.quantify(range(4))
    ValueError: 1 <= 0 <= 4 does NOT quantify
    >>> q.to_range()
    range(1, 5)
    >>> q.to_repr()
    '(1,1)'
    >>> q.to_slice()
    slice(1, 5, 1)
    >>> q.to_tuple()
    (1, 4)
    >>> tuple(q)
    (1, 2, 3, 4)
    >>> Quantifier.from_repr('(1,)')
    Quantifier((1, None))
    >>> Quantifier.from_repr('1,')
    Quantifier((1, None))
    >>> Quantifier.from_repr('(1,)')
    Quantifier((1, None))
    >>> Quantifier.from_repr('{1,}')
    Quantifier((1, None))
    >>> Quantifier.from_repr('[1,]')
    Quantifier((1, None))
    >>> Quantifier.from_repr('<1,>')
    Quantifier((1, None))

## Customized Quantifier Code Usage

    >>> from quantifiers import Quantifier
    >>> REQuantifier = type('REQuantifier',
                            (Quantifier,),
                            dict(allow_encaps=None, # only default encaps
                                 encaps='{}',       # default emcaps
                                 sep=','))          # min and max separator
    >>> q = REQuantifier.from_repr('{1,}')
    >>> q
    REQuantifier((1, None))
    >>> q.to_repr()
    '{1,}'
    >>> REQuantifier.from_repr('1,')
    ValueError: expected a Quantifier representation, not '1,'
