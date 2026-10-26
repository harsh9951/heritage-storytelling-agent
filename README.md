# 🏛️ Heritage Storytelling Agent (Powered by Sarvam AI)

An AI-driven preservation and storytelling system designed to bring historic manuscripts, inscriptions, and oral archives to life across Indic languages.

---

## 🌟 Core Capabilities

| Capability | Sarvam AI Model / API | Description |
| :--- | :--- | :--- |
| **Oral Archive Transcription** | `saaras:v3` (Speech-to-Text) | Transcribes historical audio recordings, folk testimonies, oral histories, and chants with timestamp and language detection. |
| **Manuscript Translation** | `mayura:v1` (Text Translation) | Preserves cultural nuance and tone across 11+ Indic languages and Indian English. |
| **Creative Heritage Transformation** | `sarvam-105b-conversations` (Indic LLM) | Re-imagines historical records into **guided walking tours**, **podcast episodes**, or **dramatic stories**. |
| **Multilingual Voice Narration** | `bulbul:v3` (Text-to-Speech) | High-fidelity voice synthesis using culturally resonant speakers (`anand`, `aditya`, `vijay`, `kavitha`, `rupali`, etc.). |

---

## 🌐 Web Application & Live Demo

The project includes an interactive web application featuring an audio player, curated archive explorer, and oral archive ingestion tools.

### Running the Web Server Locally
```bash
/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 server.py
```
Then visit **`http://localhost:8080`** in your browser.

---

## 🏛️ Curated Heritage Archives Gallery

The application includes six pre-built historical archives spanning diverse civilizations, dynasties, and regions across India:

1. **Brihadisvara Temple: The Granite Marvel** (1010 CE • Chola Dynasty, Tamil Nadu) — Guided Walking Tour in Hindi (`hi-IN`).
2. **The Burning of Nalanda Mahavihara** (1193 CE • Magadha, Bihar) — Heritage Podcast in Indian English (`en-IN`) covering the tragic destruction of the 9-story *Dharmaganja* library and the last master *Rahula Shribhadra*.
3. **Konark Sun Temple: The Cosmic Chariot** (13th Century CE • Eastern Ganga Dynasty, Odisha) — Podcast in Hindi (`hi-IN`) detailing the 24 astronomical sundial wheels and the legend of Dharmapada.
4. **Hampi & the Musical Pillars of Vijayanagara** (15th–16th Century CE • Karnataka) — Walking Tour in English (`en-IN`) exploring the monolithic resonant granite pillars of the Vittala Temple.
5. **Legend of Rani Velu Nachiyar & the Kuyili Army** (1780 CE • Sivaganga, Tamil Nadu) — Dramatic Oral Story in Tamil (`ta-IN`) celebrating the first warrior queen to defeat the East India Company.
6. **Dholavira: Harappan Hydraulic Engineering** (2500 BCE • Indus Valley, Gujarat) — Exploration of ancient desert rainwater harvesting and the giant 10-glyph Indus signboard.

---

## 🚀 CLI & Python SDK Usage

### 1. Interactive CLI Showcase
```bash
/Library/Frameworks/Python.framework/Versions/3.14/bin/python3 heritage_agent.py
```

### 2. Python Programmatic Usage
```python
from heritage_agent import HeritageStorytellingAgent

agent = HeritageStorytellingAgent()

archive = """
Inscriptions from 1010 CE record that Emperor Raja Raja Chola I built the Great
Brihadisvara Temple dedicated to Lord Shiva. The temple vimana rises 66 meters into the sky,
crowned by an 80-ton granite Kumbam carved from a single boulder...
"""

# Transform archive into a guided walking tour with voice narration
result = agent.process_heritage_experience(
    historical_content=archive,
    format_type="tour",           # "tour", "podcast", or "story"
    target_language_code="hi-IN", # "hi-IN", "en-IN", "ta-IN", "te-IN", etc.
    output_filename="thanjavur_tour_hi.wav"
)

print("Generated Script:", result["script"])
print("Narration Audio:", result["audio_file"])
```

### 3. Transcribing & Translating Oral Archives
```python
# Transcribe oral folklore recording
transcript_data = agent.transcribe_oral_archive("oral_history_interview.mp3")
print("Transcript:", transcript_data["transcript"])

# Translate across Indic languages
translated = agent.translate_manuscript(
    text=transcript_data["transcript"],
    source_language_code=transcript_data["detected_language"],
    target_language_code="en-IN"
)
print("Translated:", translated)
```

---

## 📁 Directory Structure
```
heritage-storytelling-agent/
├── .env.example               # Safe environment variable template
├── .gitignore                 # Strictly ignores .env and audio outputs
├── README.md                  # Comprehensive project documentation
├── server.py                  # Async aiohttp web server & API endpoints
├── heritage_agent.py          # Complete agent pipeline & interactive CLI
├── main.py                    # Minimal baseline connection test
├── static/
│   └── index.html             # Full-featured responsive web interface
└── heritage_output/
    └── .gitkeep               # Preserves audio output directory
```
