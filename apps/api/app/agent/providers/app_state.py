# standard
from typing import TYPE_CHECKING

from app.agent.configuration import locales


if TYPE_CHECKING:
    from app.agent.configuration import LocaleDetails
    from app.agent.models.product_line import ProductLineABC as ProductLine
    from app.agent.models.vendor import VendorABC as Vendor


class AppState:
    _locale = 'en-US'
    _product_line: ProductLine | None = None
    _vendor: Vendor = None

    @property
    def locale(self):
        return self._locale

    @property
    def language(self):
        return self.locale[0:2]

    @property
    def country(self):
        return self.locale[3:]

    @property
    def locale_details(self) -> LocaleDetails:
        return locales.get(self.country, locales['US'])

    @property
    def vendor(self) -> Vendor:
        if self._vendor is None:
            raise ValueError("Vendor is not set")
        if not isinstance(self._vendor, Vendor):
            raise TypeError("Vendor must be of type Vendor")
        return self._vendor

    @vendor.setter
    def vendor(self, vendor: Vendor):
        self._vendor = vendor

    @property
    def product_line(self) -> ProductLine | None:
        if self._product_line is None:
            raise ValueError("Product line is not set")
        if not isinstance(self._product_line, ProductLine):
            raise TypeError("Product line must be of type ProductLine")
        return self._product_line

    @product_line.setter
    def product_line(self, product_line: ProductLine):
        self._product_line = product_line

    def change_locale(self, locale: str):
        if self.is_valid_locale(locale):
            self._locale = locale
    
    def is_valid_locale(self, locale: str):
        return self.vendor and locale in self.vendor.config.supported_locales



# #  standard
# from abc import ABC, abstractmethod

# class AppStateABC(ABC):
#     @property
#     @abstractmethod
#     def vendor(self):
#         pass

#     @vendor.setter
#     @abstractmethod
#     def vendor(self, vendor):
#         pass

#     @property
#     @abstractmethod
#     def product_line(self):
#         pass

#     @product_line.setter
#     @abstractmethod
#     def product_line(self, product_line):
#         pass

#     @property
#     @abstractmethod
#     def locale(self):
#         pass

#     @property
#     @abstractmethod
#     def language(self):
#         pass

#     @property
#     @abstractmethod
#     def country(self):
#         pass

#     @abstractmethod
#     def change_locale(self, locale):
#         pass

#     @abstractmethod
#     def is_valid_locale(self, locale):
#         pass

# AppStateABC.register(AppState)
