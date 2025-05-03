from aquilify.wrappers import Request, Response
from aquilify import responses

from .registrationModel import UserData

from . import (
    db,
    exceptions,
    shinxmailer
)

from datetime import datetime
from pydantic import ValidationError


class ShinxManagementRegistrationServer:
    def __init__(self):
        pass
    
    async def openAccountFormRoute(self, request: Request) -> Response:
        try:
            if request.method == "POST":
                userData = await request.json()
                modelUserData = UserData(**userData) # Pydantic Model :: 8891
                
                await self._check_existing_user(modelUserData)

                insertionData = self._build_insertion_data(modelUserData)
                
                if not (await db.accountregistrationcollection.insert_one( data = insertionData )).success:
                    raise exceptions.AccountRegistrationError(
                        details = f"Registration Failed! Please try again later.",
                        code = 409  # HTTP Conflict
                    )
                    
                if not shinxmailer.send_email(subject = 'Shinx Management OTP Verification', message = "Text Messages are no longer supported.", recipient = modelUserData.email, context = {"otp": insertionData.get("otp"), "verification_url": request.url}, template_name = "otp_mail.html"):
                    await db.accountregistrationcollection.delete_one(
                        {"_id": insertionData["_id"]}
                    )
                    raise exceptions.AccountRegistrationError(
                        details = f"Registration Failed! Sending Mail error.",
                        code = 409  # HTTP Conflict
                    )
                
                request.session["_id"] = insertionData["_id"]
                request.session["_email"] = modelUserData.email
                request.session["tempId"] = insertionData["tempId"]

                return responses.JsonResponse(
                    content = {"message": "Account Registered Successfully!"}
                )
                            
        except exceptions.AccountRegistrationError as e:
            return responses.JsonResponse(
                content = { "message": e.details }, status = e.code
            )
            
        except ValidationError as ve:
            error_messages = [error['msg'] for error in ve.errors()]
            return responses.JsonResponse(
                {"message": f"{error_messages}"}, status=422
            )

        except Exception as exc:
            return responses.JsonResponse(
                { "message": "Internal Server Error" }, status = 500
            )
            
    async def _check_existing_user(self, model_user: UserData) -> None:
        query = {
            "$or": [
                {"email": model_user.email},
                {"phone": model_user.phone}
            ]
        }
        user = await db.accountregistrationcollection.find_one(query)
        if user.success:
            if user.data.get("email") == model_user.email:
                field = f"email {model_user.email}"
            else:
                field = f"phone {model_user.phone}"
            raise exceptions.AccountRegistrationError(
                details=f"An account with {field} already exists.",
                code=409
            )
            
    def _build_insertion_data(self, model_user: UserData) -> dict:
        dumped_data = model_user.model_dump()
        
        dumped_data["dob"] = model_user.dob.strftime("%Y-%m-%d") 

        data: dict = {
            "id": "$auto",
            "tempId": {"type": "$unique", "length": 11, "format": "numeric"},
            **dumped_data,
            "date": "$date",
            "datetime": "$datetime",
            "otp": {"type": "$unique", "length": 6, "format": "numeric"},
            "timestamps": {
                "account_created": datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            "emailVerified": False
        }
        return data

                
shinxManagementRegistrationServerMethod = ShinxManagementRegistrationServer()