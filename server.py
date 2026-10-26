"""
Web server for the Heritage Storytelling Agent powered by Sarvam AI.
Tracks and synchronizes live credits across sessions.
"""

import os
import json
import uuid
import datetime
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

agent = HeritageStorytellingAgent()
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
OUTPUT_DIR = BASE_DIR / "heritage_output"
CREDITS_FILE = BASE_DIR / "credits.json"
OUTPUT_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)

# -----------------------------------------------------------------------------
# Live Credits Manager
# -----------------------------------------------------------------------------
def get_live_credits_data():
    if not CREDITS_FILE.is_file():
        init_data = {"credits": 50, "total_consumed": 0, "history": []}
        CREDITS_FILE.write_text(json.dumps(init_data, indent=2))
        return init_data
    try:
        return json.loads(CREDITS_FILE.read_text())
    except Exception:
        return {"credits": 50, "total_consumed": 0, "history": []}


def get_live_credits() -> int:
    return int(get_live_credits_data().get("credits", 50))


def deduct_live_credits(amount: int = 1, action: str = "generation") -> int:
    data = get_live_credits_data()
    current = int(data.get("credits", 50))
    new_balance = max(0, current - amount)
    data["credits"] = new_balance
    data["total_consumed"] = int(data.get("total_consumed", 0)) + amount
    if "history" not in data:
        data["history"] = []
    data["history"].append({
        "timestamp": datetime.datetime.now().isoformat(),
        "action": action,
        "deducted": amount,
        "remaining": new_balance,
    })
    # Keep only the last 50 history entries
    data["history"] = data["history"][-50:]
    CREDITS_FILE.write_text(json.dumps(data, indent=2))
    return new_balance


def reset_live_credits(amount: int = 50) -> int:
    data = {
        "credits": amount,
        "total_consumed": 0,
        "history": [{
            "timestamp": datetime.datetime.now().isoformat(),
            "action": "reset",
            "deducted": 0,
            "remaining": amount,
        }]
    }
    CREDITS_FILE.write_text(json.dumps(data, indent=2))
    return amount


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


@routes.get("/api/credits")
async def credits_handler(request):
    """Returns real-time live credits balance and usage stats."""
    data = get_live_credits_data()
    return web.json_response({
        "credits": data.get("credits", 50),
        "total_consumed": data.get("total_consumed", 0),
        "history_count": len(data.get("history", [])),
    })


@routes.post("/api/credits/reset")
async def credits_reset_handler(request):
    """Resets credits balance (default 50)."""
    try:
        req_data = await request.json() if request.can_read_body else {}
        amount = int(req_data.get("amount", 50))
    except Exception:
        amount = 50
    new_bal = reset_live_credits(amount)
    return web.json_response({"success": True, "credits": new_bal})


@routes.post("/api/generate-experience")
async def generate_experience_handler(request):
    """Generates a story, podcast, or tour, and synthesizes audio narration."""
    try:
        current_credits = get_live_credits()
        if current_credits <= 0:
            return web.json_response({
                "success": False,
                "error": "Insufficient credits! Please reset your live credits.",
                "credits": 0,
            }, status=402)

        data = await request.json()
        content = data.get("content", "").strip()
        format_type = data.get("format", "story").strip().lower()
        language_code = data.get("language_code", "hi-IN").strip()

        if not content:
            return web.json_response({"error": "Content is required"}, status=400)

        filename = f"{format_type}_{language_code}_{uuid.uuid4().hex[:8]}.wav"
        result = agent.process_heritage_experience(
            historical_content=content,
            format_type=format_type,
            target_language_code=language_code,
            output_filename=filename,
        )

        remaining = deduct_live_credits(1, f"generate-{format_type}-{language_code}")

        return web.json_response({
            "success": True,
            "format": result["format"],
            "language": result["language"],
            "language_code": result["language_code"],
            "script": result["script"],
            "audio_url": f"/audio/{filename}",
            "filename": filename,
            "credits_remaining": remaining,
        })
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)


@routes.post("/api/transcribe")
async def transcribe_handler(request):
    """Transcribes an uploaded oral archive audio file."""
    try:
        current_credits = get_live_credits()
        if current_credits <= 0:
            return web.json_response({
                "success": False,
                "error": "Insufficient credits! Please reset your live credits.",
                "credits": 0,
            }, status=402)

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

        result = agent.transcribe_oral_archive(str(temp_path))
        remaining = deduct_live_credits(1, "transcribe-oral-archive")

        return web.json_response({
            "success": True,
            "transcript": result["transcript"],
            "detected_language": result["detected_language"],
            "timestamps": result.get("timestamps"),
            "credits_remaining": remaining,
        })
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)


@routes.post("/api/translate")
async def translate_handler(request):
    """Translates text across Indic languages and English."""
    try:
        current_credits = get_live_credits()
        if current_credits <= 0:
            return web.json_response({
                "success": False,
                "error": "Insufficient credits! Please reset your live credits.",
                "credits": 0,
            }, status=402)

        data = await request.json()
        text = data.get("text", "").strip()
        source_lang = data.get("source_language", "auto")
        target_lang = data.get("target_language", "en-IN")
        mode = data.get("mode", "classic-colloquial")

        if not text:
            return web.json_response({"error": "Text is required"}, status=400)

        translated = agent.translate_manuscript(
            text=text,
            source_language_code=source_lang,
            target_language_code=target_lang,
            mode=mode,
        )

        remaining = deduct_live_credits(1, f"translate-{source_lang}-to-{target_lang}")

        return web.json_response({
            "success": True,
            "translated_text": translated,
            "source_language": source_lang,
            "target_language": target_lang,
            "credits_remaining": remaining,
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
