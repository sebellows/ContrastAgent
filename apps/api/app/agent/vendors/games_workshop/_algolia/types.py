from typing import TypedDict


class CtPrice(TypedDict):
    centAmount: int
    fractionDigits: int
    currencyCode: str

class HighlightResult(TypedDict):
    value: str
    matchLevel: str
    matchedWords: list[str]

class HighlightResults(TypedDict):
    productType: HighlightResult
    name: HighlightResult
    price: HighlightResult
    sku: HighlightResult
    description: HighlightResult

class GwAlgoliaProduct(TypedDict):
    id: str
    productType: str
    version: int
    name: str
    slug: str
    price: float
    ctPrice: CtPrice
    sku: str
    images: list[str]
    description: str
    paintType: list[str]
    paintColourRange: str
    isAvailable: bool
    isPreOrder: bool
    isNewRelease: bool
    isSellingFast: bool
    isWarhammerPlusExclusive: bool
    isSpecialOrderItem: bool
    isGiftProduct: bool
    isRestricted: bool
    isDangerous: bool
    isHazardous: bool
    tabs: list[str]
    statusCode: str
    isInStock: bool
    isProductGuaranteed: bool
    quantityLimits: int
    isWebstoreExclusive: bool
    isAvailableWhileStocksLast: bool
    isLastChanceToBuy: bool
    colourVariants: list[str]
    formatVariants: list[str]
    shipsFromAbroad: bool
    supplyChannel: str
    externalVendorLink: str
    showProductPrice: bool
    objectID: str
    _highlightResult: HighlightResults
