
#./quantifiers/base_class.py


from collections.abc import Sequence
from numbers import Integral, Number


class Quantifier:
    "A simple Quantifier class."

    allow_encaps = (('(', ')'), ('{', '}'), ('[', ']'), ('<', '>'))
    "Pairs of acceptable encaps to try."

    encaps = None
    "The default encaps pair."

    sep = ','
    "The min and max value separator."

    @classmethod
    def from_repr(cls, token, start=0, stop=None, *, partial=False):
        "Parse token and return as a Quantifier"
        allow_encaps, encaps, sep = cls.allow_encaps, cls.encaps, cls.sep
        i0, i1, _ = slice(start, stop, 1).indices(len(token))
        while i0 < i1 and token[i0].isspace():
            i0 += 1
        while i0 < i1-1 and token[i1-1].isspace():
            i1 -= 1
        if encaps is None:
            for (l, r) in allow_encaps:
                if token.startswith(l, i0, i1):
                    encaps = (l, r)
                    break
        left, right = (('', '') if not encaps else encaps)
        #print('using encaps', (left, right))
        def skip_digits(i, stop):
            while i < stop and token[i] in '0123456789':
                i += 1
            return i

        def skip_space(i, stop):
            while i < stop and token[i].isspace():
                i += 1
            return i

        try:
            assert token.startswith(left, i0, i1)
            i = i0 + len(left)
            j = skip_space(skip_digits(i, i1), i1)
            k = (skip_space(j + len(sep), i1)
                 if token.startswith(sep, j, i1) else
                 j)
            l = token.index(right, skip_space(skip_digits(k, i1), i1), i1)
            if j == l:
                m = n = token[i:l].strip()
            else:
                m, n = token[i:j].strip(), token[k:l].strip()
            m, n = int(m or 0), (int(n) if n else None)
            if not partial:
                assert l + len(right) == i1
        except Exception as err:
            #raise
            pass
        else:
            return cls((m, n))

        raise ValueError('expected a Quantifier representation, not {!r}'
                         .format(token))

    _minvalue = None
    @property
    def minvalue(self):
        "The minimum value of the quantifier range."
        return self._minvalue

    _maxvalue = None
    @property
    def maxvalue(self):
        "The maximum value (inclusive) of the quantifier range."
        return self._maxvalue

    def __new__(cls, quantifier, none_value=None):
        """
        A simple Quantifier class.
        
        Arguments:
            quantifier  :[Quantifier|Integral|tuple[Integral|None]|None]
                The quantifier range value(s) (inclusive)
            none_value  :Any
                The substitute value if `quantifier` is None,
                otherwise None becomes (0, None)
        """
        if isinstance(quantifier, Quantifier):
            return quantifier
        q = (none_value if quantifier is None else quantifier)
        if q is None or (isinstance(q, Integral) and q >= 0):
            q = (q, q)
        else:
            q = tuple(q)
        if len(q) == 1:
            q += (None,)
        m, n = q
        m = (0 if m is None else int(m))
        n = (None if n is None else int(n))
        if 0 <= m and (n is None or m <= n):
            self = super().__new__(cls)
            self._minvalue = m
            self._maxvalue = n
            return self

        raise ValueError('Quantifier expects None, Integral or pair of same,'
                         ' not {!r}'.format(quantifier))

    def __iter__(self):
        "Returns an iterator that yields all values within the quantifier."
        return self.iterate()

    def __repr__(self):
        "Return a code representation token."
        return ('{}(({}, {!r}))'
                .format(type(self).__name__, self._minvalue, self._maxvalue))

    def __reversed__(self):
        "Returns a reverse iterator that yields values within the quantifier."
        return self.iterate(reverse=True)

    def get_maxvalue(self, none_value=None):
        if self._maxvalue is None:
            return none_value
        return self._maxvalue

    def iterate(self, end=None, *, reverse=False, allow_infinite=False):
        """
        Returns an iterator that yields values within the quantifier.
        
        Arguments:
            end  :PositiveIntegral
                The end value to use if max_value is None
            reverse  :bool
                If True return a reverse Iterator, else a regular one.
            allow_infinite  :bool
                Live dangerously by allowing an infinite Iterator.
        Returns:
            :Iterator
        """
        i = self._minvalue
        n = (end
             if self._maxvalue is None else
             self._maxvalue
             if end is None else
             min(end, self._maxvalue))
        if n is None:
            if reverse:
                raise ValueError('Attempt iterate FROM infinity,')
            if allow_infinite:
                while True:
                    yield i
                    i += 1
            raise ValueError('Attempt to iterate infinity,'
                             ' if you really meant to do this use'
                             ' "self.iterate(allow_infinite=True)"'
                             ' instead')
        if reverse:
            m = self._minvalue
            while m <= n:
                yield n
                n -= 1
        else:
            while i <= n:
                yield i
                i += 1

    def quantify(self, value):
        "Returns the value if it qualifies, otherwise raise ValueError"
        if isinstance(value, Number):
            if not (self._minvalue > value
                    or (self._maxvalue is not None
                         and value > self._maxvalue)):
                return value
        elif isinstance(value, Sequence):
            _ = all(self.quantify(i) for i in value)
            return value

        raise ValueError('{} <= {!r} <= {!r} does NOT quantify'
                         .format(self._minvalue, value, self._maxvalue))

    def to_range(self, end=None):
        "Returns a range instance that includes all values in quantifier."
        if end is None:
            stop = (None if self._maxvalue is None else self._maxvalue + 1)
            return range(self._minvalue, stop, 1)
        return range(*self.to_slice().indices(end))

    def to_repr(self):
        "Return a quantifier representation token."
        allow_encaps, encaps, sep = self.allow_encaps, self.encaps, self.sep
        if encaps is None and self.allow_encaps:
             encaps = self.allow_encaps[0]
        left, right = (('', '') if not encaps else encaps)
        if self._maxvalue is None:
            return left + str(self._minvalue) + sep + right
        if self._minvalue == self._maxvalue:
            return left + str(self._minvalue) + right
        return ('{}{}{}{}{}'
                .format(left, self._minvalue, sep, self._minvalue, right))

    def to_slice(self):
        "Returns quantifier as am exclusive slice."
        return slice(self._minvalue,
                     (None if self._maxvalue is None else self._maxvalue + 1),
                     1)

    def to_tuple(self):
        "Returns the min and max values as a 2-tuple."
        return tuple(self._minvalue, self._maxvalue)


