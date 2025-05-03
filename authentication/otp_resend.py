from aquilify.wrappers import Request, Response
from aquilify import responses, shortcuts
from . import (
    shinxmailer,
    exceptions,
    db
)
from utils import emails
from aquilify.exception.base import MethodNotAllowed
from datetime import datetime, timedelta

import random

class AuthenticationOTPResend:
    
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
            
            retries = userData.data.get("otp_retries", 0)
            cooldown_ts = userData.data.get("otp_cooldown")
            now = datetime.now()

            if retries >= 3:
                if cooldown_ts:
                    cooldown_end_time = datetime.strptime(cooldown_ts, "%Y-%m-%d %H:%M:%S")
                    if now < cooldown_end_time:
                        raise exceptions.AccountRegistrationError(
                            f"OTP limit exceeded! Please try again after {cooldown_end_time.strftime('%H:%M:%S')}."
                        )
                # Cooldown expired or never set → set new cooldown
                otp_cooldown_time = now + timedelta(minutes=10)
                await db.accountregistrationcollection.update_one(
                    {"_id": request.session["_id"], "tempId": request.session["tempId"]},
                    {
                        "$set": {
                            "otp_cooldown": otp_cooldown_time.strftime("%Y-%m-%d %H:%M:%S"),
                            "otp_retries": 0
                        }
                    }
                )
                raise exceptions.AccountRegistrationError(
                    f"OTP limit exceeded! Please try again after {otp_cooldown_time.strftime('%H:%M:%S')}.", code = 409
                )
            
            await db.accountregistrationcollection.update_one(
                {"_id": request.session["_id"], "tempId": request.session["tempId"]},
                {
                    "$set": {
                        "otp_retries": retries + 1
                    }
                }
            )
            
            await self._generate_otp(request = request, user = userData.data)
            
            return responses.JsonResponse(
                {"message": "OTP Sent Successfully."}
            )
            
        except exceptions.AccountRegistrationError as e:
            return responses.JsonResponse(
                content = { "message": e.details }, status = e.code
            )

        except Exception as exc:
            return responses.JsonResponse(
                { "message": "Internal Server Error" }, status = 500
            )
            
    async def _generate_otp(self, request: Request, user):
        otp = random.randint(100000, 999999)
        updateDataquery = await db.accountregistrationcollection.update_one(
            {"_id": request.session["_id"]},
            {
                "$set": {
                    "otp": str(otp)
                }
            }
        )
        
        if not updateDataquery.success:
            raise exceptions.AccountRegistrationError(details = "Internal Server error! please try again.", code=409)
        
        mailer = shinxmailer.send_email(subject = "🎉 Email Verification Successful", message = "Text Messages are no longer supported.", recipient = user['email'], context = {"otp": otp, "verification_url": request.url}, template_name = "otp_mail.html")
        if not mailer:
            raise exceptions.AccountRegistrationError(details = "Mailer Not Responding! please try again.", code = 409)
        
        return True
    
authenticationresend = AuthenticationOTPResend()