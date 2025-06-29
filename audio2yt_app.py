#!/usr/bin/env python3
# --------------------------------------------------------------
# Dre's Notebook-LM → YouTube Streamlit interface
# --------------------------------------------------------------
# - Drag in / browse to a .wav
# - Transcribes locally through Ollama (Whisper-large-v3 default)
# - Generates 3 thumbnails with OpenAI Images
# - Lets you pick the one you like
# - Builds an MP4 with FFmpeg and shows a preview
# - Single-click upload to YouTube (Data API v3)
# --------------------------------------------------------------

"""
Dre's Notebook-LM → YouTube Streamlit interface
--------------------------------------------------------------
This app allows users to:
- Upload a .wav audio file
- Transcribe it locally using Ollama (Whisper-large-v3 by default)
- Generate 3 thumbnails using OpenAI DALL-E
- Select a preferred thumbnail
- Build an MP4 video with FFmpeg
- Preview and upload the video to YouTube (Data API v3)

Environment variables required:
- OPENAI_API_KEY: for OpenAI API access
- FFmpeg must be installed and path set in FFMPEG_BIN
- YouTube OAuth token must be available at ~/.config/youtube_token.json

This code is designed to be modular and easy to extend or test.
"""

import os
import subprocess
import tempfile
import time
from pathlib import Path
import streamlit as st
import openai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ---------- CONFIG ---------------------------------------------------------
# Model and tool configuration
OLLAMA_MODEL = (
    "ZimaBlueAI/whisper-large-v3"
)  # Whisper model for transcription
FFMPEG_BIN = "/usr/local/bin/ffmpeg"  # Path to FFmpeg binary
YT_TOKEN_FILE = Path.home() / ".config/youtube_token.json"  # YouTube OAuth token
TMP_ROOT = (
    Path(tempfile.gettempdir())
    / "dre_audio2yt"
)  # Temporary directory for file storage
TMP_ROOT.mkdir(exist_ok=True)

# Set OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")  # must be set before launch
if not openai.api_key:
    st.error("OPENAI_API_KEY not set in your environment")
    st.stop()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ---------- HELPERS -----------------------------------------------------------


def say(msg: str) -> None:
    """
    Display an info message in the Streamlit UI.
    Args:
        msg (str): The message to display.
    """
    st.info(msg, icon="💡")


def ensure_ffmpeg() -> None:
    """
    Ensure FFmpeg binary exists at the configured path.
    Stops the app with an error if not found.
    """
    if not Path(FFMPEG_BIN).exists():
        st.error(
            f"FFmpeg not found at {FFMPEG_BIN}. Install via Homebrew or "
            "edit FFMPEG_BIN."
        )
        st.stop()


