from crewai import Crew, Task, Process, LLM
import streamlit as st
from agents.data_agent import create_data_agent
from agents.reply_agent import create_reply_agent
from agents.safety_agent import create_safety_agent

def get_llm() -> LLM:
    return LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=st.secrets["GROQ_API_KEY"],
        temperature=0.2,
    )

def run_shopmind_crew(customer_message: str) -> dict:
    llm = get_llm()

    data_agent = create_data_agent(llm)
    reply_agent = create_reply_agent(llm)
    safety_agent = create_safety_agent(llm)

    data_task = Task(
        description=(
            f"Customer message: '{customer_message}'\n\n"
            "Use the product_search and policy_search tools to gather every relevant fact. "
            "Return a clear summary of products (name, price, sizes/stock) and any matching policies."
        ),
        expected_output="A structured summary of products and policies that answer the customer.",
        agent=data_agent,
    )

    reply_task = Task(
        description=(
            f"Customer message: '{customer_message}'\n\n"
            "Using ONLY the facts from the previous task, write a short, friendly, professional reply (2-5 sentences). "
            "Do not invent any information. If something is missing, say the owner will check."
        ),
        expected_output="A ready-to-send customer reply.",
        agent=reply_agent,
        context=[data_task],
    )

    safety_task = Task(
        description=(
            f"Customer message: '{customer_message}'\n"
            "Drafted reply: (see previous task output)\n\n"
            "Decide whether the draft is safe to send automatically.\n"
            "Reply with EXACTLY this format:\n"
            "DECISION: AUTO_SEND\n"
            "REASON: <one short sentence>\n"
            "or\n"
            "DECISION: NEEDS_REVIEW\n"
            "REASON: <one short sentence>\n"
            "Choose NEEDS_REVIEW for any uncertainty, complaint, refund request or possible hallucination."
        ),
        expected_output="DECISION and REASON in the exact format above.",
        agent=safety_agent,
        context=[reply_task],
    )

    crew = Crew(
        agents=[data_agent, reply_agent, safety_agent],
        tasks=[data_task, reply_task, safety_task],
        process=Process.sequential,
        verbose=True,
        max_rpm=10,
    )

    result = crew.kickoff()

    final_text = str(result)
    decision = "NEEDS_REVIEW"
    reason = "Could not parse safety decision"

    if "AUTO_SEND" in final_text.upper():
        decision = "AUTO_SEND"
    if "REASON:" in final_text.upper():
        try:
            reason = final_text.split("REASON:")[-1].strip().split("\n")[0]
        except Exception:
            pass

    draft_reply = str(reply_task.output) if reply_task.output else final_text

    return {
        "draft": draft_reply,
        "decision": decision,
        "reason": reason,
        "full_result": final_text,
    }
