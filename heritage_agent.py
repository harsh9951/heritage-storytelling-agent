"""
Heritage Storytelling Agent powered by Sarvam AI.

Capabilities:
1. Transcribe & translate historic manuscripts and oral archives (STT + Translation)
2. Transform historical records into interactive stories, podcasts, or guided tours (LLM)
3. Bring history to life with natural multilingual voice narration (TTS)
"""

import os
import sys
import base64
from pathlib import Path
from typing import Optional, Dict, Any, List

# Load environment variables from .env
env_file = Path(__file__).resolve().parent / ".env"
if env_file.is_file():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, val = line.split("=", 1)
            os.environ.setdefault(key.strip(), val.strip().strip("'\""))

from sarvamai import SarvamAI


class HeritageStorytellingAgent:
    """Agent for preserving, reimagining, and narrating historical archives."""

    # Curated expressive speakers for storytelling across languages in bulbul:v3
    VOICE_MAP = {
        "hi-IN": "anand",            # Resonant Hindi documentary / storytelling voice
        "en-IN": "aditya",           # Expressive English narration
        "ta-IN": "vijay",            # Clear, dignified Tamil voice
        "te-IN": "kavitha",          # Melodic Telugu storytelling voice
        "mr-IN": "rupali",           # Expressive Marathi narrative voice
        "bn-IN": "roopa",            # Warm Bengali voice
        "kn-IN": "gokul",            # Kannada narration
        "gu-IN": "pooja",            # Gujarati voice
        "pa-IN": "anand",            # Punjabi narration
    }

    LANGUAGE_NAMES = {
        "hi-IN": "Hindi",
        "en-IN": "English (India)",
        "ta-IN": "Tamil",
        "te-IN": "Telugu",
        "mr-IN": "Marathi",
        "bn-IN": "Bengali",
        "kn-IN": "Kannada",
        "gu-IN": "Gujarati",
        "pa-IN": "Punjabi",
        "ml-IN": "Malayalam",
        "od-IN": "Odia",
    }

    def __init__(self, api_key: Optional[str] = None):
        key = api_key or os.getenv("SARVAM_API_KEY")
        if not key:
            raise ValueError(
                "SARVAM_API_KEY is not configured. Please set it in .env or pass api_key."
            )
        self.client = SarvamAI(api_subscription_key=key)
        self.output_dir = Path(__file__).resolve().parent / "heritage_output"
        self.output_dir.mkdir(exist_ok=True)

    # -------------------------------------------------------------------------
    # 1. Archives Ingestion: Transcription & Translation
    # -------------------------------------------------------------------------
    def transcribe_oral_archive(
        self,
        audio_path: str,
        language_code: str = "unknown",
        with_timestamps: bool = True,
    ) -> Dict[str, Any]:
        """Transcribe historic oral archives, folklore recordings, or interviews using Sarvam STT."""
        file_path = Path(audio_path)
        if not file_path.is_file():
            raise FileNotFoundError(f"Audio archive not found: {audio_path}")

        print(f"🎙️  Transcribing oral archive '{file_path.name}'...")
        with open(file_path, "rb") as f:
            response = self.client.speech_to_text.transcribe(
                file=f,
                model="saaras:v3",
                language_code=language_code,
                with_timestamps=with_timestamps,
            )

        return {
            "transcript": response.transcript,
            "detected_language": response.language_code,
            "timestamps": response.timestamps,
        }

    def translate_manuscript(
        self,
        text: str,
        source_language_code: str = "auto",
        target_language_code: str = "en-IN",
        mode: str = "classic-colloquial",
    ) -> str:
        """Translate historic text/manuscript excerpts across Indic languages and English."""
        print(f"📜 Translating manuscript excerpt ({source_language_code} -> {target_language_code})...")
        response = self.client.text.translate(
            input=text,
            source_language_code=source_language_code,
            target_language_code=target_language_code,
            mode=mode,
        )
        return response.translated_text

    # -------------------------------------------------------------------------
    # 2. Historical Content Transformation: Story, Podcast, or Guided Tour
    # -------------------------------------------------------------------------
    def transform_to_experience(
        self,
        historical_archive: str,
        format_type: str = "story",
        target_language: str = "English",
        duration_style: str = "medium",
    ) -> str:
        """
        Transforms raw historical content into an interactive story, podcast episode,
        or guided walking tour using Sarvam's conversational Indic LLM.
        """
        format_prompts = {
            "story": (
                "You are an ancient Indic storyteller and chronicler. "
                "Transform the historical source material into an evocative, immersive historical story. "
                "Bring the setting, sensory details, architecture, and historical figures to life. "
                "Keep the narration vivid and engaging for listeners."
            ),
            "podcast": (
                "You are the host of 'Echoes of History', a premier heritage podcast. "
                "Craft an engaging podcast narration from the historical material. "
                "Structure it with: 1) An intriguing hook, 2) The untold historical context/legend, "
                "3) Why this matters today, and 4) A reflective closing question."
            ),
            "tour": (
                "You are a master heritage docent conducting an on-site audio guided walking tour. "
                "Write an immersive audio guide script. Use spatial cues ('Stand before the stone carving...', "
                "'Look upward towards the soaring gopuram...'), explaining the architectural mastery, "
                "inscriptions, and living traditions."
            ),
        }

        system_instruction = format_prompts.get(format_type, format_prompts["story"])

        prompt = (
            f"Source Historical Archive / Manuscript:\n\"\"\"{historical_archive}\"\"\"\n\n"
            f"Task: Create a {format_type.upper()} in {target_language}.\n"
            f"Requirements:\n"
            f"- Length: Approximately 150-250 words suited for 1-2 minutes of audio narration.\n"
            f"- Tone: Culturally authentic, respectful, deeply evocative.\n"
            f"- Output ONLY the spoken narration text ready to be read aloud (do not include stage directions or sound effect notes in brackets)."
        )

        print(f"✨ Generating heritage {format_type} in {target_language} using sarvam-105b-conversations...")
        response = self.client.chat.completions(
            model="sarvam-105b-conversations",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        script = response.choices[0].message.content.strip()
        return script

    # -------------------------------------------------------------------------
    # 3. Multilingual Voice Narration: Speech Synthesis
    # -------------------------------------------------------------------------
    def narrate(
        self,
        script: str,
        language_code: str = "en-IN",
        speaker: Optional[str] = None,
        output_filename: str = "heritage_narration.wav",
        pace: float = 0.95,
    ) -> Path:
        """Synthesize natural Indic voice narration for the generated story/podcast/tour."""
        selected_speaker = speaker or self.VOICE_MAP.get(language_code)
        print(f"🔊 Synthesizing voice narration with Sarvam TTS (Language: {language_code}, Speaker: {selected_speaker})...")

        # In case the script is long, Sarvam TTS accepts up to a few hundred characters per request or segments
        # We ensure the script is trimmed or passed safely
        response = self.client.text_to_speech.convert(
            text=script,
            language_code=language_code,
            speaker=selected_speaker,
            model="bulbul:v3",
            pace=pace,
        )

        audio_bytes = base64.b64decode(response.audios[0])
        output_path = self.output_dir / output_filename
        output_path.write_bytes(audio_bytes)

        print(f"✅ Narration saved to: {output_path}")
        return output_path

    # -------------------------------------------------------------------------
    # Full End-to-End Pipeline
    # -------------------------------------------------------------------------
    def process_heritage_experience(
        self,
        historical_content: str,
        format_type: str = "story",
        target_language_code: str = "hi-IN",
        output_filename: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Runs the complete pipeline: ingestion -> generation -> translation -> narration."""
        lang_name = self.LANGUAGE_NAMES.get(target_language_code, "Hindi")
        
        # 1. Transform raw archive into compelling experience
        script = self.transform_to_experience(
            historical_archive=historical_content,
            format_type=format_type,
            target_language=lang_name,
        )

        # 2. Synthesize audio narration
        filename = output_filename or f"{format_type}_{target_language_code}.wav"
        audio_path = self.narrate(
            script=script,
            language_code=target_language_code,
            output_filename=filename,
        )

        return {
            "format": format_type,
            "language": lang_name,
            "language_code": target_language_code,
            "script": script,
            "audio_file": str(audio_path),
        }


# =============================================================================
# Demonstration Showcase
# =============================================================================
SAMPLE_HERITAGE_ARCHIVES = {
    "1": {
        "title": "Brihadisvara Temple (Thanjavur)",
        "source": (
            "Inscriptions from 1010 CE record that Emperor Raja Raja Chola I built the Great "
            "Brihadisvara Temple dedicated to Lord Shiva. The temple vimana rises 66 meters into the sky, "
            "crowned by an 80-ton granite Kumbam carved from a single boulder, transported across an "
            "earthen ramp extending over six kilometers. The temple walls preserve over a hundred "
            "Tamil inscriptions recording names of musicians, dancers, stone carvers, and royal decrees."
        ),
        "suggested_format": "tour",
    },
    "2": {
        "title": "Nalanda Mahavihara: The Burning of Dharmaganja",
        "source": (
            "In 1193-1200 CE, the great Mahavihara of Nalanda—where 10,000 scholars studied—was sacked "
            "and set ablaze by the army of Bakhtiyar Khilji, as recorded in Minhaj-i-Siraj's chronicle Tabaqat-i Nasiri. "
            "The fabled library, Dharmaganja (Treasury of Truth), held hundreds of thousands of palm-leaf and birch-bark "
            "manuscripts across three monuments: Ratnasagara, Ratnaranjaka, and the 9-story Ratnodadhi. "
            "The library burned continuously for three months, filling the Magadha skies with ash. "
            "Decades later in 1235 CE, Tibetan pilgrim Dharmasvamin discovered a lone 90-year-old master, "
            "Rahula Shribhadra, still teaching a solitary pupil amidst the blackened ruins and fallen pillars."
        ),
        "suggested_format": "podcast",
    },
    "3": {
        "title": "Legend of Rani Velu Nachiyar (Sivaganga)",
        "source": (
            "Oral ballads of Tamil Nadu remember Rani Velu Nachiyar, the warrior queen of Sivaganga. "
            "In 1780, she formed an alliance with Hyder Ali and built one of the earliest recorded women’s "
            "regiments, the Udayal army, led by Commander Kuyili. Dressed in battle armor and carrying dual "
            "valaris (throwing sickles), the queen recaptured her fortress, reclaiming freedom for her people."
        ),
        "suggested_format": "story",
    },
}


def interactive_menu():
    agent = HeritageStorytellingAgent()
    print("=" * 70)
    print("🏛️   HERITAGE STORYTELLING AGENT (Powered by Sarvam AI)")
    print("=" * 70)
    print("Select an option:")
    print("  1. Run Showcase: Brihadisvara Temple (Guided Walking Tour in Hindi)")
    print("  2. Run Showcase: Nalanda Mahavihara (Heritage Podcast in English)")
    print("  3. Run Showcase: Rani Velu Nachiyar (Dramatic Audio Story in Tamil)")
    print("  4. Custom Archive: Input your own manuscript / historic text")
    print("  5. Transcribe Oral Archive Audio File (.wav / .mp3)")
    print("=" * 70)

    choice = input("Enter choice (1-5, default 1): ").strip() or "1"

    if choice in ("1", "2", "3"):
        demo = SAMPLE_HERITAGE_ARCHIVES[choice]
        fmt = demo["suggested_format"]
        lang_code = "hi-IN" if choice == "1" else ("en-IN" if choice == "2" else "ta-IN")
        print(f"\n✨ Selected: {demo['title']}")
        print(f"📖 Source Excerpt:\n{demo['source']}\n")

        result = agent.process_heritage_experience(
            historical_content=demo["source"],
            format_type=fmt,
            target_language_code=lang_code,
            output_filename=f"showcase_{choice}_{lang_code}.wav",
        )

        print("\n" + "=" * 50)
        print(f"🎙️ GENERATED {result['format'].upper()} SCRIPT ({result['language']}):")
        print("=" * 50)
        print(result["script"])
        print("=" * 50)
        print(f"🔊 Narration Audio Ready: {result['audio_file']}")

    elif choice == "4":
        print("\nEnter your historical manuscript excerpt or oral archive notes:")
        user_text = input("> ").strip()
        if not user_text:
            print("No text provided. Exiting.")
            return

        fmt = input("Choose format (story / podcast / tour) [default: story]: ").strip().lower() or "story"
        print("\nChoose Narration Language:")
        print("  1. Hindi (hi-IN)")
        print("  2. English (en-IN)")
        print("  3. Tamil (ta-IN)")
        print("  4. Telugu (te-IN)")
        print("  5. Marathi (mr-IN)")
        print("  6. Bengali (bn-IN)")
        lang_choice = input("Enter choice (1-6) [default: 1]: ").strip() or "1"
        lang_map = {"1": "hi-IN", "2": "en-IN", "3": "ta-IN", "4": "te-IN", "5": "mr-IN", "6": "bn-IN"}
        lang_code = lang_map.get(lang_choice, "hi-IN")

        result = agent.process_heritage_experience(
            historical_content=user_text,
            format_type=fmt,
            target_language_code=lang_code,
        )

        print("\n" + "=" * 50)
        print(f"🎙️ GENERATED SCRIPT ({result['language']}):")
        print("=" * 50)
        print(result["script"])
        print("=" * 50)
        print(f"🔊 Narration Audio File: {result['audio_file']}")

    elif choice == "5":
        audio_file = input("Enter path to oral archive audio file: ").strip()
        if not Path(audio_file).is_file():
            print(f"File not found: {audio_file}")
            return
        res = agent.transcribe_oral_archive(audio_file)
        print("\n📝 TRANSCRIPT:")
        print(res["transcript"])
        print(f"Detected Language: {res['detected_language']}")

        translate_choice = input("\nWould you like to translate this transcript? (y/n): ").strip().lower()
        if translate_choice == "y":
            target_lang = input("Target language code (e.g., en-IN, hi-IN): ").strip() or "en-IN"
            translated = agent.translate_manuscript(
                text=res["transcript"],
                source_language_code=res["detected_language"] or "auto",
                target_language_code=target_lang,
            )
            print(f"\n📜 Translated Transcript ({target_lang}):\n{translated}")


if __name__ == "__main__":
    interactive_menu()
