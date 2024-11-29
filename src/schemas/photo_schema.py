from pydantic import BaseModel


class PhotoBase(BaseModel):
    id: str
    file_id: str


class PhotoCreate(PhotoBase):
    pass


class PhotoUpdate(PhotoBase):
    pass


class PhotoResponse(PhotoBase):
    pass


class PhotoListResponse(PhotoBase):
    pass
