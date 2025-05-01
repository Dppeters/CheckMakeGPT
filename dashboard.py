import streamlit as st
<<<<<<< HEAD
import pandas as pd
=======
>>>>>>> clean-main
import json
import yaml
from pathlib import Path
import os
import time
from datetime import datetime
from core.tester import CustomGPTTester
from core.openai_evaluator import OpenAIScorer
import openai

CONFIG_DIR = "config"
PROMPTS_DIR = "prompts"
OUTPUTS_DIR = "outputs"
PERSONAS_DIR = "personas"
os.makedirs(CONFIG_DIR, exist_ok=True)
os.makedirs(PROMPTS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(PERSONAS_DIR, exist_ok=True)

AGENT_FILE = Path(CONFIG_DIR) / "agent_info.yaml"

def save_agent_info(agent_id, persona, nickname=""):
    with open(AGENT_FILE, "w") as f:
        yaml.dump({"agent_id": agent_id, "nickname": nickname}, f)
    with open(Path(PERSONAS_DIR) / f"{agent_id}.txt", "w") as f:
        f.write(persona)

def load_agent_info():
    if AGENT_FILE.exists():
        with open(AGENT_FILE, "r") as f:
            return yaml.safe_load(f)
    return {}

def load_persona(agent_id):
    path = Path(PERSONAS_DIR) / f"{agent_id}.txt"
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""

def get_prompt_files():
    return [f.stem for f in Path(PROMPTS_DIR).glob("*.txt")]

def load_prompts(filename):
    with open(Path(PROMPTS_DIR) / f"{filename}.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

def get_criteria_files():
    return [f.stem.replace("criteria_", "") for f in Path(CONFIG_DIR).glob("criteria_*.yaml")]

def validate_environment():
    errors = []
    if "CUSTOMGPT_API_KEY" not in st.session_state:
        errors.append("CustomGPT API key not provided")
    if "OPENAI_API_KEY" not in st.session_state:
        errors.append("OpenAI API key not provided")
    return errors if errors else None

def render_prompts_tab():
    st.title("Prompt Management")
    tab1, tab2, tab3 = st.tabs(["Create New", "Edit Existing", "View All"])

    with tab1:
        with st.form("new_prompt_set"):
            name = st.text_input("Set Name*", help="No special characters or spaces")
            prompts = st.text_area("Prompts*", height=300)
            if st.form_submit_button("Save Set"):
                if not name or not prompts:
                    st.error("Name and prompts are required")
                else:
                    (Path(PROMPTS_DIR) / f"{name}.txt").write_text(prompts)
                    st.success(f"Saved '{name}' successfully!")

    with tab2:
        st.subheader("Edit Existing Set")
        prompt_files = get_prompt_files()
        selected = st.selectbox("Choose set to edit", prompt_files)
        if prompt_files:
<<<<<<< HEAD
            current_content = Path(PROMPTS_DIR, f"{selected}.txt").read_text()
=======
            try:
                current_content = Path(PROMPTS_DIR, f"{selected}.txt").read_text(encoding="utf-8")
            except UnicodeDecodeError:
                current_content = Path(PROMPTS_DIR, f"{selected}.txt").read_text(encoding="utf-8", errors="replace")
>>>>>>> clean-main
            new_content = st.text_area("Edit prompts", value=current_content, height=300)
            if st.button("Save Changes"):
                Path(PROMPTS_DIR, f"{selected}.txt").write_text(new_content)
                st.success("Updated successfully!")
            if st.button("Delete Set", type="secondary"):
                Path(PROMPTS_DIR, f"{selected}.txt").unlink()
                st.rerun()

    with tab3:
        st.subheader("All Prompt Sets")
        for p in get_prompt_files():
            with st.expander(p):
<<<<<<< HEAD
                content = Path(PROMPTS_DIR, f"{p}.txt").read_text()
=======
                try:
                    content = Path(PROMPTS_DIR, f"{p}.txt").read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    content = Path(PROMPTS_DIR, f"{p}.txt").read_text(encoding="utf-8", errors="replace")
>>>>>>> clean-main
                st.text(content)

def render_evaluation_criteria_tab():
    st.title("Evaluation Criteria")
    criteria_files = get_criteria_files()
    preset_to_load = st.selectbox("Load Existing Preset", criteria_files)

    if "criteria" not in st.session_state:
        if preset_to_load:
            preset_path = Path(CONFIG_DIR) / f"criteria_{preset_to_load}.yaml"
            st.session_state.criteria = yaml.safe_load(preset_path.read_text())
        else:
            st.session_state.criteria = []

    st.subheader("Edit Criteria")
    edited = []
    for i, criterion in enumerate(st.session_state.criteria):
        cols = st.columns([1, 3, 1, 0.5])
        with cols[0]:
            name = st.text_input("Name", value=criterion["name"], key=f"name_{i}")
        with cols[1]:
            desc = st.text_input("Description", value=criterion["description"], key=f"desc_{i}")
        with cols[2]:
            weight = st.number_input("Weight", 0.0, 1.0, step=0.05, value=criterion["weight"], key=f"weight_{i}")
        with cols[3]:
            delete = st.button("❌", key=f"delete_{i}")
        if not delete:
            edited.append({"name": name, "description": desc, "weight": weight})

    st.session_state.criteria = edited
    total_weight = sum(item["weight"] for item in edited)
    st.caption(f"Total weight: {total_weight:.2f}")
    if abs(total_weight - 1.0) > 0.001:
        st.error("Weights must sum to 1.0")

    new_name = st.text_input("Save as preset...")
    if st.button("Save Preset") and new_name:
        preset_path = Path(CONFIG_DIR) / f"criteria_{new_name}.yaml"
        preset_path.write_text(yaml.dump(st.session_state.criteria))
        st.success(f"Saved as '{new_name}' preset")

    if st.button("Reload Selected Preset"):
        preset_path = Path(CONFIG_DIR) / f"criteria_{preset_to_load}.yaml"
        st.session_state.criteria = yaml.safe_load(preset_path.read_text())
        st.rerun()

def render_run_evaluation_tab():
    st.title("Run Evaluation")
    if env_errors := validate_environment():
        st.error("\n".join(env_errors))
        return

    info = load_agent_info()
    current_agent_id = info.get("agent_id", "")
    current_nickname = info.get("nickname", current_agent_id)
    st.selectbox("Agent to Evaluate", options=[current_nickname] if current_nickname else ["No agent configured"], index=0)

    col1, col2 = st.columns(2)
    with col1:
        prompt_set = st.selectbox("Prompt Set", get_prompt_files())
    with col2:
        criteria_file = st.selectbox("Evaluation Criteria", get_criteria_files())

    if st.button("Run Full Evaluation"):
        prompts = load_prompts(prompt_set)
        criteria = yaml.safe_load(Path(CONFIG_DIR, f"criteria_{criteria_file}.yaml").read_text())
        tester = CustomGPTTester()
        scorer = OpenAIScorer(criteria)

        progress_bar = st.progress(0)
        results = []

        for i, prompt in enumerate(prompts):
            test_result = tester.test_prompt(prompt)
            if test_result["success"]:
                evaluation = scorer.evaluate(prompt, test_result["response"])
                result = {
                    "timestamp": datetime.now().isoformat(),
                    "prompt": prompt,
                    "response": test_result["response"],
                    "conversation_id": test_result["conversation_id"],
                    **evaluation
                }
                st.json(result)
                results.append(result)
            else:
                st.error(f"Failed on prompt '{prompt[:50]}...': {test_result['error']}")

            progress_bar.progress((i + 1) / len(prompts))
            time.sleep(1)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_path = Path(OUTPUTS_DIR) / f"results_{timestamp}.json"
        result_path.write_text(json.dumps(results, indent=2))
        st.success(f"Results saved to: {result_path}")
        st.download_button("Download JSON", data=json.dumps(results, indent=2), file_name=result_path.name)

def render_persona_tab():
    st.title("Persona Workshop")

    info = load_agent_info()
    agent_id = info.get("agent_id", "")
    if not agent_id:
        st.warning("No agent configured. Please set one in the Agent tab.")
        return

    persona = load_persona(agent_id)
    st.subheader("Current Persona")
    st.text_area("Persona Content", persona, height=250, key="loaded_persona")

    custom_request = st.text_area("Custom Change Request (optional)", placeholder="e.g., Make it sound more inclusive")

<<<<<<< HEAD
    if st.button("Suggest Improvements"):
        openai.api_key = st.session_state.get("OPENAI_API_KEY")
=======
    # Initialize OpenAI client
    from openai import OpenAI
    api_key = st.session_state.get("OPENAI_API_KEY")
    if not api_key:
        st.error("Please enter your OpenAI API key in the Connections tab.")
        return
    client = OpenAI(api_key=api_key)

    if st.button("Suggest Improvements"):
>>>>>>> clean-main
        system_msg = "You are a marketing and persona refinement expert."
        user_prompt = f"""
        Review the following persona:

        {persona}

        Suggest specific edits to improve effectiveness, clarity, tone, or alignment with brand. Consider this user request:
        {custom_request or 'N/A'}

        Provide:
        1. A list of suggested edits
        2. The rationale for each suggestion
        """

<<<<<<< HEAD
        response = openai.ChatCompletion.create(
=======
        response = client.chat.completions.create(
>>>>>>> clean-main
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        feedback = response.choices[0].message.content
        st.subheader("Suggested Edits")
        st.text_area("Suggestions", feedback, height=300)

    if st.button("Generate Optimized Persona"):
<<<<<<< HEAD
        openai.api_key = st.session_state.get("OPENAI_API_KEY")
=======
>>>>>>> clean-main
        system_msg = "You are a marketing persona optimization expert."
        user_prompt = f"""
        Optimize the following marketing persona based on this user request:
        {custom_request or 'Make it clearer and more engaging'}

        Persona:
        {persona}

        Provide:
        1. An improved version
        2. Key changes made
        3. Reasoning behind the changes
        """

<<<<<<< HEAD
        response = openai.ChatCompletion.create(
=======
        response = client.chat.completions.create(
>>>>>>> clean-main
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        optimized = response.choices[0].message.content
        st.subheader("Optimized Persona")
        st.text_area("Result", optimized, height=300)

def render_agent_tab():
    st.title("Agent Setup")
    info = load_agent_info()
    current_id = info.get("agent_id", "")
    current_nickname = info.get("nickname", "")
    current_persona = load_persona(current_id) if current_id else ""

    with st.form("agent_setup"):
        agent_id = st.text_input("Agent ID (CustomGPT Project ID)", value=current_id)
        nickname = st.text_input("Agent Nickname", value=current_nickname)
        persona_text = st.text_area("Agent Persona", value=current_persona, height=300)
        if st.form_submit_button("Save Agent"):
            save_agent_info(agent_id, persona_text, nickname)
            st.success("Agent info and persona saved.")

def render_connections_tab():
    st.title("API Keys Only")
    with st.form("api_keys"):
        openai_key = st.text_input("OpenAI API Key", type="password")
        customgpt_key = st.text_input("CustomGPT API Key", type="password")

        if st.form_submit_button("Save Keys"):
            if openai_key:
                st.session_state["OPENAI_API_KEY"] = openai_key
                openai.api_key = openai_key
            if customgpt_key:
                st.session_state["CUSTOMGPT_API_KEY"] = customgpt_key
            st.success("Keys saved for this session.")

def main():
    st.set_page_config(layout="wide", page_title="CheckMakeGPT")
    with st.sidebar:
        st.title("CheckMakeGPT")
        tab = st.radio("Navigation", [
            "📦 Agent",
            "📝 Prompts",
            "⚙️ Evaluation Criteria",
            "▶️ Run Evaluation",
            "🧐 Persona Optimizer",
            "🔐 Connections"
        ])
        st.markdown("---")
        info = load_agent_info()
        st.info(f"Agent: {info.get('nickname') or info.get('agent_id', 'Not set')}")
        st.caption(f"Model: gpt-4-turbo")

    if tab == "📝 Prompts":
        render_prompts_tab()
    elif tab == "⚙️ Evaluation Criteria":
        render_evaluation_criteria_tab()
    elif tab == "▶️ Run Evaluation":
        render_run_evaluation_tab()
    elif tab == "🧐 Persona Optimizer":
        render_persona_tab()
    elif tab == "📦 Agent":
        render_agent_tab()
    elif tab == "🔐 Connections":
        render_connections_tab()

if __name__ == "__main__":
    main()