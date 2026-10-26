# 🏛️ Heritage Storytelling Agent (Powered by Sarvam AI)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/harsh9951/heritage-storytelling-agent)
[![Live Web App](https://img.shields.io/badge/Live%20Demo-Available%20Now-success?style=for-the-badge&logo=cloudflare)](https://upgrading-casinos-gasoline-usd.trycloudflare.com)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue?style=for-the-badge&logo=github)](https://github.com/harsh9951/heritage-storytelling-agent)
[![Powered by](https://img.shields.io/badge/AI-Sarvam%20Indic%20Models-orange?style=for-the-badge)](https://sarvam.ai)

An AI-driven preservation and storytelling system designed to bring historic manuscripts, inscriptions, and oral archives to life across Indic languages using Sarvam AI's Indic models.

---

## 🔗 Live Server & Deployment Links

| Resource | URL | Description |
| :--- | :--- | :--- |
| 🌐 **Live Public Web App** | [https://upgrading-casinos-gasoline-usd.trycloudflare.com](https://upgrading-casinos-gasoline-usd.trycloudflare.com) | Live HTTPS deployment running on Cloudflare Tunnel |
| 🖥️ **Local Web Server** | [http://localhost:8080](http://localhost:8080) | Default local server address when running locally |
| 📦 **GitHub Repository** | [https://github.com/harsh9951/heritage-storytelling-agent](https://github.com/harsh9951/heritage-storytelling-agent) | Full source code, documentation & assets |

---

## 📡 Server REST API Endpoints

The web server (`server.py`) provides the following JSON & streaming endpoints:

| Method | Endpoint | Description | Request Payload / Params |
| :---: | :--- | :--- | :--- |
| `GET` | `/` | Web application frontend | None (serves `static/index.html`) |
| `GET` | `/api/samples` | Fetch pre-built historical archives & summaries | None |
| `POST` | `/api/generate-experience` | Generate story/tour/podcast & synthesize speech | `{"content": "...", "format": "tour"\|"podcast"\|"story", "language_code": "hi-IN"}` |
| `POST` | `/api/transcribe` | Transcribe oral archive audio using `saaras:v3` | Multipart form data with `audio` file |
| `POST` | `/api/translate` | Translate text across Indic languages with `mayura:v1` | `{"text": "...", "source_language": "auto", "target_language": "en-IN"}` |
| `GET` | `/audio/{filename}` | Stream and download generated narration audio | Audio filename (`.wav`) |

---

## 🌟 Core Capabilities & Sarvam AI Stack

| Capability | Sarvam AI Model / API | Description |
| :--- | :--- | :--- |
| **Oral Archive Transcription** | `saaras:v3` (Speech-to-Text) | Transcribes historical audio recordings, folk testimonies, oral histories, and chants with timestamp and language detection. |
| **Manuscript Translation** | `mayura:v1` (Text Translation) | Preserves cultural nuance and tone across 11+ Indic languages and Indian English. |
| **Creative Heritage Transformation** | `sarvam-105b-conversations` (Indic LLM) | Re-imagines historical records into **guided walking tours**, **podcast episodes**, or **dramatic stories**. |
| **Multilingual Voice Narration** | `bulbul:v3` (Text-to-Speech) | High-fidelity voice synthesis using culturally resonant speakers (`anand`, `aditya`, `vijay`, `kavitha`, `rupali`, etc.). |

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

## 🚀 Running the Project Locally

### 1. Prerequisites & Environment Setup
Clone the repository and copy the environment template:
```bash
git clone https://github.com/harsh9951/heritage-storytelling-agent.git
cd heritage-storytelling-agent

cp .env.example .env
# Edit .env and paste your Sarvam AI API key:
# SARVAM_API_KEY=sk_...
```

### 2. Install Dependencies
```bash
pip install -U sarvamai aiohttp python-dotenv
```

### 3. Start the Web Server
```bash
python3 server.py
```
Open **[http://localhost:8080](http://localhost:8080)** in your browser.

### 4. Create a Public Tunnel (Optional)
To share a live public HTTPS link with anyone without deploying to a cloud host:
```bash
# Using Cloudflare Tunnel
cloudflared tunnel --url http://localhost:8080
```

---

## 📁 Directory Structure
```
heritage-storytelling-agent/
├── .env.example               # Safe environment variable template
├── .gitignore                 # Strictly ignores .env and audio outputs
├── README.md                  # Comprehensive project documentation & server links
├── server.py                  # Async aiohttp web server & API endpoints
├── heritage_agent.py          # Complete agent pipeline & interactive CLI
├── main.py                    # Minimal baseline connection test
├── static/
│   └── index.html             # Full-featured responsive web interface
└── heritage_output/
    └── .gitkeep               # Preserves audio output directory
```
