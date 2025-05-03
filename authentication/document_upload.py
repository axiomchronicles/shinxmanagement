from aquilify.wrappers import Request, Response
from aquilify import responses, shortcuts
from aquilify.exception.base import MethodNotAllowed
from . import (
    db,
    exceptions
)

import uuid
import os
import aiofiles

from datetime import datetime

class DocumentVerification:
    
    def __init__(self):
        self.UPLOAD_DIR = "media/documents"
    
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
            
            if not userData.data["emailVerified"] == True:
                return await shortcuts.redirect("/shinxmanagement/account/verify", status_code = 302)
            
            form = await request.form()
            file = form["document"]
            
            await self._save_file(file=file, request=request, doctype = form["docType"])
            return responses.JsonResponse(
                content = {"message": "Document Uploaded Successfully."}
            )
            
        except exceptions.AccountRegistrationError as e:
            return responses.JsonResponse(
                content = { "message": e.details }, status = e.code
            )

        except Exception as exc:
            return responses.JsonResponse(
                { "message": "Internal Server Error" }, status = 500
            )
            
    async def _save_file(self, file, request: Request, doctype: str):
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)

        uid = str(uuid.uuid4())
        filename = file.filename
        ext = os.path.splitext(filename)[1]  # Includes the dot (e.g., '.pdf')

        new_filename = f"{uid}{ext}"
        file_path = os.path.join(self.UPLOAD_DIR, new_filename)

        async with aiofiles.open(file_path, "wb") as out_file:
            while chunk := await file.read(1024):  # Read in chunks
                await out_file.write(chunk)
                
        updatedbQuery = await db.accountregistrationcollection.update_one(
            {"_id": request.session["_id"]},
            {
                "$set": {
                    "document": {
                        "uid": uid,
                        "filename": new_filename,
                        "filext": ext,
                        "path": file_path,
                        "hostUrl": f"{self.UPLOAD_DIR}/{new_filename}",
                        "docType": doctype
                    },
                    "timestamps": {
                        "document_upload": datetime.now().strftime('%Y-%m-%d %H:%M')
                    }
                }
            }
        )
        
        if not updatedbQuery.success:
            raise exceptions.AccountRegistrationError(details="Internal server error! please try again.", code=409)
        
        return True
    
documentverification = DocumentVerification()