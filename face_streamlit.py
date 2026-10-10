from pathlib import Path

import cv2
import numpy as np
import streamlit as st
from PIL import Image, ImageOps

# --- Page setup (must be the first Streamlit call) -------------------------
st.set_page_config(page_title="Face Detection", page_icon="🙂")
st.title("Face Detection with Haar Cascade")
st.caption("OpenCV Haar-cascade face detection.")

# --- Cascade loading -------------------------------------------------------
# Build an absolute path from this file's location so it works no matter
# which working directory the hosting platform starts the app from.
BASE_DIR = Path(__file__).resolve().parent
LOCAL_CASCADE = BASE_DIR / "haarcascade_frontalface_default.xml"

# Limit very large images so the free hosting tier doesn't run out of memory.
MAX_SIDE = 1600


@st.cache_resource
def load_cascade():
    # 1) Prefer the XML shipped with the project.
    if LOCAL_CASCADE.exists():
        cascade = cv2.CascadeClassifier(str(LOCAL_CASCADE))
        if not cascade.empty():
            return cascade

    # 2) Fall back to the copy bundled inside the OpenCV package.
    fallback = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
    cascade = cv2.CascadeClassifier(str(fallback))
    if not cascade.empty():
        return cascade

    return None


cascade = load_cascade()

if cascade is None:
    st.error(
        "Could not load the Haar cascade file. Make sure "
        "`haarcascade_frontalface_default.xml` is in the same folder as "
        "`face_streamlit.py` in your repository."
    )
    st.stop()

# --- Input -----------------------------------------------------------------
source = st.radio("Choose input", ["Upload image", "Camera"])

file = None
if source == "Upload image":
    file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
else:
    file = st.camera_input("Take a picture")

# --- Detection -------------------------------------------------------------
if file is not None:
    try:
        image = Image.open(file)
        image = ImageOps.exif_transpose(image)  # fix rotated phone photos
        image = image.convert("RGB")

        # Downscale oversized images
        if max(image.size) > MAX_SIDE:
            image.thumbnail((MAX_SIDE, MAX_SIDE))

        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        result = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        st.image(
            result,
            caption=f"Faces detected: {len(faces)}",
            use_container_width=True,
        )
        st.success(f"Faces detected: {len(faces)}")

    except Exception as exc:
        st.error(f"Could not process this image: {exc}")
