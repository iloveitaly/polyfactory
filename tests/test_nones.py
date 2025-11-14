from typing import Optional

from pydantic import BaseModel

from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.fields import AlwaysNone, NeverNone


def test_never_none() -> None:
    class MyModel(BaseModel):
        name: Optional[str]

    class MyFactory(ModelFactory[MyModel]):
        name = NeverNone()

    assert MyFactory.build().name is not None


def test_always_none() -> None:
    class MyModel(BaseModel):
        name: Optional[str]

    class MyFactory(ModelFactory[MyModel]):
        name = AlwaysNone()

    # AlwaysNone ensures the field is always set to None
    assert MyFactory.build().name is None


def test_always_none_vs_plain_none() -> None:
    """Test that AlwaysNone provides more explicit intent than plain None assignment.

    Note: While `name = None` works similarly to `name = AlwaysNone()` in terms of
    the final result, AlwaysNone makes the intent more explicit and is processed
    differently internally (goes through should_set_none_value rather than
    being treated as a static field value).
    """

    class MyModel(BaseModel):
        always_none_field: Optional[str]
        plain_none_field: Optional[str]

    class MyFactory(ModelFactory[MyModel]):
        always_none_field = AlwaysNone()
        plain_none_field = None

    instance = MyFactory.build()
    assert instance.always_none_field is None
    assert instance.plain_none_field is None


def test_never_none_with_allow_none_optionals() -> None:
    """Test that NeverNone prevents None even when __allow_none_optionals__ is True."""

    class MyModel(BaseModel):
        always_generated: Optional[str]
        sometimes_none: Optional[str]

    class MyFactory(ModelFactory[MyModel]):
        __allow_none_optionals__ = True
        always_generated = NeverNone()

    # Build multiple times to verify NeverNone consistency
    for _ in range(10):
        instance = MyFactory.build()
        # always_generated should never be None due to NeverNone
        assert instance.always_generated is not None
        # sometimes_none can be None or a value (random with __allow_none_optionals__)
        assert instance.sometimes_none is None or isinstance(instance.sometimes_none, str)
