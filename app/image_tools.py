"""Image generation and Cloud Storage upload tools for UrbanNest."""

import json
import uuid
from google import genai
from google.genai import types
from google.adk.tools import ToolContext
from google.cloud import storage

PROJECT_ID = "qwiklabs-gcp-04-6db14bebe7b8"
BUCKET_NAME = "urbannest-assets-6db14bebe7b8"
IMAGE_MODEL = "gemini-3.1-flash-lite-image"


async def generate_property_image(
    prompt: str,
    tool_context: ToolContext = None,
) -> str:
    """Generate a photo or visual rendering of an apartment or property listing and host it publicly.

    Uses gemini-3.1-flash-lite-image in the global region to generate an interior room or
    exterior architectural rendering. Saves the image as an ADK artifact and uploads the bytes
    directly to Cloud Storage, returning the public HTTPS URL.

    Args:
        prompt: Detailed description of the apartment interior or building exterior to generate
            (e.g., 'Modern sunlit living room with hardwood floors and minimalist furniture in San Francisco').
        tool_context: ADK ToolContext injected by runtime for artifact persistence.

    Returns:
        JSON string containing the public HTTPS URL, filename, and status.
    """
    if not prompt:
        return json.dumps({"status": "error", "message": "Prompt cannot be empty."})

    try:
        # Initialize Gemini client in global region for Vertex AI
        genai_client = genai.Client(
            vertexai=True,
            project=PROJECT_ID,
            location="global",
        )

        response = genai_client.models.generate_content(
            model=IMAGE_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=[types.Modality.IMAGE],
            ),
        )

        image_bytes = None
        mime_type = "image/png"

        if response.candidates and response.candidates[0].content:
            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.data:
                    image_bytes = part.inline_data.data
                    mime_type = part.inline_data.mime_type or "image/png"
                    break

        if not image_bytes:
            return json.dumps({
                "status": "error",
                "message": "No image data returned from model.",
            })

        extension = "jpg" if "jpeg" in mime_type else "png"
        filename = f"property_{uuid.uuid4().hex[:10]}.{extension}"

        # 1. Save with tool_context.save_artifact for Playground Artifacts panel
        if tool_context:
            artifact_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
            await tool_context.save_artifact(filename=filename, artifact=artifact_part)

        # 2. Upload same bytes directly to public Cloud Storage bucket
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_string(image_bytes, content_type=mime_type)

        public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"

        return json.dumps({
            "status": "success",
            "public_url": public_url,
            "filename": filename,
            "message": f"Successfully generated property image and published to Cloud Storage: {public_url}",
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Failed to generate or upload property image: {str(e)}",
        })
