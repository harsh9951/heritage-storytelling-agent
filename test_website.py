"""
Comprehensive test suite for the Heritage Storytelling Agent website & backend.
"""

import sys
import json
import urllib.request
import urllib.error

BASE_URL = "http://localhost:8080"

def log_test(name, passed, detail=""):
    symbol = "✅" if passed else "❌"
    print(f"{symbol} {name}")
    if detail:
        print(f"   ↳ {detail}")

def test_homepage():
    try:
        with urllib.request.urlopen(f"{BASE_URL}/") as resp:
            status = resp.status
            content = resp.read().decode("utf-8")
            has_credits = "credits-badge" in content
            has_title = "HERITAGE STORYTELLER" in content
            passed = status == 200 and has_credits and has_title
            log_test("Homepage (GET /)", passed, f"Status: {status}, Credits Element: {has_credits}")
            return passed
    except Exception as e:
        log_test("Homepage (GET /)", False, str(e))
        return False

def test_samples():
    try:
        with urllib.request.urlopen(f"{BASE_URL}/api/samples") as resp:
            status = resp.status
            data = json.loads(resp.read().decode("utf-8"))
            count = len(data)
            passed = status == 200 and count >= 6
            titles = [d.get("title") for d in data.values()]
            log_test("Archives Catalog (GET /api/samples)", passed, f"Found {count} archives: {', '.join(titles[:3])}...")
            return passed
    except Exception as e:
        log_test("Archives Catalog (GET /api/samples)", False, str(e))
        return False

def test_translation():
    try:
        payload = json.dumps({
            "text": "Nalanda was the ancient center of learning in Magadha.",
            "source_language": "en-IN",
            "target_language": "hi-IN"
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{BASE_URL}/api/translate",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            translated = data.get("translated_text", "")
            passed = data.get("success") and len(translated) > 0
            log_test("Translation API (POST /api/translate)", passed, f"Result: '{translated}'")
            return passed
    except Exception as e:
        log_test("Translation API (POST /api/translate)", False, str(e))
        return False

def test_generation_and_audio():
    try:
        payload = json.dumps({
            "content": "In 1010 CE, Emperor Raja Raja Chola I built the Great Brihadisvara Temple crowned by an 80-ton granite stone.",
            "format": "story",
            "language_code": "hi-IN"
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{BASE_URL}/api/generate-experience",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        print("   ⏳ Calling sarvam-105b & bulbul:v3...")
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            script = data.get("script", "")
            audio_url = data.get("audio_url", "")
            gen_passed = data.get("success") and len(script) > 0 and len(audio_url) > 0
            log_test("Experience Generation (POST /api/generate-experience)", gen_passed, f"Script: {len(script.split())} words, Audio: {audio_url}")

            if not gen_passed:
                return False

            # Verify the audio URL streams correctly
            with urllib.request.urlopen(f"{BASE_URL}{audio_url}") as audio_resp:
                audio_status = audio_resp.status
                audio_len = len(audio_resp.read())
                audio_passed = audio_status == 200 and audio_len > 100000
                log_test("Audio Streaming (GET /audio/...)", audio_passed, f"Status: {audio_status}, Audio Size: {audio_len / 1024:.1f} KB")
                return audio_passed
    except Exception as e:
        log_test("Experience Generation & Audio Streaming", False, str(e))
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 RUNNING HERITAGE STORYTELLER TEST SUITE")
    print("=" * 60)
    
    results = [
        test_homepage(),
        test_samples(),
        test_translation(),
        test_generation_and_audio(),
    ]

    passed_count = sum(1 for r in results if r)
    print("=" * 60)
    print(f"Summary: {passed_count}/{len(results)} tests passed.")
    print("=" * 60)
    if passed_count < len(results):
        sys.exit(1)
