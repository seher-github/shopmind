from crewai import Agent, LLM
import streamlit as st

def create_data_agent(llm: LLM) -> Agent:
    from tools.shop_tools import ProductSearchTool, PolicySearchTool

    return Agent(
        role="Shop Data Specialist",
        goal="Accurately retrieve product availability, prices, sizes and relevant shop policies for the customer question.",
        backstory=(
            "You are the reliable inventory and policy expert of a small clothing shop. "
            "You only use the official catalog and policy documents. You never invent stock or prices."
        ),
        tools=[ProductSearchTool(), PolicySearchTool()],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3,
    )
