# CheckMakeGPT 🧠

CheckMakeGPT is a Streamlit-based tool that allows users to evaluate, optimize, and manage CustomGPT personas and prompt sets using OpenAI's GPT models.

---

## 🚀 Features

- Persona workshop with GPT-4 optimization and revision
- Custom prompt set creation and management
- Evaluation criteria builder (with weights and rubric)
- Automated evaluation pipeline using CustomGPT + OpenAI
- API key inputs secured per session (no persistent storage of secrets)

---

## 📁 Project Structure

```
CheckMakeGPT/
├── config/                 # Presets and criteria files
├── prompts/                # Custom prompt sets
├── personas/               # Saved agent personas
├── outputs/                # Evaluation result files
├── core/
│   ├── tester.py           # Handles CustomGPT interactions
│   └── openai_evaluator.py# Handles OpenAI evaluation scoring
├── dashboard.py            # Main Streamlit app
├── .gitignore              # Excludes secrets and local files
├── README.md               # You're reading it!
```

---

## 🔐 API Key Security

Users enter their API keys via the **Connections** tab. Keys are stored securely in session state and never saved to disk.

Add the following to `.gitignore` (already included):

```
.env
config/*.yaml
user_keys.json
```

---

## 🧪 Local Usage

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app**:
   ```bash
   streamlit run dashboard.py
   ```

3. **Enter your OpenAI and CustomGPT keys** in the "🔐 Connections" tab to start.

---

## 🌐 Deployment

This app is Streamlit Cloud-ready. Just connect this repo and make sure `.streamlit/secrets.toml` is empty or safely configured if you pre-fill default keys.

---

## ✨ Status

✅ Fully refactored to support `openai>=1.0.0`
✅ No secrets committed
✅ Safe for team collaboration

---

## 🤝 Author

**David Peters** – Ph.D. candidate in Media Psychology, VR researcher, and creative tech developer.
