from crewai import Agent, LLM

def create_safety_agent(llm: LLM) -> Agent:
    return Agent(
        role="Safety & Compliance Reviewer",
        goal="Decide whether a drafted reply is safe to send automatically or must be reviewed by the shop owner.",
        backstory=(
            "You are the careful safety gatekeeper. You approve replies only when they are accurate, "
            "polite, contain no invented facts, and do not involve complaints, refunds, legal issues or uncertain stock. "
            "When in doubt you always choose NEEDS_REVIEW."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=2,
    )
