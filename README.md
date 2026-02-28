# Titanic Dataset Chat Agent

Chat with the Titanic dataset using natural language. Ask questions, get answers and charts.

Built with FastAPI + LangChain + Streamlit.

## Setup

```bash
# clone and cd into the project
cd assignment1

# create virtual env (optional but recommended)
python -m venv venv
venv\Scripts\activate   # windows
# source venv/bin/activate  # mac/linux

# install deps
pip install -r requirements.txt
```

Create a `.env` file (see `.env.example`):
```
HUGGINGFACEHUB_API_TOKEN=hf_your-token-here
```

Get a free token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).

## Running Locally

You need two terminals:

**Terminal 1 — Backend (FastAPI):**
```bash
uvicorn main:app --reload
```
Runs on http://localhost:8000

**Terminal 2 — Frontend (Streamlit):**
```bash
streamlit run app.py
```
Opens on http://localhost:8501

The Streamlit app auto-detects if the backend is running. If it can't reach FastAPI, it runs the agent directly (no backend needed).

## Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file path** to `app.py`
5. In **Advanced settings > Secrets**, add:
   ```
   HUGGINGFACEHUB_API_TOKEN = "hf_your-token-here"
   ```
6. Deploy

On Streamlit Cloud there's no FastAPI server, so the app automatically falls back to running the LangChain agent directly. Everything works the same.

## Project Structure

```
assignment1/
├── agent.py           # LangChain pandas agent logic
├── main.py            # FastAPI backend
├── app.py             # Streamlit frontend
├── requirements.txt
├── .env.example
└── README.md
```

## What You Can Ask

- "How many passengers survived?"
- "Show survival rate by gender as a bar chart"
- "What's the average age of first class passengers?"
- "Plot the fare distribution"
- "Compare survival rates across passenger classes"

The agent uses Mixtral-8x7B (free via HuggingFace Inference API) + LangChain's pandas agent to analyze the dataframe and optionally generate matplotlib charts.
