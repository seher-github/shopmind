import streamlit as st
from crew.shopmind_crew import run_shopmind_crew

st.set_page_config(page_title="ShopMind", page_icon="🛍️", layout="centered")
st.title("🛍️ ShopMind")
st.caption("CrewAI multi-agent assistant for small clothing shops")

with st.sidebar:
    st.header("Owner Dashboard")
    st.info("Messages that need review appear here.")
    if "pending" not in st.session_state:
        st.session_state.pending = []
    for i, item in enumerate(st.session_state.pending):
        with st.expander(f"Review #{i+1}"):
            st.write("**Customer:**", item["msg"])
            st.write("**Draft:**", item["reply"])
            st.write("**Reason:**", item["reason"])
            if st.button("Approve & mark sent", key=f"ok_{i}"):
                st.session_state.pending.pop(i)
                st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type a customer message…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("CrewAI agents working…"):
            try:
                result = run_shopmind_crew(prompt)
            except Exception as e:
                st.error(f"Error: {e}")
                st.stop()

        draft = result["draft"]
        decision = result["decision"]
        reason = result["reason"]

        if decision == "AUTO_SEND":
            st.markdown(draft)
            st.success("✅ Auto-sent (safe)")
            st.session_state.messages.append({"role": "assistant", "content": draft})
        else:
            st.warning("⚠️ Needs owner review")
            st.markdown(f"**Draft reply:**\n\n{draft}")
            st.caption(f"Reason: {reason}")
            st.session_state.pending.append({
                "msg": prompt,
                "reply": draft,
                "reason": reason,
            })
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"[Pending owner review]\n\n{draft}"
            })
