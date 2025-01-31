
#./quantifiers/__main__.py


from quantifiers.testers import *


def main(argv=None):
    """
    Creates and tests a Quantifier class against TestPairs.

    Usage:
        python -m quantifiers {Configs} {TestPairs}

    Configs:
        sep=SEP             Sets the Quantifier separator token [default: ","].
        encaps=PAIR         Adds an encapsulation a csv pair,
                            the first pair will be the default.

    TestPairs:
        ARGUMENT:EXPECT    The given constructor argument and expected
                           result pair.

    Note: It is advisable to use quotes around arguments
          to avoid shell expansion and unpredictable results.
    """
    if argv is None:
        from sys import argv
        if len(argv) <= 1 or any((a in ('-?', '-h', '--help', 'help')) for a
                                 in argv[1:]):
            print(main.__doc__.strip())
            exit(0)

    pairs, allow_encaps, encaps, sep = [], None, None, None
    for arg in argv[1:]:
        try:
            i = arg.index('=', 1)
        except:
            #print('pair', arg)
            try:
                left, right = csv_split(arg, ':')
            except:
                print(csv_split(arg, ':'))
            else:
                if right.endswith(('Error', 'Exception')):
                    try:
                        t = getattr(__builtins__, right)
                        assert (isinstance(t, type)
                                and issubclass(t, Exception))
                    except:
                        pass
                    else:
                        right = t
                pairs.append((left, right))
                continue

            print('Bad test pair {!r}'.format(arg), flush=True)
            exit(1)
        else:
            #print('keyword', arg)
            key, value = arg[:i].strip(), arg[i+1:].strip()
            if key == 'encaps':
                enc = csv_split(value, ',', 2)
                try:
                    left, right = enc
                except:
                    print('Bad Encaps: {!r}'.format(value))
                    exit(1)
                if encaps is None:
                    encaps = enc
                if allow_encaps is None:
                    allow_encaps = []
                if enc not in allow_encaps:
                    allow_encaps.append(enc)
            elif key == 'sep':
                if sep is not None:
                    print('multiple sep, previous {!r}, current {!r}'
                          .format(sep, value), flush=True)
                    exit(1)
                sep = value
            else:
                print('invalid keyword {!r} with value {!r}'
                      .format(key, value), flush=True)
                exit(1)

    #print('pairs', pairs)
    test_constructor(pairs, allow_encaps=allow_encaps,
                     encaps=encaps, sep=sep)


if __name__ == '__main__':
    main()
