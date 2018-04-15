from typing import Dict, Set, List
import abc
import syntax


class Statement:

    @abc.abstractmethod
    def get_variables(self) -> Set[str]:
        pass

    @abc.abstractmethod
    def evaluate(self, variables: Dict[str, bool]) -> bool:
        pass

    @abc.abstractmethod
    def __str__(self) -> str:
        pass


class MissingVariableException(Exception):

    def __init__(self, variable_name: str):
        self.variable_name = variable_name

    def __str__(self):
        return "Missing variable '" + self.variable_name + "'"


class TrueStatement(Statement):

    def get_variables(self) -> Set[str]:
        return set()

    def evaluate(self, variables: Dict[str, bool]) -> bool:
        return True

    def __str__(self) -> str:
        return syntax.TRUE_CONSTANT


class FalseStatement(Statement):

    def get_variables(self) -> Set[str]:
        return set()

    def evaluate(self, variables: Dict[str, bool]) -> bool:
        return False

    def __str__(self) -> str:
        return syntax.FALSE_CONSTANT


class VariableStatement(Statement):

    def __init__(self, variable_name: str):
        self.variable_name = variable_name

    def get_variables(self) -> Set[str]:
        return {self.variable_name}

    def evaluate(self, variables: Dict[str, bool]) -> bool:
        if self.variable_name not in variables:
            raise MissingVariableException(self.variable_name)
        return variables[self.variable_name]

    def __str__(self) -> str:
        return self.variable_name


class AndStatement(Statement):

    def __init__(self, statements: List[Statement]):
        self.statements = statements

    def get_variables(self) -> Set[str]:
        return set.union(*[sta.get_variables() for sta in self.statements])

    def evaluate(self, variables: Dict[str, bool]) -> bool:
        return all([sta.evaluate(variables) for sta in self.statements])

    def __str__(self) -> str:
        return syntax.OPENING_BRACKET + (' '+syntax.AND_OPERATOR+' ').join([sta.__str__() for sta in self.statements]) + syntax.CLOSING_BRACKET


class OrStatement(Statement):

    def __init__(self, statements: List[Statement]):
        self.statements = statements

    def get_variables(self) -> Set[str]:
        return set.union(*[sta.get_variables() for sta in self.statements])

    def evaluate(self, variables: Dict[str, bool]) -> bool:
        return any([sta.evaluate(variables) for sta in self.statements])

    def __str__(self) -> str:
        return syntax.OPENING_BRACKET + (' '+syntax.OR_OPERATOR+' ').join([sta.__str__() for sta in self.statements]) + syntax.CLOSING_BRACKET


class XorStatement(Statement):

    def __init__(self, statement1: Statement, statement2: Statement):
        self.statement1 = statement1
        self.statement2 = statement2

    def get_variables(self) -> Set[str]:
        return self.statement1.get_variables() | self.statement2.get_variables()

    def evaluate(self, variables: Dict[str, bool]) -> bool:
        return self.statement1.evaluate(variables) != self.statement2.evaluate(variables)

    def __str__(self) -> str:
        return "({} {} {})".format(self.statement1.__str__(), syntax.XOR_OPERATOR, self.statement2.__str__())


class NotStatement(Statement):

    def __init__(self, statement: Statement):
        self.statement = statement

    def get_variables(self) -> Set[str]:
        return self.statement.get_variables()

    def evaluate(self, variables: Dict[str, bool]) -> bool:
        return not self.statement.evaluate(variables)

    def __str__(self) -> str:
        return syntax.NOT_OPERATOR + self.statement.__str__()


class ImplStatement(Statement):

    def __init__(self, statement1: Statement, statement2: Statement):
        self.statement1 = statement1
        self.statement2 = statement2

    def get_variables(self) -> Set[str]:
        return self.statement1.get_variables() | self.statement2.get_variables()

    def evaluate(self, variables: Dict[str, bool]) -> bool:
        return (not self.statement1.evaluate(variables)) or self.statement2.evaluate(variables)

    def __str__(self) -> str:
        return "({} {} {})".format(self.statement1.__str__(), syntax.IMPL_OPERATOR, self.statement2.__str__())


class XnorStatement(Statement):

    def __init__(self, statement1: Statement, statement2: Statement):
        self.statement1 = statement1
        self.statement2 = statement2

    def get_variables(self) -> Set[str]:
        return self.statement1.get_variables() | self.statement2.get_variables()

    def evaluate(self, variables: Dict[str, bool]) -> bool:
        return self.statement1.evaluate(variables) == self.statement2.evaluate(variables)

    def __str__(self) -> str:
        return "({} {} {})".format(self.statement1.__str__(), syntax.XNOR_OPERATOR, self.statement2.__str__())
