from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from data.shop_data import PRODUCTS, POLICIES
import json

class ProductSearchInput(BaseModel):
    query: str = Field(..., description="Customer question or product keywords")

class ProductSearchTool(BaseTool):
    name: str = "product_search"
    description: str = "Search the shop catalog for products matching the customer query. Returns name, price, sizes & stock."
    args_schema: Type[BaseModel] = ProductSearchInput

    def _run(self, query: str) -> str:
        query_lower = query.lower()
        matches = []
        for p in PRODUCTS:
            if (p["name"].lower() in query_lower or
                p["category"] in query_lower or
                any(word in query_lower for word in p["name"].lower().split()) or
                any(kw in query_lower for kw in ["t-shirt", "jacket", "dress", "stock", "price", "size"])):
                matches.append(p)

        if not matches and any(kw in query_lower for kw in ["price", "stock", "size", "available"]):
            matches = PRODUCTS

        return json.dumps(matches, indent=2) if matches else "No matching products found."

class PolicySearchInput(BaseModel):
    query: str = Field(..., description="Customer question about delivery, returns, payment, etc.")

class PolicySearchTool(BaseTool):
    name: str = "policy_search"
    description: str = "Look up shop policies for delivery, returns, shipping regions or payment."
    args_schema: Type[BaseModel] = PolicySearchInput

    def _run(self, query: str) -> str:
        query_lower = query.lower()
        relevant = {}
        if any(kw in query_lower for kw in ["deliver", "ship", "shipping", "when will"]):
            relevant["delivery"] = POLICIES["delivery"]
            relevant["shipping_regions"] = POLICIES["shipping_regions"]
        if any(kw in query_lower for kw in ["return", "refund", "exchange"]):
            relevant["returns"] = POLICIES["returns"]
        if any(kw in query_lower for kw in ["pay", "payment", "card"]):
            relevant["payment"] = POLICIES["payment"]
        return json.dumps(relevant, indent=2) if relevant else "No specific policy matched."