@st.cache_data(show_spinner="Transcribing …")
def transcribe_with_ollama(wav_path: Path) -> str:
    """
    Transcribe audio using the Ollama Whisper model.
    Args:
        wav_path (Path): Path to the .wav file to transcribe.
    Returns:
        str: The transcribed text.
    Raises:
        RuntimeError: If the transcription process fails.
    """
    cmd = [
        "ollama",
        "run",
        OLLAMA_MODEL,
        "-f",
        str(wav_path),
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()


@st.cache_data(show_spinner="Generating thumbnails …")
def generate_thumbnails(prompt: str, count: int = 3, size: str = "1024x1024"):
    """
    Generate thumbnails using OpenAI DALL-E API.
    Args:
        prompt (str): The prompt to use for image generation.
        count (int): Number of images to generate.
        size (str): Image size (e.g., '1024x1024').
    Returns:
        list[Path]: List of paths to generated images.
    """
    rsp = openai.images.generate(
        prompt=prompt,
        model="dall-e-3",
        n=count,
        size=size,
        response_format="b64_json",
    )
    imgs = []
    for idx, d in enumerate(rsp.data):
        # openai.util.tofile is not a public API; use base64 decode instead
        import base64
        img_bytes = base64.b64decode(d.b64_json)
        img_path = TMP_ROOT / f"thumb_{int(time.time())}_{idx}.png"
        img_path.write_bytes(img_bytes)
        imgs.append(img_path)
    return imgs


def build_video(audio: Path, image: Path, out_mp4: Path) -> None:
    """
    Build an MP4 video from audio and image using FFmpeg.
    Args:
        audio (Path): Path to the audio file.
        image (Path): Path to the image file.
        out_mp4 (Path): Output path for the MP4 video.
    Raises:
        subprocess.CalledProcessError: If FFmpeg fails.
    """
    cmd = [
        FFMPEG_BIN,
        "-y",
        "-loop",
        "1",
        "-i",
        str(image),
        "-i",
        str(audio),
        "-c:v",
        "libx264",
        "-tune",
        "stillimage",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-pix_fmt",
        "yuv420p",
        "-shortest",
        str(out_mp4),
    ]
    subprocess.run(cmd, check=True)


def youtube_uploader(mp4: Path, title: str, desc: str) -> str:
    """
    Upload a video to YouTube using the Data API v3.
    Args:
        mp4 (Path): Path to the MP4 video file.
        title (str): Video title.
        desc (str): Video description.
    Returns:
        str: The YouTube video ID.
    Raises:
        RuntimeError: If the OAuth token is missing.
    """
    if not YT_TOKEN_FILE.exists():
        raise RuntimeError(
            "YouTube OAuth token JSON not found—run the OAuth flow first."
        )
    creds = Credentials.from_authorized_user_file(YT_TOKEN_FILE)
    yt = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": title,
            "description": desc,
            "tags": ["audio2yt", "ollama", "Whisper"],
            "categoryId": "28",
        },
        "status": {"privacyStatus": "public"},
    }
    request = yt.videos().insert(
        part="snippet,status", body=body, media_body=str(mp4)
    )
    return request.execute()["id"]

# ---------- UI --------------------------------------------------------------


st.set_page_config(page_title="Notebook-LM to YouTube", layout="centered")
st.title("🎙️ → 📺  Notebook-LM Clip Uploader")

# Ensure FFmpeg is available before proceeding
ensure_ffmpeg()

# File upload UI
uploaded = st.file_uploader("Drop a .wav clip here", type=["wav"])
if uploaded:
    with st.spinner("Saving file …"):
        orig_path = TMP_ROOT / uploaded.name
        orig_path.write_bytes(uploaded.getbuffer())
    st.success(f"Saved {orig_path.name}")

    # Step 1  —  Transcription
    try:
        transcript = transcribe_with_ollama(orig_path)
        st.text_area(
            "Transcript (editable before upload)", value=transcript, key="tx"
        )
    except Exception as e:
        st.error(f"Transcription failed: {e}")
        st.stop()

    # Step 2  —  Thumbnails
    thumbs = generate_thumbnails(prompt=transcript[:200])
    cols = st.columns(len(thumbs))
    chosen_idx = 0
    for i, (col, img_path) in enumerate(zip(cols, thumbs)):
        with col:
            if st.radio(label="", options=["Use this"], key=f"thumb_{i}"):
                chosen_idx = i
            st.image(str(img_path), use_column_width=True)
    chosen_thumb = thumbs[chosen_idx]

    # Step 3  —  Build video
    if st.button("🔧 Render MP4"):
        mp4_path = TMP_ROOT / f"{orig_path.stem}.mp4"
        try:
            with st.status("Rendering video …", expanded=True) as status:
                build_video(orig_path, chosen_thumb, mp4_path)
                status.update(label="Video rendered ✔", state="complete")
        except Exception as e:
            st.error(f"FFmpeg error: {e}")
            st.stop()

        st.video(str(mp4_path))

        # Step 4  —  Upload
        if st.button("⬆️ Upload to YouTube"):
            try:
                with st.spinner("Uploading … this can take a minute"):
                    vid_id = youtube_uploader(
                        mp4_path,
                        title=orig_path.stem.replace('_', ' '),
                        desc=st.session_state.tx,
                    )
                st.success(f"Uploaded! https://youtu.be/{vid_id}")
            except Exception as e:
                st.error(f"Upload failed: {e}")
