from aquilify import shortcuts
from aquilify import responses
from aquilify.wrappers import Request, Response


async def documentUploadViewRoute(request: Request) -> Response:
    if not request.method == "GET":
        return responses.JsonResponse(
            content = {"error": "Method Not Allowed"}, status = 405
        )
        
    return await shortcuts.render(
        request = request, template_name = "document_upload.html"
    )