from aquilify import shortcuts
from aquilify import responses
from aquilify.wrappers import Request, Response


async def thankyouMsgViewRoute(request: Request) -> Response:
    if not request.method == "GET":
        return responses.JsonResponse(
            content = {"error": "Method Not Allowed"}, status = 405
        )
    
    if "_id" not in request.session:
        return await shortcuts.redirect("/shinxmanagement/home", 302)
    
    return await shortcuts.render(
        request = request, template_name = "account_thankyou.html"
    )