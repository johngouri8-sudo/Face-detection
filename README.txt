# Face Detection System

A simple face detection application built with Python, OpenCV, and Streamlit. It uses OpenCV's pre-existing Haar Cascade classifier to detect faces in images.

## Features

- Upload an image (`.jpg`, `.jpeg`, or `.png`) for face detection.
- Take a picture using the camera input.
- Draw rectangles around detected faces.
- Display the processed image and the number of faces detected.

## Project Files

- `face_streamlit.py` — Main Streamlit application.
- `haarcascade_frontalface_default.xml` — Haar Cascade classifier (the app also falls back to OpenCV's bundled copy if this file is missing).
- `requirements.txt` — Python dependencies.
- `README.txt` — This file.

## Run Locally

1. Install Python 3.9 or newer.
2. Open a terminal in the project directory.
3. (Optional) Create and activate a virtual environment.
4. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the app:

   ```bash
   streamlit run face_streamlit.py
   ```

Streamlit will display a local URL in the terminal. Open it in your browser.

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository and upload these files to the **root** of the repo:
   - `face_streamlit.py`
   - `haarcascade_frontalface_default.xml`
   - `requirements.txt`
   - `README.txt` (optional)
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **Create app** (or **New app**) and choose your repository and branch.
4. Set **Main file path** to `face_streamlit.py`.
5. (Optional) Under **Advanced settings**, choose Python 3.11 or 3.12.
6. Click **Deploy**. The first build takes a few minutes.

### Deployment notes

- `requirements.txt` uses `opencv-python-headless` instead of `opencv-python`. The regular package needs system graphics libraries (libGL) that are not available on Streamlit Cloud and causes `ImportError: libGL.so.1` errors.
- Do not list both `opencv-python` and `opencv-python-headless` in the requirements.
- The camera input needs HTTPS and browser camera permission; Streamlit Cloud provides HTTPS automatically.
- The Jupyter notebook, Flask API (`face_flask.py`) and `app.py` are not needed for deployment; you don't need to upload them.

## How It Works

1. Choose **Upload image** or **Camera**.
2. Upload an image or take a picture.
3. The application converts the image to grayscale.
4. The Haar Cascade classifier detects faces.
5. The application draws rectangles around detected faces and displays the result.

## Notes

- This project uses an existing OpenCV Haar Cascade classifier; it does not train a new face-detection model.
- Detection quality can vary with lighting, face angle, image quality, and occlusion.
