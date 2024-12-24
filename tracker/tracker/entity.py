from pydantic import BaseModel, Field


class Trace(BaseModel):
    id: str = Field(..., title="The ID of the trace item")

    request: dict = Field(..., title="The request object")
    response: dict = Field(..., title="The response object")

    created_at: str = Field(..., title="The timestamp of the trace item creation")
    updated_at: str = Field(..., title="The timestamp of the trace item update")
