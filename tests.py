from unittest import TestCase

from statement import TrueStatement, FalseStatement, VariableStatement, MissingVariableException, AndStatement, \
    OrStatement, XorStatement, ImplStatement, XnorStatement, NotStatement


class TestTrueStatement(TestCase):
    def test_get_variables(self):
        self.assertSetEqual(TrueStatement().get_variables(), set())

    def test_evaluate(self):
        self.assertTrue(TrueStatement().evaluate({'a': True, 'b': False}))

    def test_str(self):
        self.assertEqual(TrueStatement().__str__(), '1')


class TestFalseStatement(TestCase):
    def test_get_variables(self):
        self.assertSetEqual(FalseStatement().get_variables(), set())

    def test_evaluate(self):
        self.assertFalse(FalseStatement().evaluate({'a': True, 'b': False}))

    def test_str(self):
        self.assertEqual(FalseStatement().__str__(), '0')


class TestVariableStatement(TestCase):
    def test_get_variables(self):
        self.assertSetEqual(VariableStatement('foo').get_variables(), {'foo'})

    def test_evaluate(self):
        self.assertTrue(VariableStatement('foo').evaluate({'foo': True}))
        self.assertFalse(VariableStatement('bar').evaluate({'bar': False}))
        self.assertRaises(MissingVariableException, lambda: VariableStatement('foo').evaluate({'bar': False}))

    def test_str(self):
        self.assertEqual(VariableStatement('foo').__str__(), 'foo')


class TestAndStatement(TestCase):
    def test_get_variables(self):
        self.assertSetEqual(AndStatement([VariableStatement('foo'), VariableStatement('foo'), VariableStatement('bar'),
                                          TrueStatement()]).get_variables(), {'foo', 'bar'})

    def test_evaluate(self):
        self.assertTrue(AndStatement([TrueStatement()]).evaluate({}))
        self.assertFalse(AndStatement([FalseStatement()]).evaluate({}))
        self.assertTrue(AndStatement([TrueStatement(), TrueStatement(), TrueStatement()]).evaluate({}))
        self.assertFalse(AndStatement([TrueStatement(), FalseStatement(), TrueStatement()]).evaluate({}))

    def test_str(self):
        self.assertEqual(AndStatement(
            [VariableStatement('foo'), VariableStatement('foo'), VariableStatement('bar'), TrueStatement()]).__str__(),
                         "(foo & foo & bar & 1)")


class TestOrStatement(TestCase):
    def test_get_variables(self):
        self.assertSetEqual(OrStatement([VariableStatement('foo'), VariableStatement('foo'), VariableStatement('bar'),
                                         TrueStatement()]).get_variables(), {'foo', 'bar'})

    def test_evaluate(self):
        self.assertTrue(OrStatement([TrueStatement()]).evaluate({}))
        self.assertFalse(OrStatement([FalseStatement()]).evaluate({}))
        self.assertTrue(OrStatement([TrueStatement(), TrueStatement(), TrueStatement()]).evaluate({}))
        self.assertTrue(OrStatement([TrueStatement(), FalseStatement(), TrueStatement()]).evaluate({}))

    def test_str(self):
        self.assertEqual(OrStatement(
            [VariableStatement('foo'), VariableStatement('foo'), VariableStatement('bar'), TrueStatement()]).__str__(),
                         "(foo | foo | bar | 1)")


class TestXorStatement(TestCase):
    def test_get_variables(self):
        self.assertSetEqual(XorStatement(VariableStatement('foo'), VariableStatement('bar')).get_variables(), {'foo', 'bar'})
        self.assertSetEqual(XorStatement(VariableStatement('foo'), VariableStatement('foo')).get_variables(), {'foo'})

    def test_evaluate(self):
        self.assertFalse(XorStatement(FalseStatement(), FalseStatement()).evaluate({}))
        self.assertTrue(XorStatement(FalseStatement(), TrueStatement()).evaluate({}))
        self.assertTrue(XorStatement(TrueStatement(), FalseStatement()).evaluate({}))
        self.assertFalse(XorStatement(TrueStatement(), TrueStatement()).evaluate({}))

    def test_str(self):
        self.assertEqual(XorStatement(VariableStatement('foo'), FalseStatement()).__str__(), "(foo ^ 0)")


class TestImplStatement(TestCase):
    def test_get_variables(self):
        self.assertSetEqual(ImplStatement(VariableStatement('foo'), VariableStatement('bar')).get_variables(), {'foo', 'bar'})
        self.assertSetEqual(ImplStatement(VariableStatement('foo'), VariableStatement('foo')).get_variables(), {'foo'})

    def test_evaluate(self):
        self.assertTrue(ImplStatement(FalseStatement(), FalseStatement()).evaluate({}))
        self.assertTrue(ImplStatement(FalseStatement(), TrueStatement()).evaluate({}))
        self.assertFalse(ImplStatement(TrueStatement(), FalseStatement()).evaluate({}))
        self.assertTrue(ImplStatement(TrueStatement(), TrueStatement()).evaluate({}))

    def test_str(self):
        self.assertEqual(ImplStatement(VariableStatement('foo'), FalseStatement()).__str__(), "(foo > 0)")


class TestXnorStatement(TestCase):
    def test_get_variables(self):
        self.assertSetEqual(XnorStatement(VariableStatement('foo'), VariableStatement('bar')).get_variables(), {'foo', 'bar'})
        self.assertSetEqual(XnorStatement(VariableStatement('foo'), VariableStatement('foo')).get_variables(), {'foo'})

    def test_evaluate(self):
        self.assertTrue(XnorStatement(FalseStatement(), FalseStatement()).evaluate({}))
        self.assertFalse(XnorStatement(FalseStatement(), TrueStatement()).evaluate({}))
        self.assertFalse(XnorStatement(TrueStatement(), FalseStatement()).evaluate({}))
        self.assertTrue(XnorStatement(TrueStatement(), TrueStatement()).evaluate({}))

    def test_str(self):
        self.assertEqual(XnorStatement(VariableStatement('foo'), FalseStatement()).__str__(), "(foo = 0)")


class TestNotStatement(TestCase):
    def test_get_variables(self):
        self.assertSetEqual(NotStatement(TrueStatement()).get_variables(), set())

    def test_evaluate(self):
        self.assertFalse(NotStatement(TrueStatement()).evaluate({}))
        self.assertTrue(NotStatement(FalseStatement()).evaluate({}))

    def test_str(self):
        self.assertEqual(NotStatement(VariableStatement('foo')).__str__(), "~foo")