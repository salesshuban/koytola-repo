from ...analytics import TrackingTypes
from ...graphql.core.enums import to_enum


TrackingTypeEnum = to_enum(TrackingTypes, type_name="TrackingTypeEnum")
