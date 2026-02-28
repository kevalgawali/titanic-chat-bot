# Titanic Dataset Chat Agent

Chat with the Titanic dataset using natural language. Ask questions, get answers and charts.

Built as a single Streamlit application with local LLM calls.

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

Start the Streamlit interface only:

```bash
streamlit run streamlit_app.py
```

All logic (including `ask()` calls and model inference) happen inside the same process. There is no separate backend.


## Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file path** to `streamlit_app.py`
5. In **Advanced settings > Secrets**, add:
   ```
   HUGGINGFACEHUB_API_TOKEN = "hf_your-token-here"
   ```
6. Deploy

Since the application is self‑contained, there is no backend dependency—Streamlit Cloud will run the chat UI directly.


## Project Structure

```
assignment1/
├── agent.py           # data/LLM logic (query the dataframe)
├── streamlit_app.py   # single Streamlit UI
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
