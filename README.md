# 🏙️ UrbanNest · AI Real Estate & Apartment Concierge

An agentic application built on Google Cloud Agent Platform, ADK, and Gemini that helps apartment hunters discover, evaluate, and budget for urban housing.

---

## 🌟 Features

- 🧠 **Cross-Session Memory**: Powered by Vertex AI Agent Platform Memory Bank — retains your budget limits, pet policies (breed/weight), target neighborhoods, and amenities across conversations.
- 🗄️ **Structured Apartment Catalog**: Real-time property catalog in Google Cloud Firestore with unit specs, verified amenities, pet rules, and pricing.
- 🖼️ **Public Image Storage**: Google Cloud Storage bucket integration for media assets and architectural photos.
- 🎨 **Visual Concept Generation**: On-demand interior staging and exterior architectural visualizations generated with `gemini-3.1-flash-lite-image`.
- 🧪 **Code Execution Sandbox**: Safe Python sandbox powered by Vertex AI Agent Engine Code Sandbox for calculating monthly occupancy costs, utility estimates, and income affordability rules.
- 🗺️ **Maps Integration**: Location coordinates and nearby amenity lookups powered by Google Maps Geocoding & Places (New) APIs.
- 🪟 **Agent-to-User Interface (A2UI)**: Rich UI cards with spec badges, photos, and comparison breakdowns.
- 🌐 **Modern Chat Frontend**: Fast, responsive FastAPI proxy communicating over the A2A protocol with markdown parsing and quick-prompt chips.

---

## 📁 Project Structure

```text
urbannest/
├── app/
│   ├── agent.py                 # Core ADK agent with memory, prompt, and tool registration
│   ├── fast_api_app.py          # Backend server
│   └── app_utils/
│       ├── tools.py             # Firestore query, tour booking, Maps, Image gen & Sandbox tools
│       ├── memory.py            # Vertex AI Memory Bank integration
│       └── a2ui_utils.py        # A2UI rich card generation callback
├── frontend/
│   ├── main.py                  # FastAPI A2A proxy server
│   ├── requirements.txt         # Frontend dependencies
│   └── static/
│       └── index.html           # Modern UrbanNest chat UI with A2UI support
├── tests/                       # Unit and integration test suite
├── project_brief.md             # Project brief and design requirements
├── agents-cli-manifest.yaml     # agents-cli deployment manifest
└── pyproject.toml               # Project dependencies and configuration
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.11+
- `uv` package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Authenticated Google Cloud SDK:
  ```bash
  gcloud auth login
  gcloud auth application-default login
  ```

### 2. Install Dependencies
```bash
uv sync
```

### 3. Run the Agent Locally (ADK Web)
```bash
uv run adk web . --port 8080 --reload_agents
```

### 4. Run the Web Frontend
```bash
cd frontend
pip install -r requirements.txt
export AGENT_ENGINE_RESOURCE_NAME="<your-agent-runtime-id>"
export AGENT_DIRECTORY="app"
python main.py
```
Open [http://localhost:8080](http://localhost:8080) to interact with the UrbanNest UI.

---

## 🧪 Testing

Run unit and integration tests:
```bash
uv run pytest
```
