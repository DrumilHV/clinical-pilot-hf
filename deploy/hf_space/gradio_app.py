"""Hugging Face Spaces entrypoint.

Renamed from app.py → gradio_app.py to avoid the name collision where Python
mistakes the script file itself for the `app` package when doing
`import app.ui.*`.

Set HF_SPACE_BACKEND_URL via Spaces Secrets to point at the deployed FastAPI.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Repo root = parents[2] of deploy/hf_space/gradio_app.py
ROOT = Path(__file__).resolve().parents[2]

# Remove the script's own directory from sys.path so that
# `import app` resolves to the repo's app/ package, not this file.
script_dir = str(Path(__file__).resolve().parent)
if script_dir in sys.path:
    sys.path.remove(script_dir)

# Insert repo root so `import app.ui.*` works
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import gradio as gr  # noqa: E402

from app.ui.doctor_tab import build_tab as build_doctor_tab  # noqa: E402
from app.ui.nurse_admin_tab import build_tab as build_nurse_admin_tab  # noqa: E402
from app.ui.patient_tab import build_tab as build_patient_tab  # noqa: E402

BACKEND_URL = os.getenv("HF_SPACE_BACKEND_URL", "http://localhost:8000")


def build_app() -> gr.Blocks:
    with gr.Blocks(title="CliniqAI") as demo:
        gr.Markdown(
            f"# 🪶 CliniqAI\nClinical operations AI for Indian hospitals. "
            f"Backend: `{BACKEND_URL}`"
        )
        with gr.Tabs():
            with gr.Tab("Doctor"):
                build_doctor_tab()
            with gr.Tab("Patient"):
                build_patient_tab()
            with gr.Tab("Nurse & Admin"):
                build_nurse_admin_tab()
    return demo


if __name__ == "__main__":
    build_app().launch(
        server_name="0.0.0.0",
        server_port=int(os.getenv("GRADIO_SERVER_PORT", "7860")),
        theme=gr.themes.Soft(),
        share=False,
    )
