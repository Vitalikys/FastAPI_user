from fastapi import APIRouter
from starlette.responses import Response, FileResponse

router = APIRouter()


@router.get("/demo_html")
def plain_html():
    """ send html content as a plane text """
    html_content = "<h2>Hello from simple html, using Response from starlette</h2>\
     <br> Content as plain text "
    return Response(media_type="text/html", content=html_content)
    # return HTMLResponse(content=html_content)


@router.get("/cv", name="My CV file")
def cv_url():
    """ send index.html file with css and img dependencies """
    return FileResponse(path="static/resume/index.html")
