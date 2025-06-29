# Getting Started with Notebook-LM Audio2YouTube

Welcome! This guide will help you set up and run the project for the first time.

---

## Prerequisites

- **Python 3.9+**
- **[OpenAI Whisper](https://github.com/openai/whisper)** (installed via pip, for local transcription)
- **[FFmpeg](https://ffmpeg.org/)** (install via Homebrew or your package manager)
- **OpenAI API key** ([get one here](https://platform.openai.com/account/api-keys))
- **Google API key** (from Google Cloud Console)
- **YouTube Data API OAuth token** (see below)

---

## 1. Clone the Repository

```bash
git clone https://github.com/jchacker5/pod2yt.git
cd pod2yt
```

---

## 2. Set Up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 4. Configure API Keys

Create a `.env` file in the project root:

```
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AIzaSy...
```

---

## 5. YouTube OAuth Token

- Follow the [YouTube Data API OAuth flow](https://developers.google.com/youtube/v3/guides/auth/client-side-web-apps).
- Save your token JSON as `~/.config/youtube_token.json`.

---

## 6. Run the App

```bash
streamlit run audio2yt_app.py
```

---

## 7. Using the App

1. Drop a `.wav` file in the uploader.
2. Wait for transcription (editable in the UI, powered by local Whisper).
3. Pick your favorite AI-generated thumbnail.
4. Render the MP4 video.
5. Preview and upload to YouTube—all from the browser!

---

## 8. Running Tests

```bash
PYTHONPATH=. pytest tests/ --maxfail=3 --disable-warnings -v
```

---

## Troubleshooting

- **Missing dependencies?** Run `pip install -r requirements.txt` again.
- **FFmpeg not found?** Check the path in `audio2yt_app.py` and your system install.
- **API errors?** Double-check your `.env` keys and YouTube OAuth token location.
- **Still stuck?** Open an issue on GitHub or check the README for more help.

---

## More Info

- See [README.md](README.md) for project overview and contribution guidelines.
- See [tests/README.md](tests/README.md) for test details.

---

**Happy automating!**
