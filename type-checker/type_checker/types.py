# -*- coding: utf-8 -*-

class JavaConstructor(object):
    def __init__(self, argument_types=[]):
        self.argument_types = argument_types

class JavaType(object):

    def __init__(self, name, direct_supertypes = []):
        self.name = name
        self.direct_supertypes = direct_supertypes

    def is_subtype_of(self, other):
        """ True if this type is a direct _or_ indirect subtype of the given other type. """
        return(
            other == self
            or any(t.is_subtype_of(other) for t in self.direct_supertypes))

    def is_supertype_of(self, other):
        """ Convenience counterpart to is_subtype_of. """
        return other.is_subtype_of(self)

class JavaClassOrInterface(JavaType):

    def __init__(self, name, direct_supertypes = [], constructor = JavaConstructor([]), methods = []):
        super().__init__(name, direct_supertypes)
        self.name = name
        self.constructor = constructor
        self.methods = { method.name: method for method in methods }

    def method_named(self, name):
        """ Returns the JavaMethod with the given name, which may come from a supertype. """
        try:
            return self.methods[name]
        except KeyError:
            for type in self.direct_supertypes:
                try:
                    return type.method_named(name)
                except NoSuchMethod:
                    pass
            raise NoSuchMethod("{0} has no method named {1}".format(self.name, name))

class NoSuchMethod(Exception):
    pass

class JavaMethod(object):
    def __init__(self, name, argument_types=[], return_type=None):
        self.name = name
        self.argument_types = argument_types
        self.return_type = return_type
