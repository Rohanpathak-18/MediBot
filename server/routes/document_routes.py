import uuid

from pathlib import Path

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from server.services.document_service import (
    process_document
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    allowed_extensions = {
        ".pdf",
        ".docx",
        ".txt"
    }


    extension = Path(
        file.filename
    ).suffix.lower()


    if extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail=(
                "Only PDF, DOCX and TXT "
                "files are supported."
            )
        )


    try:

        # Generate ONE ID
        document_id = str(
            uuid.uuid4()
        )


        # Make sure upload directory exists
        upload_dir = Path(
            "server/data/uploads"
        )

        upload_dir.mkdir(
            parents=True,
            exist_ok=True
        )


        # Save uploaded file
        filename = (
            f"{document_id}{extension}"
        )

        file_path = (
            upload_dir / filename
        )


        contents = await file.read()


        with open(
            file_path,
            "wb"
        ) as f:

            f.write(contents)


        # Process document
        result = process_document(
            str(file_path),
            extension,
            document_id
        )


        return {
            "success": True,
            "document_id": result[
                "document_id"
            ],
            "filename": file.filename,
            "chunks": result["chunks"]
        }


    except Exception as e:

        print(
            "DOCUMENT UPLOAD ERROR:",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )