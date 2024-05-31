from fastapi import APIRouter, Response, status
from app.controllers.tendencies_controller import TendenciesController

router = APIRouter()

@router.post(
    "/update_trends/",
    tags=["update_trends"],
    response_description="Update Google and Twitter trends",
    status_code=status.HTTP_201_CREATED,
)
async def update_trends(response: Response):
    TendenciesController.update_trends()

    response.status_code = status.HTTP_201_CREATED
    return Response(content=None)
