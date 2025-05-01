[1mdiff --git a/dashboard.py b/dashboard.py[m
[1mindex 4a9fa05..9a6961f 100644[m
[1m--- a/dashboard.py[m
[1m+++ b/dashboard.py[m
[36m@@ -1,5 +1,4 @@[m
 import streamlit as st[m
[31m-import pandas as pd[m
 import json[m
 import yaml[m
 from pathlib import Path[m
[36m@@ -33,9 +32,9 @@[m [mdef load_agent_info():[m
             return yaml.safe_load(f)[m
     return {}[m
 [m
[31m-def load_persona(agent_id):[m
[31m-    path = Path(PERSONAS_DIR) / f"{agent_id}.txt"[m
[31m-    return path.read_text() if path.exists() else ""[m
[32m+[m[32mdef load_persona(file_name):[m
[32m+[m[32m    path = Path(PERSONAS_DIR) / f"{file_name}.txt"[m
[32m+[m[32m    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""[m
 [m
 def get_prompt_files():[m
     return [f.stem for f in Path(PROMPTS_DIR).glob("*.txt")][m
[36m@@ -75,7 +74,10 @@[m [mdef render_prompts_tab():[m
         prompt_files = get_prompt_files()[m
         selected = st.selectbox("Choose set to edit", prompt_files)[m
         if prompt_files:[m
[31m-            current_content = Path(PROMPTS_DIR, f"{selected}.txt").read_text()[m
[32m+[m[32m            try:[m
[32m+[m[32m                current_content = Path(PROMPTS_DIR, f"{selected}.txt").read_text(encoding="utf-8")[m
[32m+[m[32m            except UnicodeDecodeError:[m
[32m+[m[32m                current_content = Path(PROMPTS_DIR, f"{selected}.txt").read_text(encoding="utf-8", errors="replace")[m
             new_content = st.text_area("Edit prompts", value=current_content, height=300)[m
             if st.button("Save Changes"):[m
                 Path(PROMPTS_DIR, f"{selected}.txt").write_text(new_content)[m
[36m@@ -88,7 +90,10 @@[m [mdef render_prompts_tab():[m
         st.subheader("All Prompt Sets")[m
         for p in get_prompt_files():[m
             with st.expander(p):[m
[31m-                content = Path(PROMPTS_DIR, f"{p}.txt").read_text()[m
[32m+[m[32m                try:[m
[32m+[m[32m                    content = Path(PROMPTS_DIR, f"{p}.txt").read_text(encoding="utf-8")[m
[32m+[m[32m                except UnicodeDecodeError:[m
[32m+[m[32m                    content = Path(PROMPTS_DIR, f"{p}.txt").read_text(encoding="utf-8", errors="replace")[m
                 st.text(content)[m
 [m
 def render_evaluation_criteria_tab():[m
[36m@@ -201,8 +206,15 @@[m [mdef render_persona_tab():[m
 [m
     custom_request = st.text_area("Custom Change Request (optional)", placeholder="e.g., Make it sound more inclusive")[m
 [m
[32m+[m[32m    # Initialize OpenAI client[m
[32m+[m[32m    from openai import OpenAI[m
[32m+[m[32m    api_key = st.session_state.get("OPENAI_API_KEY")[m
[32m+[m[32m    if not api_key:[m
[32m+[m[32m        st.error("Please enter your OpenAI API key in the Connections tab.")[m
[32m+[m[32m        return[m
[32m+[m[32m    client = OpenAI(api_key=api_key)[m
[32m+[m
     if st.button("Suggest Improvements"):[m
[31m-        openai.api_key = st.session_state.get("OPENAI_API_KEY")[m
         system_msg = "You are a marketing and persona refinement expert."[m
         user_prompt = f"""[m
         Review the following persona:[m
[36m@@ -217,7 +229,7 @@[m [mdef render_persona_tab():[m
         2. The rationale for each suggestion[m
         """[m
 [m
[31m-        response = openai.ChatCompletion.create([m
[32m+[m[32m        response = client.chat.completions.create([m
             model="gpt-4-turbo",[m
             messages=[[m
                 {"role": "system", "content": system_msg},[m
[36m@@ -230,7 +242,6 @@[m [mdef render_persona_tab():[m
         st.text_area("Suggestions", feedback, height=300)[m
 [m
     if st.button("Generate Optimized Persona"):[m
[31m-        openai.api_key = st.session_state.get("OPENAI_API_KEY")[m
         system_msg = "You are a marketing persona optimization expert."[m
         user_prompt = f"""[m
         Optimize the following marketing persona based on this user request:[m
[36m@@ -245,7 +256,7 @@[m [mdef render_persona_tab():[m
         3. Reasoning behind the changes[m
         """[m
 [m
[31m-        response = openai.ChatCompletion.create([m
[32m+[m[32m        response = client.chat.completions.create([m
             model="gpt-4-turbo",[m
             messages=[[m
                 {"role": "system", "content": system_msg},[m
