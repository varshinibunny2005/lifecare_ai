# ❤️ LifeCare AI

LifeCare AI is a Streamlit-based medical assistant that analyzes user-described symptoms using a large language model (Llama 3.3 70B via the Groq API) and returns a structured summary, possible causes, and recommended next steps.

> ⚠️ **Disclaimer:** This application is for informational purposes only and is **not** a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider.

---

## Features

- **Guided multi-page flow:** Home → User Verification → Symptom Entry → AI Analysis
- **Structured AI output:** Symptom summary, possible causes, and recommended next steps
- **File upload support:** Upload a PNG/JPG image or a PDF report with an in-app preview (first page preview for PDFs)
- **Personalized prompts:** Name, age, and gender are included in the analysis request
- **Clean custom UI:** Styled buttons, centered layout, and a built-in medical disclaimer

---

## Tech Stack

| Component | Technology |
|---|---|
| Frontend / App framework | [Streamlit](https://streamlit.io/) |
| LLM provider | [Groq API](https://console.groq.com/) |
| Model | `llama-3.3-70b-versatile` |
| PDF preview | PyMuPDF (`fitz`) |
| Image handling | Pillow |
| Config | python-dotenv |
| HTTP client | requests |

---

## Project Structure

```
LifeCare-AI/
├── app.py              # Main Streamlit application
├── logo.png            # Logo shown on the home page (required)
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (not committed)
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd LifeCare-AI
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

Create a `requirements.txt` with the following:

```
streamlit
requests
python-dotenv
Pillow
PyMuPDF
```

Then run:

```bash
pip install -r requirements.txt
```

### 4. Get a Groq API key

Create a free API key at [console.groq.com](https://console.groq.com/keys).

### 5. Configure environment variables

Create a `.env` file in the project root:

```
groq_api=your_groq_api_key_here
```

> The variable name must be exactly `groq_api` (lowercase), as read by `os.getenv("groq_api")` in the code.

### 6. Add the logo

Place your `logo.png` in the project root (the home page loads it with `st.image("logo.png")`).

### 7. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## How It Works

1. **Home:** Overview of the app with a medical disclaimer and a **Get Started** button.
2. **User Verification:** Enter full name, age (> 0), and gender.
3. **Symptoms:** Describe symptoms in the text box and optionally upload an image or PDF report.
4. **Analyze:** The app builds a prompt from the user details and symptoms, sends it to the Groq chat completions endpoint, and displays the structured response.

### AI request settings

| Parameter | Value |
|---|---|
| Endpoint | `https://api.groq.com/openai/v1/chat/completions` |
| Model | `llama-3.3-70b-versatile` |
| Temperature | `0.7` |
| Max tokens | `1024` |

---

## Known Limitations

- **Uploaded files are preview-only.** Images and PDFs are displayed in the UI but their contents are **not** sent to the model; the analysis is based on the text symptoms only.
- Allowed upload types are `png`, `jpg`, and `pdf` (`.jpeg` is not currently included).
- The model can produce inaccurate or incomplete medical information; results must not be treated as a diagnosis.
- No user authentication or data persistence; state lives only in the Streamlit session.

---

## Security & Privacy Notes

- Never commit your `.env` file. Add it to `.gitignore`:
  ```
  .env
  venv/
  __pycache__/
  ```
- Symptom text and user details are sent to a third-party API (Groq). Do not use real patient-identifiable data in demos.

---

## Possible Improvements

- Send image/PDF content to a vision-capable or document-parsing pipeline for analysis
- Add `.jpeg` to the accepted upload types
- Download the analysis as a PDF report
- Add multilingual support
- Add an emergency-symptom warning (e.g., chest pain, breathing difficulty) that advises seeking immediate care

---
