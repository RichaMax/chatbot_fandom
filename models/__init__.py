from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    """
    This class is a base class to be used for our pydantic model that automatically transforms field names to camel case.

    We use camel case for our JSON APIs (see https://archlet.atlassian.net/wiki/spaces/Engineering/pages/2664038521/RESTful+API+Design+Guidelines#snake_case-vs.-camelCase-for-Field-Names)
    when dumping to JSON.
    Internally, we still use snake case for our field names.
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
