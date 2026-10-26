# 🏛️ Heritage Storytelling Agent (Powered by Sarvam AI)

An AI-driven preservation and storytelling system designed to bring historic manuscripts, inscriptions, and oral archives to life in Indic languages.

---

## 🌟 Core Capabilities

| Capability | Sarvam AI Model / API | Description |
| :--- | :--- | :--- |
| **Oral Archive Transcription** | `saaras:v3` (Speech-to-Text) | Transcribes historical audio recordings, folk testimonies, oral histories, and chants with timestamp support. |
| **Manuscript Translation** | `mayura:v1` (Text Translation) | Preserves cultural nuance and tone across 11+ Indic languages and Indian English. |
| **Creative Heritage Transformation** | `sarvam-105b-conversations` (Indic LLM) | Re-imagines historical records into **guided walking tours**, **podcast episodes**, or **dramatic stories**. |
| **Multilingual Voice Narration** | `bulbul:v3` (Text-to-Speech) | High-fidelity voice synthesis using culturally resonant speakers (`anand`, `aditya`, `vijay`, `kavitha`, `rupali`, etc.). |

---

## 🚀 Quickstart

### 1. Run the Interactive Showcase
```bash
/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 heritage_agent.py
```

### 2. Python SDK Usage

```python
from heritage_agent import HeritageStorytellingAgent

agent = HeritageStorytellingAgent()

# 1. Provide historic excerpt or manuscript
archive = """
Inscriptions from 1010 CE record that Emperor Raja Raja Chola I built the Great
Brihadisvara Temple dedicated to Lord Shiva. The temple vimana rises 66 meters into the sky,
crowned by an 80-ton granite Kumbam carved from a single boulder...
"""

# 2. Run end-to-end transformation & audio generation
result = agent.process_heritage_experience(
    historical_content=archive,
    format_type="tour",           # "tour", "podcast", or "story"
    target_language_code="hi-IN", # "hi-IN", "en-IN", "ta-IN", "te-IN", etc.
    output_filename="thanjavur_tour_hi.wav"
)

print(result["script"])
print(f"Audio saved to: {result['audio_file']}")
```

### 3. Transcribing Oral Archives
```python
# Transcribe an audio interview or folklore recording
transcript_data = agent.transcribe_oral_archive("path/to/archive_recording.mp3")
print(transcript_data["transcript"])

# Translate the oral archive into another language
english_version = agent.translate_manuscript(
    text=transcript_data["transcript"],
    source_language_code=transcript_data["detected_language"],
    target_language_code="en-IN"
)
```

---

## 📁 Directory Structure
```
sarvam-ai/
├── .env                       # API key configuration
├── .gitignore                 # Protects .env
├── main.py                    # Minimal baseline connection test
├── heritage_agent.py          # Full Heritage Storytelling Agent pipeline & CLI
├── heritage_output/           # Generated .wav narration audio files
└── README.md                  # Documentation
```
