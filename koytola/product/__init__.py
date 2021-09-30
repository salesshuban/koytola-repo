from enum import Enum


class ProductAvailabilityStatus(str, Enum):
    NOT_PUBLISHED = "not-published"
    OUT_OF_STOCK = "out-of-stock"
    LOW_STOCK = "low-stock"
    NOT_YET_AVAILABLE = "not-yet-available"
    READY_FOR_PURCHASE = "ready-for-purchase"

    @staticmethod
    def get_display(status):
        status_mapping = {
            ProductAvailabilityStatus.NOT_PUBLISHED: "not published",
            ProductAvailabilityStatus.OUT_OF_STOCK: "out of stock",
            ProductAvailabilityStatus.LOW_STOCK: "stock running low",
            ProductAvailabilityStatus.NOT_YET_AVAILABLE: "not yet available",
            ProductAvailabilityStatus.READY_FOR_PURCHASE: "ready for purchase",
        }

        if status in status_mapping:
            return status_mapping[status]
        else:
            raise NotImplementedError(f"Unknown status: {status}")


class ProductUnits:
    """The price unit types per product unit."""

    CM = "centimeter"
    CM2 = "centimeter-square"
    CM3 = "centimeter-cube"
    GAL = "gallon"
    GRAM = "gram"
    ITEM = "item"
    KG = "kilogram"
    LB = "lbm"
    LT = "liter"
    MG = "milligram"
    MM = "millimeter"
    MM2 = "millimeter-square"
    MM3 = "millimeter-cube"
    MT = "meter"
    MT2 = "meter-square"
    MT3 = "meter-cube"
    OZ = "ounce"
    TON = "ton"

    CHOICES = [
        (CM, "Centi-Meter unit"),
        (CM2, "Centi-Meter Square Unit"),
        (CM3, "Centi-Meter Cube Unit"),
        (GAL, "Gallon unit"),
        (GRAM, "Gram unit"),
        (ITEM, "Item unit"),
        (KG, "Kilo-Gram unit"),
        (LB, "Pound unit"),
        (LT, "Liter unit"),
        (MG, "Milli-Gram unit"),
        (MM, "Milli-Meter unit"),
        (MM2, "Milli-Meter Square unit"),
        (MM3, "Milli-Meter Cube unit"),
        (MT, "Meter unit"),
        (MT2, "Meter Square Unit"),
        (MT3, "Meter Cube unit"),
        (OZ, "Ounce unit"),
        (TON, "Ton unit"),
    ]


class DeliveryTimeOption:
    RTS = "ready to ship"
    NTTS = "needs time to ship"

    CHOICES = [
        (RTS, "Ready To Ship"),
        (NTTS, "Needs Time To Ship"),
    ]
