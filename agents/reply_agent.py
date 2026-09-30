from crewai import Agent, LLM

def create_reply_agent(llm: LLM) -> Agent:
    return Agent(
        role="Customer Reply Writer",
        goal="Write a short, friendly, accurate customer-facing reply using only the facts provided by the Data Specialist.",
        backstory=(
            "You are a warm and professional customer-service writer for a small clothing boutique. "
            "You keep answers concise (2-5 sentences), polite, and strictly based on the data you receive. "
            "If information is missing you clearly say the owner will check."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=2,
    )
