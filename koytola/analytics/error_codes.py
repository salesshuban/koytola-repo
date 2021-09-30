from enum import Enum


class AnalyticsErrorCode(Enum):
    ACCESS_DENIED = "access_denied"
    GRAPHQL_ERROR = "graphql_error"
    INVALID = "invalid"
    NOT_FOUND = "not_found"
    REQUIRED = "required"


class TrackingErrorCode(Enum):
    GRAPHQL_ERROR = "graphql_error"
    INVALID = "invalid"
    TOO_MANY_ITEMS = "too_many_items"
