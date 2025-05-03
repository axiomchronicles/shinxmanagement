from aquilify import shortcuts
from aquilify import responses
from aquilify.wrappers import Request, Response

from utils import emails

async def accountVerificationViewRoute(request: Request) -> Response:
    if not request.method == "GET":
        return responses.JsonResponse(
            content = {"error": "Method Not Allowed"}, status = 405
        )
        
    return await shortcuts.render(
        request = request, template_name = "email_verification.html", context = { "email": emails.mask_email(request.session["_email"]) if "_email" in request.session else None }
    )