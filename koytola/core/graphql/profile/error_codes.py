from enum import Enum


class ProfileErrorCode(Enum):
    ACCESS_DENIED = "access_denied"
    ACTIVE_PROFILE = "active_profile"
    GRAPHQL_ERROR = "graphql_error"
    INACTIVE_PROFILE = "inactive_profile"
    INVALID = "invalid"
    INVALID_PROFILE = "invalid_profile"
    NOT_FOUND = "not_found"
    PUBLISHED_PROFILE = "published_profile"
    REQUIRED = "required"
    UNIQUE = "unique"
    UNPUBLISHED_PROFILE = "unpublished_profile"


