from aquilify.wrappers import Request, Response
from . import exceptions, db
from aquilify.exception.base import MethodNotAllowed
from aquilify import responses, shortcuts

import random
from datetime import datetime

from . import shinxmailer

class AuthenticationOTPVerification:
    def __init__(self):
        pass
    
    async def main(self, request: Request) -> Response:
        try:
            if not request.method == "POST":
                raise MethodNotAllowed
                        
            if not "_id" in request.session:
                return await shortcuts.redirect("/shinxmanagement/home", status_code = 302)
            
            userData = await db.accountregistrationcollection.find_one(
                {"_id": request.session["_id"], "tempId": request.session["tempId"]}
            )
            
            if not userData.success:
                return await shortcuts.redirect("/shinxmanagement/home", status_code = 302)
            
            userinput = await request.json()
            
            if not ( userinput["otp"] == userData.data["otp"] ):
                raise exceptions.AccountRegistrationError(
                    details = "Invalid Otp! Please try again.", code = 409
                )
                
            query = await db.accountregistrationcollection.update_one(
                { "_id": userData.data["_id"]},
                {
                    "$set": {
                        "emailVerified": True, 
                        "emailVerifiedDateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "timestamps": {
                            "account_verified": datetime.now().strftime('%Y-%m-%d %H:%M')
                        }
                    }
                }
            )
            
            if not query.success:
                raise exceptions.AccountRegistrationError(
                    details = "Something went wrong! please try again."
                )
            
            if not shinxmailer.send_email(subject = "🎉 Email Verification Successful", message = "Text Messages are no longer supported.", recipient = request.session["_email"], context = {"name": userData.data["fullname"]}, template_name = "mails/email_verified.html"):
                raise exceptions.AccountRegistrationError(
                    details = f"Something Went wrong! please try again.",
                    code = 409  # HTTP Conflict
                )
            
            return responses.JsonResponse(
                content = {"message": "OTP Successfully Verified."}
            )
            
        except exceptions.AccountRegistrationError as e:
            return responses.JsonResponse(
                content = { "message": e.details }, status = e.code
            )

        except Exception as exc:
            import traceback
            traceback.print_exc()
            return responses.JsonResponse(
                { "message": "Internal Server Error" }, status = 500
            )
            
authenticationotpverification = AuthenticationOTPVerification()