import streamlit as st
import time
import os
from dotenv import load_dotenv
from engine.pipeline import ContentPipeline

# Load environment variables early
load_dotenv()

# Page Config
st.set_page_config(
    page_title="Nomad Cosmic | Entertainment GenAI",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Courier+Prime&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    /* Unique Blueprint Background */
    .stApp {
        background-color: #0B0C10;
        background-image: 
            linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 40px 40px;
    }
    
    /* Sleek Sidebar */
    div[data-testid="stSidebar"] {
        background-color: #111218 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 5px 0 20px rgba(0,0,0,0.5);
    }
    
    /* Elegant Glowing Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #e63946, #ff7b7b);
        color: white;
        border: 1px solid rgba(255, 123, 123, 0.3);
        box-shadow: 0 4px 15px rgba(230, 57, 70, 0.2);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        border-radius: 8px;
        height: 3.5em;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(230, 57, 70, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.5);
    }
    
    /* Cinematic Inputs */
    .stTextArea>div>div>textarea, .stTextInput>div>div>input {
        background-color: rgba(0, 0, 0, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #f1faee !important;
        border-radius: 8px !important;
        font-size: 1.05rem !important;
        padding: 10px !important;
    }
    .stTextArea>div>div>textarea:focus, .stTextInput>div>div>input:focus {
        border-color: #e63946 !important;
        box-shadow: 0 0 15px rgba(230, 57, 70, 0.3) !important;
    }
    
    /* Floating Output Cards */
    .output-section {
        background: rgba(26, 28, 36, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 30px;
        border-radius: 12px;
        border-left: 6px solid #e63946;
        margin-bottom: 30px;
        color: #e0e0e0;
        line-height: 1.7;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        font-size: 1.1rem;
    }
    
    /* Realistic Screenplay Format */
    .script-text {
        font-family: 'Courier Prime', 'Courier New', Courier, monospace;
        background-color: #fdfdfd;
        color: #111;
        padding: 60px 80px;
        border-radius: 4px;
        white-space: pre-wrap;
        box-shadow: 10px 10px 25px rgba(0,0,0,0.6);
        max-width: 850px;
        margin: 0 auto 30px auto;
        line-height: 1.4;
        font-size: 1.05rem;
    }
    
    /* Gradient Headers */
    h1, h2, h3 {
        background: -webkit-linear-gradient(45deg, #e63946, #ffb3b3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }
    
    .stExpander {
        border: none !important;
        background-color: transparent !important;
    }
    div[data-testid="stExpanderDetails"] {
        border-left: 2px solid rgba(255,255,255,0.1);
        padding-left: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'pipeline' not in st.session_state:
    st.session_state.pipeline = None
if 'outputs' not in st.session_state:
    st.session_state.outputs = {}

def init_pipeline():
    try:
        st.session_state.pipeline = ContentPipeline()
        return True
    except Exception as e:
        st.error(f"Initialization Failed: {e}")
        return False

# Attempt auto-init if API key is present
api_key = os.getenv("GEMINI_API_KEY")
if not st.session_state.pipeline and api_key and api_key != "your_gemini_api_key_here":
    init_pipeline()

# Sidebar - Controls
with st.sidebar:
    st.title("🎬 Nomad Cosmic")
    st.subheader("Design Your Masterpiece")

    st.markdown("# Process Status")
    status_placeholder = st.empty()
    if st.session_state.pipeline:
        st.success("System Ready (API Connected)")
    else:
        st.warning("Waiting for API Key configuration")

    st.divider()
    
    genre = st.selectbox("Select Genre", 
                        ["Sci-Fi", "Thriller", "Drama", "Comedy", "Horror", "Fantasy", "Action"])
    
    tone = st.selectbox("Select Tone", 
                       ["Serious", "Emotional", "Dark", "Humorous", "Suspenseful", "Poetic"])
    
    output_type = st.selectbox("Pipeline Target", 
                              ["Full Pipeline", "Pitch Only", "Script Scene Only", "Logline & Concept"])
    
    st.divider()
    st.info("Ensuring industry-standard screenplay formatting and narrative logic.")

# Main UI
st.title("Entertainment Content Generator")
st.markdown("---")


idea_input = st.text_area("Enter your seed idea or topic:", 
                         placeholder="A story about a time-traveling historian who accidentally deletes their own existence...",
                         height=150)
    
generate_btn = st.button("GENERATE CONTENT")


    

# Generation Logic
if generate_btn:
    if not idea_input:
        st.warning("Please enter an idea first.")
    else:
        if not st.session_state.pipeline:
            init_pipeline()
            
        if st.session_state.pipeline:
            with st.spinner("Brainstorming with GenAI..."):
                try:
                    if output_type == "Full Pipeline":
                        st.session_state.outputs = st.session_state.pipeline.run_full_pipeline(idea_input, genre, tone)
                    else:
                        # Specific stage logic
                        if "Pitch" in output_type:
                            concept = st.session_state.pipeline.run_stage('concept', {'idea': idea_input, 'genre': genre, 'tone': tone})
                            logline = st.session_state.pipeline.run_stage('logline', {'concept': concept})
                            pitch = st.session_state.pipeline.run_stage('pitch', {'concept': concept, 'logline': logline})
                            st.session_state.outputs = {'concept': concept, 'logline': logline, 'pitch': pitch}
                        elif "Scene" in output_type:
                            concept = st.session_state.pipeline.run_stage('concept', {'idea': idea_input, 'genre': genre, 'tone': tone})
                            outline = st.session_state.pipeline.run_stage('outline', {'pitch': concept})
                            chars = st.session_state.pipeline.run_stage('characters', {'outline': outline})
                            scene = st.session_state.pipeline.run_agentic_scene(outline, chars)
                            planner = st.session_state.pipeline.run_planner(scene)
                            st.session_state.outputs = {'scene': scene, 'planner': planner}
                        else:
                            concept = st.session_state.pipeline.run_stage('concept', {'idea': idea_input, 'genre': genre, 'tone': tone})
                            logline = st.session_state.pipeline.run_stage('logline', {'concept': concept})
                            st.session_state.outputs = {'concept': concept, 'logline': logline}
                    
                    if not st.session_state.outputs or all(v == "" for v in st.session_state.outputs.values()):
                         st.error("Model returned empty results. Please check your API key or idea input.")
                    else:
                         st.success("Generation Complete!")
                         st.rerun() # Ensure the UI updates immediately
                except Exception as e:
                    st.error(f"Generation Error: {str(e)}")

# Results Display
if st.session_state.outputs:
    st.markdown("---")
    
    for stage, content in st.session_state.outputs.items():
        with st.expander(f"{stage.upper()}", expanded=(stage in ['pitch', 'scene', 'planner'])):
            if stage == 'scene':
                st.markdown(f'<div class="script-text">{content}</div>', unsafe_allow_html=True)
            elif stage == 'planner':
                st.markdown(f'<div class="output-section" style="border-left: 5px solid #4CAF50; background-color: #1e241e;">{content}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="output-section">{content}</div>', unsafe_allow_html=True)
            
            # Refine Button
            if stage not in ['planner', 'critic']:
                if st.button(f"Regenerate {stage.capitalize()}", key=f"regen_{stage}"):
                    with st.spinner(f"Rewriting {stage}..."):
                        new_output = st.session_state.pipeline.run_stage(stage, {'idea': idea_input, 'genre': genre, 'tone': tone, 'concept': st.session_state.outputs.get('concept', ''), 'logline': st.session_state.outputs.get('logline', ''), 'pitch': st.session_state.outputs.get('pitch', ''), 'outline': st.session_state.outputs.get('outline', ''), 'characters': st.session_state.outputs.get('characters', '')})
                        st.session_state.outputs[stage] = new_output
                        st.rerun()

    # Memory Viewer & Reset
    with st.sidebar:
        st.divider()
        if st.checkbox("Show Memory (Vector DB Contents)"):
            if st.session_state.pipeline:
                st.write(st.session_state.pipeline.db.get_all_history())
            else:
                st.write("Memory is empty.")
        
        if st.button("Reset Application"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
