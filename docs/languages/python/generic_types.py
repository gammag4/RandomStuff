from dataclasses import dataclass
from typing import Generic, TypeVar

# Define class C
class C:
    def c_method(self) -> str:
        return "method in C"

# Define class C2
class C2:
    def c2_method(self) -> str:
        return "method in C2"

# Define a TypeVar T bound to C: T must be subclass of C
T = TypeVar('T', bound=C)
U = TypeVar('U', bound=C2)

@dataclass
class A(ABC, Generic[T, U]):
    a: T
    b: u

    def call_c(self) -> str:
        # Since T is bound to C, we know `.c_method()` is available
        return self.a.c_method() + self.b.c2_method()

# Example subclass
class SubC(C):
    def c_method(self) -> str:
        return "overridden in SubC"

# Example subclass
class SubC2(C2):
    def c2_method(self) -> str:
        return "overridden in SubC2"

# Instantiate A with an instance of a subclass of C
x = A[SubC, SubC2](a=SubC(), b=SubC2())
print(x.call_c())  # prints “overridden in SubC”
