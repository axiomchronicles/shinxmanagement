from aquilify import shortcuts
from aquilify import responses
from aquilify.wrappers import Request, Response

from authentication.db import accountregistrationcollection
from authentication.exceptions import AccountRegistrationError

async def accountTimelineViewRoute(request: Request) -> Response:
    try:
        if not "_id" in request.session:
            return await shortcuts.redirect("/shinxmanagement/home", status_code = 302)

        userData = await accountregistrationcollection.find_one(
            {"_id": request.session["_id"], "tempId": request.session["tempId"]}
        )
        if not userData.success:
            return await shortcuts.redirect("/shinxmanagement/home", status_code = 302)
        
        return await shortcuts.render(
            request = request, template_name = "account_success.html", context = {
                "timestamps": userData.data["timestamps"],
                "tempId": userData.data["tempId"],
                "email": userData.data["email"]
            }
        )
    
    except AccountRegistrationError as e:
        return responses.JsonResponse(
            content = { "message": e.details }, status = e.code
        )
    except Exception as exc:
        return responses.JsonResponse(
            { "message": "Internal Server Error" }, status = 500
        )