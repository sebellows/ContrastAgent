from app.models.tag import Tag
from app.schemas.tag import TagCreateInternal, TagDelete, TagUpdate, TagUpdateInternal

from .crud_adaptor import CRUDAdaptor


CRUDTag = CRUDAdaptor[Tag, TagCreateInternal, TagUpdate, TagUpdateInternal, TagDelete, None]
crud_tags = CRUDTag(Tag)
