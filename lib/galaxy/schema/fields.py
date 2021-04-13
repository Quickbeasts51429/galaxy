import re
from typing import (
    Optional,
)

from pydantic import (
    Field,
)
from pydantic.networks import AnyUrl

ENCODED_DATABASE_ID_PATTERN = re.compile('f?[0-9a-f]+')
ENCODED_ID_LENGTH_MULTIPLE = 16


class EncodedDatabaseIdField(str):
    """
    Encoded Database ID validation.
    """

    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(
            min_length=16,
            pattern='[0-9a-fA-F]+',
            examples=['0123456789ABCDEF'],
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('String required')
        if v.startswith("F"):
            # Library Folder ids start with an additional "F"
            len_v = len(v) - 1
        else:
            len_v = len(v)
        if len_v % ENCODED_ID_LENGTH_MULTIPLE:
            raise ValueError('Invalid id length, must be multiple of 16')
        m = ENCODED_DATABASE_ID_PATTERN.fullmatch(v.lower())
        if not m:
            raise ValueError('Invalid characters in encoded ID')
        return cls(v)

    def __repr__(self):
        return f'EncodedDatabaseID ({super().__repr__()})'


def ModelClassField(class_name: str) -> str:
    """Represents a database model class name annotated as a constant
    pydantic Field.
    :param class_name: The name of the database class.
    :return: A constant pydantic Field with default annotations for model classes.
    """
    return Field(
        class_name,
        title="Model class",
        description="The name of the database model class.",
        const=True,  # Make this field constant
    )


# Generic and common Field annotations that can be reused across models


UrlField: AnyUrl = Field(
    ...,
    title="URL",
    description="The relative URL to access this item.",
    deprecated=False  # TODO Should this field be deprecated in FastAPI?
)

DownloadUrlField: AnyUrl = Field(
    ...,
    title="Download URL",
    description="The URL to download this item from the server.",
)

AnnotationField: Optional[str] = Field(
    ...,
    title="Annotation",
    description="An annotation to provide details or to help understand the purpose and usage of this item.",
)

AccessibleField: bool = Field(
    ...,
    title="Accessible",
    description="Whether this item is accessible to the current user due to permissions.",
)
