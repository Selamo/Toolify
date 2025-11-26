from fastapi import APIRouter, HTTPException, Form, UploadFile, Depends
from datetime import datetime
from typing import Optional
from app.model.schemas import ChatResponse
from app.chains.chat_chain import _chat_chain
from app.services.vision_service import describe_image
from app.dependencies import optional_image_file_validator

router = APIRouter(prefix="/api", tags=["Chat"])

@router.post("/chat", response_model=ChatResponse)
async def chat(
    message: str = Form(...),
    file: Optional[UploadFile] = Depends(optional_image_file_validator)
):
    """
    A single-turn chat endpoint to converse with the Gemini AI assistant.
    Supports English (en), French (fr), and Nigerian Pidgin (pdg).
    This endpoint can optionally accept an image file for context.
    """
    try:
        full_message = message
        if file:
            image_bytes = await file.read()
            if image_bytes:
                image_description = describe_image(image_bytes)
                if image_description:
                    full_message = (
                        f"The user has uploaded an image with the following description: '{image_description}'.\n"
                        f"The user's message is: '{message}'"
                    )

        # invoke_chat now returns a Pydantic object (LLMStructuredOutput)
        structured_response = await _chat_chain.invoke_chat(full_message)

        return ChatResponse(
            content=structured_response.response,
            language=structured_response.language,
            timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing error: {str(e)}")
