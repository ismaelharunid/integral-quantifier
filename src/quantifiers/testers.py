
#./quantifiers/testers.py



from .base_class import Quantifier


def test_constructor(pairs, *,
                allow_encaps=None, encaps=None, sep=None):
    attrs = {}
    if allow_encaps is not None:
        attrs['allow_encaps'] = allow_encaps
    if encaps is not None:
        attrs['encaps'] = encaps
    if sep is not None:
        attrs['sep'] = sep
    cls = (type('Quantifier', (Quantifier,), attrs)
           if attrs else
           Quantifier)
    if attrs:
        print('==== Quantifier class factory code ====')
        print('MyQuantifier = type("MyQuantifier",')
        print('                    (Quantifier,),')
        print('                    {!r})'.format(attrs))
    print('==== Using ====')
    print('cls.allow_encaps', cls.allow_encaps)
    print('cls.encaps', cls.encaps)
    print('cls.sep', cls.sep)

    total = errors = failure = 0
    print('==== Tests ====')
    for arg, expect in pairs:
        try:
            q = (cls.from_repr(arg) if isinstance(arg, str) else cls(arg))
        except Exception as err:
            if isinstance(expect, type) and issubclass(err, expect):
                print('[PASS] argument {!r}, expected error {!r}'
                      .format(arg, expect))
            else:
                print('[ERR ] argument {!r}, expected {!r}, actual error {!r}'
                      .format(arg, expect, str(err)))
                errors += 1
        else:
            if isinstance(expect, str):
                if str(q) == expect:
                    print('[PASS] argument {!r}, expected {}'
                          .format(arg, expect))
                else:
                    print('[FAIL] argument {!r}, expected {}, actual {!r}'
                          .format(arg, expect, q))
                    failure += 1
            else:
                if q == expect:
                    print('[PASS] argument {!r}, expected {!r}'
                          .format(arg, expect))
                else:
                    print('[FAIL] argument {!r}, expected {!r}, actual {1r}'
                          .format(arg, expect, q))
                    failure += 1
        total += 1
    
    passing = total - errors - failure
    success = passing * 100 / total
    print('==== Results ====')
    print('Passes {:10d}'.format(passing))
    print('Fails  {:10d}'.format(failure))
    print('Errors {:10d}'.format(errors))
    print('Total  {:10d}'.format(total))
    print('Success {:8.1f}%'.format(success))


def csv_split(source, sep=',', max=0):
    if sep in source:
        return tuple(i.strip() for i in source.split(sep, max-1))
    return (source.strip(),)


