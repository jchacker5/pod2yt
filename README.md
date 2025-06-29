# 🎙️→📺 Notebook-LM Audio2YouTube

A Streamlit-powered tool to turn your audio clips into YouTube-ready videos—fully automated, open source, and developer-friendly.

## Overview

**Notebook-LM Audio2YouTube** lets you:

- Upload a `.wav` audio file
- Transcribe it locally using Ollama (Whisper-large-v3 by default)
- Generate 3 AI thumbnails with OpenAI DALL-E
- Pick your favorite thumbnail
- Build an MP4 video with FFmpeg
- Preview and upload to YouTube in one click

All in a clean, interactive web UI. Perfect for podcasters, educators, and anyone who wants to automate their audio-to-YouTube workflow.

---

## Features

- **Local transcription** (Ollama Whisper)
- **AI thumbnail generation** (OpenAI DALL-E)
- **MP4 video rendering** (FFmpeg)
- **YouTube upload** (YouTube Data API v3)
- **Editable transcript** before upload
- **Modern UI** (Streamlit, responsive, mobile-friendly)
- **Modular, well-documented code**

---

## Quickstart

### 1. Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com/) (for Whisper transcription)
- [FFmpeg](https://ffmpeg.org/) (install via Homebrew or your package manager)
- [OpenAI API key](https://platform.openai.com/account/api-keys)
- YouTube Data API OAuth token (see below)

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment

Create a `.env` file with your OpenAI key:

```env
OPENAI_API_KEY=sk-...
```

### 4. Run the app

```bash
streamlit run audio2yt_app.py
```

### 5. YouTube OAuth

- Follow the [YouTube Data API OAuth flow](https://developers.google.com/youtube/v3/guides/auth/client-side-web-apps) to get your token.
- Save the token JSON as `~/.config/youtube_token.json`.

---

## Usage

1. Drop a `.wav` file in the uploader.
2. Wait for transcription (editable in the UI).
3. Pick your favorite AI-generated thumbnail.
4. Render the MP4 video.
5. Preview and upload to YouTube—all from the browser!

---

## Tech Stack

- **Python**
- **Streamlit** (UI)
- **Ollama Whisper** (transcription)
- **OpenAI DALL-E** (thumbnails)
- **FFmpeg** (video rendering)
- **YouTube Data API v3** (upload)
- **Type-hinted, modular code**

---

## Contributing

We welcome contributions! 🚀

- Fork the repo and create a feature branch.
- Write clean, documented code (see existing style).
- Add tests for new features (pytest or unittest).
- Open a pull request with a clear description.

**Ideas for contribution:**

- Add support for more audio formats
- Improve error handling and UI feedback
- Add more video customization options
- Integrate with other AI models
- Write more tests and docs

If you're new to open source, this is a great place to start—just open an issue or ask for guidance!

---

## License

MIT License. See [LICENSE](LICENSE).

---

## Community & Support

- Open an issue for bugs or feature requests
- PRs and suggestions are always welcome
- Let's build something awesome together!

---

**Happy automating!**
