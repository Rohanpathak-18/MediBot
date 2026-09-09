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


# =========================================================
# PROJECT PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

UPLOAD_DIR = BASE_DIR / "server" / "data" / "uploads"


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


# =========================================================
# UPLOAD DOCUMENT
# =========================================================

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    allowed_extensions = {
        ".pdf",
        ".docx",
        ".txt"
    }


    # -----------------------------------------------------
    # Validate filename
    # -----------------------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is required."
        )


    extension = Path(
        file.filename
    ).suffix.lower()


    # -----------------------------------------------------
    # Validate extension
    # -----------------------------------------------------

    if extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail=(
                "Only PDF, DOCX and TXT "
                "files are supported."
            )
        )


    try:

        # -------------------------------------------------
        # Generate document ID
        # -------------------------------------------------

        document_id = str(
            uuid.uuid4()
        )


        # -------------------------------------------------
        # Create upload directory
        # -------------------------------------------------

        UPLOAD_DIR.mkdir(
            parents=True,
            exist_ok=True
        )


        # -------------------------------------------------
        # Create filename
        # -------------------------------------------------

        filename = (
            f"{document_id}{extension}"
        )


        file_path = (
            UPLOAD_DIR / filename
        )


        # -------------------------------------------------
        # Read uploaded file
        # -------------------------------------------------

        contents = await file.read()


        # -------------------------------------------------
        # Basic file size check
        # 10 MB
        # -------------------------------------------------

        max_size = 10 * 1024 * 1024


        if len(contents) > max_size:

            raise HTTPException(
                status_code=400,
                detail="File size must be below 10 MB."
            )


        # -------------------------------------------------
        # Save file
        # -------------------------------------------------

        with open(
            file_path,
            "wb"
        ) as f:

            f.write(contents)


        print(
            "Document saved:",
            file_path
        )


        # -------------------------------------------------
        # Process document
        # -------------------------------------------------

        result = process_document(

            str(file_path),

            extension,

            document_id

        )


        # -------------------------------------------------
        # Return response
        # -------------------------------------------------

        return {

            "success": True,

            "document_id": result[
                "document_id"
            ],

            "filename": file.filename,

            "chunks": result[
                "chunks"
            ]

        }


    except HTTPException:

        raise


    except Exception as e:

        print(
            "DOCUMENT UPLOAD ERROR:",
            repr(e)
        )


        raise HTTPException(

            status_code=500,

            detail=str(e)

        )