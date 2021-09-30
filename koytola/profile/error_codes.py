from enum import Enum


class ProfileErrorCode(Enum):
    CONTACT_FILTER = "contact_filter"
    GRAPHQL_ERROR = "graphql_error"
    INVALID = "invalid"
    NOT_FOUND = "not_found"
    REQUIRED = "required"
    SLUG_TAKEN = "slug_taken"
    UNIQUE = "unique"
