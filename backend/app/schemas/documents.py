from pydantic import BaseModel


class DocumentsResponse(BaseModel):
    documents: list[str]