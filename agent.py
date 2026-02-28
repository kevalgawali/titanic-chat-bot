import os
import re
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO, StringIO
import base64
import sys

from huggingface_hub import InferenceClient
from dotenv import load_dotenv
load_dotenv()

# kill plt.show() so it doesn't block
plt.show = lambda *args, **kwargs: None

# load titanic data
try:
    df = sns.load_dataset('titanic')
except Exception:
    df = pd.read_csv('titanic.csv')


SYSTEM_PROMPT = f"""You are a data analyst. You have a pandas DataFrame called `df` with Titanic data.

Columns and dtypes:
{df.dtypes.to_string()}

First 3 rows:
{df.head(3).to_string()}

When the user asks a question:
1. Write Python code using pandas to answer it. The df is already loaded.
2. Use print() to output the answer.
3. If the user asks for a chart/plot/visualization, use matplotlib (plt). Call plt.figure() first. Do NOT call plt.show().
4. Keep code short and simple.

IMPORTANT: Only output Python code inside ```python ... ``` block. Nothing else."""

MODEL_ID = "Qwen/Qwen2.5-72B-Instruct"


def call_llm(system_prompt: str, user_message: str) -> str:
    """Call HuggingFace Inference API via huggingface_hub InferenceClient."""
    token = os.environ.get("HUGGINGFACEHUB_API_TOKEN", "")
    if not token:
        raise RuntimeError(
            "HUGGINGFACEHUB_API_TOKEN is not set. "
            "Add it to your .env file or Streamlit secrets."
        )
    client = InferenceClient(token=token)
    response = client.chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        model=MODEL_ID,
        temperature=0.1,
        max_tokens=1024,
    )
    return response.choices[0].message.content


def extract_code(text):
    """pull python code from the LLM response"""
    # try ```python blocks first
    matches = re.findall(r'```python\s*(.*?)```', text, re.DOTALL)
    if matches:
        return matches[0].strip()
    # try generic ``` blocks
    matches = re.findall(r'```\s*(.*?)```', text, re.DOTALL)
    if matches:
        return matches[0].strip()
    return None


def run_code(code):
    """execute code and capture printed output"""
    old_stdout = sys.stdout
    sys.stdout = captured = StringIO()
    local_vars = {"df": df, "pd": pd, "plt": plt, "sns": sns}
    try:
        exec(code, local_vars)
    finally:
        sys.stdout = old_stdout
    return captured.getvalue().strip()


def grab_plot():
    """grab current matplotlib figure as base64 png"""
    if not plt.get_fignums():
        return None
    buf = BytesIO()
    plt.gcf().savefig(buf, format='png', bbox_inches='tight', dpi=150, facecolor='white')
    buf.seek(0)
    img = base64.b64encode(buf.read()).decode()
    plt.close('all')
    return img


def ask(question: str) -> dict:
    plt.close('all')

    try:
        raw = call_llm(SYSTEM_PROMPT, question)
    except Exception as e:
        return {"answer": f"LLM call failed: {type(e).__name__}: {e}", "plot": None}

    code = extract_code(raw)
    if not code:
        # model didn't give code, just return the text
        return {"answer": raw.strip() if raw.strip() else "No response from model. Try rephrasing.", "plot": None}

    try:
        output = run_code(code)
    except Exception as e:
        return {"answer": f"Code execution error: {type(e).__name__}: {e}", "plot": None}

    plot = grab_plot()

    # if code printed something, use that as the answer
    if output:
        answer = output
    elif plot:
        answer = "Here's the chart you asked for."
    else:
        answer = "Done, but there was no output. Try rephrasing?"

    return {"answer": answer, "plot": plot}
