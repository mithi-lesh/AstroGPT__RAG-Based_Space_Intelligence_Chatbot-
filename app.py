import streamlit as st
import tempfile
import os
import rag_engine

st.set_page_config(page_title="Astro-GPT Expert", page_icon="🌌", layout="wide")

# Custom CSS for Premium Space-Themed UI
page_bg_css = """
<style>
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 50% 100%, #171b2d 0%, #070912 100%);
    color: #e2e8f0;
}
[data-testid="stHeader"] {
    background: transparent !important;
}
[data-testid="stSidebar"] {
    background-color: rgba(15, 23, 42, 0.4) !important;
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255,255,255,0.05);
}
h1 {
    font-family: 'Inter', sans-serif;
    background: -webkit-linear-gradient(45deg, #a855f7, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    margin-bottom: 0px !important;
}
.subtitle {
    font-size: 1.1rem;
    color: #94a3b8;
    margin-bottom: 2rem;
    font-weight: 300;
}
.stChatMessage {
    background-color: rgba(30, 41, 59, 0.6);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.05);
    backdrop-filter: blur(5px);
    margin-bottom: 10px;
}
.stChatInputContainer {
    background-color: transparent !important;
}
</style>
"""
st.markdown(page_bg_css, unsafe_allow_html=True)

col1, col2 = st.columns([1, 4])
with col1:
    image_path = "stitch.jpg"
    if os.path.exists(image_path):
        st.image(image_path, width=120)
    else:
        st.markdown("### Astro-GPT & Stitch 🌌👽")
        st.markdown("<small>Tip: add `stitch.jpg` to the app directory or update the path.</small>", unsafe_allow_html=True)

with col2:
    st.title("Astro-GPT & Stitch 🌌👽")
    st.markdown('<p class="subtitle">Your Expert Small Language Model & Chief Observatory Assistant</p>', unsafe_allow_html=True)

# Sidebar for config and upload
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Google Gemini API Key", type="password", placeholder="AIzaSy...")
    st.markdown("<small>[Get your free Gemini API Key here](https://aistudio.google.com/app/apikey)</small>", unsafe_allow_html=True)
    st.divider()
    
    st.header("🗄️ Ingest Knowledge")
    st.markdown("<small>Drop your astronomical PDFs (Textbooks, ArXiv papers, observation logs) to train Astro-GPT's memory.</small>", unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)
    
    if st.button("Process Documents") and uploaded_files:
        progress_bar = st.progress(0)
        total_chunks = 0
        
        for i, uploaded_file in enumerate(uploaded_files):
            with st.spinner(f"Ingesting {uploaded_file.name}..."):
                # Save file temporarily to pass to the engine
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                
                try:
                    num_chunks = rag_engine.process_document(tmp_path, uploaded_file.name)
                    total_chunks += num_chunks
                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {e}")
                finally:
                    os.remove(tmp_path)
            
            progress_bar.progress((i + 1) / len(uploaded_files))
            
        st.success(f"Successfully memorized {len(uploaded_files)} documents ({total_chunks} chunks). Astro-GPT is ready.")


# Main Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add a greeting message
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Aloha! I am Astro-GPT and this is my fuzzy assistant, Stitch! Please feed us some astronomical PDF data in the sidebar, provide your AI key, and ask us anything from interpreting James Webb data to explaining stellar nucleosynthesis! 🌺🚀"
    })

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask about astrophysics, telescope data, or stellar dynamics..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if not api_key:
        with st.chat_message("assistant"):
            err_msg = "Please enter your Google Gemini API Key in the sidebar before querying."
            st.error(err_msg)
            st.session_state.messages.append({"role": "assistant", "content": err_msg})
    else:
        with st.chat_message("assistant"):
            with st.spinner("Accessing vector database & synthesizing answer..."):
                try:
                    import os
                    if api_key:
                        os.environ["gemini_api"] = api_key
                    
                    # Pass the prompt as the user_query and previous messages (excluding the current prompt) as history
                    response_text, context_chunks = rag_engine.query_astro_gpt(prompt, st.session_state.messages[:-1])
                    st.markdown(response_text)
                    
                    if context_chunks:
                        with st.expander("📚 View Retrieved Database Context"):
                            for i, chunk in enumerate(context_chunks):
                                st.markdown(f"**Source Chunk {i+1}:**\n {chunk}")
                                
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                except Exception as e:
                    st.error(f"An error occurred: {e}")
