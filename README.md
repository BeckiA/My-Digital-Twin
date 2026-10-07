# Digital Twin - Career AI Assistant

This folder contains the **Digital Twin** project from Lab 4. The Digital Twin is an interactive conversational AI that represents you on your personal website or portfolio, answering questions about your career, background, skills, and experience, while sending real-time notifications to your phone via Pushover.

---

## 📁 Project Structure

| File / Folder | Description |
|---|---|
| [`4_lab4.ipynb`](4_lab4.ipynb) | Interactive Jupyter Notebook exploring the step-by-step creation of the digital twin, tool calling, and Pushover alerts. |
| [`app.py`](app.py) | Main modular script that launches the Gradio web interface and manages the OpenAI chat loop. |
| [`context.py`](context.py) | Extracts information from `linkedin.pdf` and `summary.txt` to construct the twin's dynamic system prompt. |
| [`tools.py`](tools.py) | OpenAI function/tool definitions and execution handlers (`record_user_details`, `record_unknown_question`) with Pushover push alerts. |
| [`styles.py`](styles.py) | Custom CSS, JavaScript tweaks, and starter prompt buttons for the Gradio UI. |
| [`summary.txt`](summary.txt) | Text summary of your personal background, bio, and key accomplishments. |
| [`linkedin.pdf`](linkedin.pdf) | Your LinkedIn profile export used by the twin as reference knowledge. |
| [`requirements.txt`](requirements.txt) | Python dependencies required to run the application. |
| [`twin/`](twin/) | Local resource mirror providing path compatibility for running `4_lab4.ipynb`. |

---

## 🚀 Features

- **Personalized Knowledge**: Grounded in your LinkedIn profile export (`linkedin.pdf`) and executive summary (`summary.txt`).
- **Autonomous Tool Calling**:
  - `record_user_details`: Collects visitor contact information (name, email, notes) and sends push notifications to your phone.
  - `record_unknown_question`: Logs questions the AI twin could not answer so you can follow up or update your profile.
- **Pushover Notifications**: Immediate push notifications sent directly to your phone when visitors engage or ask unknown questions.
- **Modern Web Interface**: Responsive Gradio chat interface with custom styling and sample conversation starters.

---

## 🛠️ Prerequisites & Configuration

### 1. Environment Variables

Create or ensure a `.env` file exists at the root of the project with the following keys:

```env
OPENAI_API_KEY=your_openai_api_key
PUSHOVER_USER=your_pushover_user_key
PUSHOVER_TOKEN=your_pushover_app_token
```

> **Note**: Free Pushover credentials can be obtained at [pushover.net](https://pushover.net).

### 2. Customize Your Twin

Before running or deploying, update the profile assets with your own information:
1. Replace [`linkedin.pdf`](linkedin.pdf) with your downloaded LinkedIn profile (from LinkedIn profile -> *More* -> *Save to PDF*).
2. Edit [`summary.txt`](summary.txt) with your concise personal summary and key highlights.

---

## 💻 Running Locally

### Using `uv` (Recommended)

```bash
# Navigate to this folder
cd digital_twin

# Run the Gradio app
uv run app.py
```

### Using standard `python` & `pip`

```bash
# Navigate to this folder
cd digital_twin

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Once started, open the printed local URL (e.g. `http://127.0.0.1:7860`) in your browser.

### Running via Jupyter Notebook

Open and run [`4_lab4.ipynb`](4_lab4.ipynb) in your preferred Jupyter environment (Cursor / VS Code or JupyterLab).

---

## 🌐 Deployment (Render)

Render can host the twin for free as a Web Service:

1. Create a dedicated GitHub repository for your digital twin.
2. Push `app.py`, `context.py`, `tools.py`, `styles.py`, `requirements.txt`, `summary.txt`, and `linkedin.pdf` into that repository.
3. In [Render](https://render.com), create a new **Web Service** connected to your repository.
4. Set:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
5. Under **Environment Variables**, add:
   - `OPENAI_API_KEY`
   - `PUSHOVER_USER`
   - `PUSHOVER_TOKEN`
   - `GRADIO_SERVER_NAME`: `0.0.0.0`
   - `GRADIO_SERVER_PORT`: `10000`
