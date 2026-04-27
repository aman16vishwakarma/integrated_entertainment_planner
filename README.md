# Nomad Cosmic - Agentic Entertainment Planner

**Nomad Cosmic** is an **Autonomous Agentic AI System** designed to simulate an entire Hollywood Writers' Room and Production Planning team. It utilizes **Retrieval-Augmented Generation (RAG)** to maintain narrative consistency and a **Multi-Agent Control Loop** to evaluate, rewrite, and plan the logistics of entertainment assets.

## 🚀 Features

- **Multi-Agent Architecture**: 
  - **Writer Agent**: Generates creative content.
  - **Critic Agent**: Reviews generated content for quality, pacing, and formatting, forcing autonomous rewrites if standards aren't met.
  - **Planner Agent**: Analyzes the final approved script and extracts actionable production logistics (Locations, Props, Characters, and Budget).
- **Narrative Memory**: Uses **FAISS** Vector Database and **Sentence-Transformers** to ensure the AI remembers plot points and character arcs across pipeline stages.
- **Resilient Logic**: Implements an Exponential Backoff Middleware to handle API rate limits and network latency gracefully.
- **Premium Cinematic UI**: A sleek, custom-designed Streamlit dashboard utilizing advanced CSS (Grid backgrounds, glassmorphism, and gradient typography).

## 🛠 Tech Stack

- **Core**: Python 3.9+
- **LLM**: Google Gemini 2.5 Flash
- **Agentic Memory**: FAISS (Vector DB)
- **Embeddings**: Sentence-Transformers (`all-MiniLM-L6-v2`)
- **Frontend / Orchestration**: Streamlit

## ⚙️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/aman16vishwakarma/integrated_entertainment_planner.git
   cd integrated_entertainment_planner
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables**:
   Create a `.env` file in the root directory and add your [Google Gemini API Key](https://aistudio.google.com/):
   ```text
   GEMINI_API_KEY=your_api_key_here
   ```

## 🚀 How to Run

Launch the application using Streamlit:
```bash
streamlit run app.py
```

## 🏗 Architecture & Agentic Workflow

The project follows a recursive multi-agent workflow:
1. **Initial Seed**: User provides a topic, genre, and tone.
2. **Pre-Production**: Concept, Logline, Pitch, Outline, and Characters are generated.
3. **The Writers' Room Loop**:
   - `Writer` drafts the script scene.
   - `Critic` evaluates it.
   - If rejected, `Writer` rewrites (bounded to 2 iterations to prevent infinite loops).
4. **Logistics**: `Planner` extracts production requirements.
5. **Output**: Delivered to the cinematic Streamlit UI.

---
*Built for AWS EC2 DevOps & Agentic AI Demonstrations.*