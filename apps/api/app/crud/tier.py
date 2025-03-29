from app.models.tier import Tier
from app.schemas.tier import TierCreateInternal, TierDelete, TierUpdate, TierUpdateInternal

from .crud_adaptor import CRUDAdaptor


CRUDTier = CRUDAdaptor[Tier, TierCreateInternal, TierUpdate, TierUpdateInternal, TierDelete, None]
crud_tiers = CRUDTier(Tier)
