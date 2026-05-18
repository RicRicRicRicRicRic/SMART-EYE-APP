from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
import uuid

from ..database import get_db
from ..models.emergency_responder import EmergencyResponder
from ..endpoints.user_info import get_current_user
from ..config.supabase import supabase_client

router = APIRouter(prefix="/me", tags=["Profile"])


@router.post("/profile-picture", status_code=status.HTTP_200_OK)
async def upload_profile_picture(
    file: UploadFile = File(...),
    current_user: EmergencyResponder = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print(f"DEBUG UPLOAD: Filename={file.filename}, Content-Type={file.content_type}, Size={file.size}")

    # Accept images
    image_extensions = {'jpg', 'jpeg', 'png', 'webp', 'gif'}
    file_ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""

    if file_ext not in image_extensions and not (file.content_type and file.content_type.startswith("image/")):
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Only images allowed. Got: {file.filename} ({file.content_type})"
        )

    ext = file_ext if file_ext else "jpg"
    file_name = f"{current_user.responder_id}/{uuid.uuid4()}.{ext}"

    try:
        contents = await file.read()
        if len(contents) == 0:
            raise HTTPException(400, detail="Empty file")

        # Upload to Supabase - Fixed options
        supabase_client.client.storage.from_("profile_pictures").upload(
            file_name, 
            contents,
            file_options={
                "content-type": file.content_type or f"image/{ext}",
                "upsert": "true"          # Must be string "true"
            }
        )

        public_url = supabase_client.client.storage.from_("profile_pictures").get_public_url(file_name)

        current_user.profile_picture_url = public_url
        db.commit()
        db.refresh(current_user)

        print(f"DEBUG UPLOAD SUCCESS: {public_url}")
        return {
            "message": "Profile picture uploaded successfully",
            "profile_picture_url": public_url
        }

    except Exception as e:
        print(f"DEBUG UPLOAD ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")