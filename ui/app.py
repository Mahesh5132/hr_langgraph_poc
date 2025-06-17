
### --- hr_langgraph_poc/ui/app.py ---
import streamlit as st
from router.router_chain import get_intent
from graph.hr_graph import graph
from utils.user_context import get_user_context

st.title("🧑\u200d💼 HR Assistant Chatbot")

user_input = st.chat_input("Ask HR anything...")

if user_input:
    user_context = get_user_context()
    intent = get_intent(user_input)

    state = {
        "input": user_input,
        "intent": intent,
        "employee_id": user_context["employee_id"],
        "role": user_context["role"],
        "month": "June"  # In real system, use NLP to extract this
    }

    result = graph.invoke(state)
    st.chat_message("assistant").markdown(result["response"])