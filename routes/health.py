import os
from dotenv import load_dotenv
from typing import Literal
from pydantic import BaseModel, Field
from fastapi import APIRouter, status

load_dotenv()


class StatusResponseModel(BaseModel):
    version: str = Field("1.0", max_length=10)
    filesystem: Literal["nt", "posix"]
    maintenance: bool


router = APIRouter(
    prefix="/health",
    tags=['Health']
)


@router.get(
    "/status",
    response_model=StatusResponseModel,
    status_code=status.HTTP_200_OK,
    summary="Get the status of Smart-Car-Lock API"
)
async def get_status():

    return StatusResponseModel(
        version=os.getenv("VERSION", "Unknown"),
        filesystem=os.name,
        maintenance=False
    )
