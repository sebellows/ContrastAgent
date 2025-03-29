from app.models.locale_details import LocaleDetails
from app.schemas.locale_details import LocaleDetailsCreateInternal, LocaleDetailsDelete, LocaleDetailsUpdate, LocaleDetailsUpdateInternal

from .crud_adaptor import CRUDAdaptor


CRUDLocaleDetails = CRUDAdaptor[LocaleDetails, LocaleDetailsCreateInternal, LocaleDetailsUpdate, LocaleDetailsUpdateInternal, LocaleDetailsDelete, None]
crud_locale_detailss = CRUDLocaleDetails(LocaleDetails)
