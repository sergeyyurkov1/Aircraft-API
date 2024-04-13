from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    Security,
)
from fastapi.responses import Response
from pydantic import AnyUrl

import dependencies
from models import screenshoter

router = APIRouter()


# Important to include response_class=Response for automatic documentation
@router.post(
    "/screenshot/v1/site/",
    tags=["Screenshoter"],
    response_class=Response,
    dependencies=[Security(dependencies.get_api_key)],
    deprecated=True,
)
def take_screenshot_of_a_website(
    site_url: AnyUrl = Query(
        ..., description="URL of the site to take a screenshot of"
    ),
    # site_url: AnyUrl,
):
    content = screenshoter.take_screenshot(site_url)
    if content:
        return Response(content=content, media_type="image/png")
    else:
        raise HTTPException(
            status_code=400, detail=f"Cannot take a screenshot of <{site_url}>"
        )
