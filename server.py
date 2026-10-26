"""
Web server for the Heritage Storytelling Agent powered by Sarvam AI.
Supports both default server API key and custom user-provided API keys.
"""

import os
import uuid
from pathlib import Path
from aiohttp import web

# Load .env
env_file = Path(__file__).resolve().parent / ".env"
if env_file.is_file():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, val = line.split("=", 1)
            os.environ.setdefault(key.strip(), val.strip().strip("'\""))

from heritage_agent import HeritageStorytellingAgent, SAMPLE_HERITAGE_ARCHIVES

default_agent = HeritageStorytellingAgent()
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
OUTPUT_DIR = BASE_DIR / "heritage_output"
OUTPUT_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)


def get_agent_for_request(request) -> tuple[HeritageStorytellingAgent, bool]:
    """
    Returns an agent instance:
    - If caller sends custom 'x-sarvam-api-key', use their key.
    - Otherwise, falls back to the server's default agent (configured with SARVAM_API_KEY).
    """
    custom_key = request.headers.get("x-sarvam-api-key", "").strip()
    if custom_key:
        return HeritageStorytellingAgent(api_key=custom_key), True
    return default_agent, False


routes = web.RouteTableDef()


@routes.get("/")
async def index_handler(request):
    index_file = STATIC_DIR / "index.html"
    if not index_file.is_file():
        return web.Response(text="index.html not found", status=404)
    return web.FileResponse(index_file)


@routes.get("/api/samples")
async def samples_handler(request):
    """Returns curated heritage archives for quick demoing."""
    return web.json_response(SAMPLE_HERITAGE_ARCHIVES)


@routes.post("/api/generate-experience")
async def generate_experience_handler(request):
    """Generates a story, podcast, or tour, and synthesizes audio narration."""
    try:
        active_agent, is_custom = get_agent_for_request(request)

        data = await request.json()
        content = data.get("content", "").strip()
        format_type = data.get("format", "story").strip().lower()
        language_code = data.get("language_code", "hi-IN").strip()

        if not content:
            return web.json_response({"error": "Content is required"}, status=400)

        filename = f"{format_type}_{language_code}_{uuid.uuid4().hex[:8]}.wav"
        result = active_agent.process_heritage_experience(
            historical_content=content,
            format_type=format_type,
            target_language_code=language_code,
            output_filename=filename,
        )

        return web.json_response({
            "success": True,
            "format": result["format"],
            "language": result["language"],
            "language_code": result["language_code"],
            "script": result["script"],
            "audio_url": f"/audio/{filename}",
            "filename": filename,
            "used_custom_key": is_custom,
        })
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)


@routes.post("/api/transcribe")
async def transcribe_handler(request):
    """Transcribes an uploaded oral archive audio file."""
    try:
        active_agent, is_custom = get_agent_for_request(request)

        reader = await request.multipart()
        field = await reader.next()
        if not field or field.name != "audio":
            return web.json_response({"error": "Audio file field 'audio' expected"}, status=400)

        filename = f"upload_{uuid.uuid4().hex[:8]}_{field.filename or 'audio.wav'}"
        temp_path = OUTPUT_DIR / filename

        with open(temp_path, "wb") as f:
            while True:
                chunk = await field.read_chunk()
                if not chunk:
                    break
                f.write(chunk)

        result = active_agent.transcribe_oral_archive(str(temp_path))

        return web.json_response({
            "success": True,
            "transcript": result["transcript"],
            "detected_language": result["detected_language"],
            "timestamps": result.get("timestamps"),
            "used_custom_key": is_custom,
        })
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)


@routes.post("/api/translate")
async def translate_handler(request):
    """Translates text across Indic languages and English."""
    try:
        active_agent, is_custom = get_agent_for_request(request)

        data = await request.json()
        text = data.get("text", "").strip()
        source_lang = data.get("source_language", "auto")
        target_lang = data.get("target_language", "en-IN")
        mode = data.get("mode", "classic-colloquial")

        if not text:
            return web.json_response({"error": "Text is required"}, status=400)

        translated = active_agent.translate_manuscript(
            text=text,
            source_language_code=source_lang,
            target_language_code=target_lang,
            mode=mode,
        )

        return web.json_response({
            "success": True,
            "translated_text": translated,
            "source_language": source_lang,
            "target_language": target_lang,
            "used_custom_key": is_custom,
        })
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)


@routes.get("/audio/{filename}")
async def audio_handler(request):
    """Serves generated narration audio files with correct streaming headers."""
    filename = request.match_info["filename"]
    audio_path = OUTPUT_DIR / filename
    if not audio_path.is_file():
        return web.Response(text="Audio file not found", status=404)
    return web.FileResponse(
        audio_path,
        headers={
            "Content-Type": "audio/wav",
            "Accept-Ranges": "bytes",
            "Cache-Control": "public, max-age=3600",
        },
    )


def create_app():
    app = web.Application(client_max_size=50 * 1024 * 1024)  # 50 MB max upload
    app.add_routes(routes)
    return app


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app = create_app()
    print(f"🚀 Heritage Storytelling Agent Web Server starting on http://localhost:{port}")
    web.run_app(app, host="0.0.0.0", port=port)
