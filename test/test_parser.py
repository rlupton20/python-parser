import python_parser.python_parser as lib


# Test basic tag matching
def test_match_tag():
    p = lib.tag("foo")
    assert(p("foo") == "foo")


def test_match_tag_fail():
    p = lib.tag("foo")
    assert(p("flo") == None)


def test_match_init():
    p = lib.tag("foo")
    assert(p.run_parser("foot") == ("foo", "t"))


def test_match_init():
    p = lib.tag("foo")
    assert(p.run_parser("foot") == ("foo", "t"))


def test_match_init_complete():
    p = lib.tag("foo")
    assert(p("foot") == None)


# Now test parser base class
def test_derived_partial():
    p = lib.tag("foo").partial()
    assert(p("foot") == "foo")


def test_map():
    p = lib.tag("foo").map(len)
    assert(p("foo") == 3)


# Test sequencing combinator
def test_sequence():
    p = lib.sequence(lib.tag("foo"), lib.tag("bar"))
    assert(p("foobar") == ("foo", "bar"))


def test_sequence_fail():
    p = lib.sequence(lib.tag("foo"), lib.tag("baz"))
    assert(p("foobar") == None)


def test_args_via_sequence():
    class Dummy(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y

    p = lib.sequence(lib.tag("foo"), lib.tag("bar")).map(lambda args: Dummy(*args))
    r = p("foobar")
    assert(r != None)
    assert(r.x == "foo")
    assert(r.y == "bar")


# Test decorator combinators
def test_function_decorator():

    @lib.parser(lib.tag("foo"))
    def plen(s):
        return len(s)

    assert(plen("foo") == 3)
    assert(plen("boo") == None)

    

def test_class_decorator():

    @lib.DeriveParser(lib.tag("foo"), lib.tag("bar"))
    class Dummy(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y

    p = Dummy.parser()
    r = p("foobar")

    # Successful cases
    assert(r != None)
    assert(r.x == "foo")
    assert(r.y == "bar")
    # Failure case
    assert(p("foobaz") == None)
    assert(p("foobarr") == None)