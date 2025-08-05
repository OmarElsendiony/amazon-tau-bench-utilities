import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FetchInvestorPortfolio(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str) -> str:
        portfolios = data.get("portfolios", {})
        portfolio_holdings = data.get("portfolio_holdings", {})
        instruments = data.get("instruments", {})
        
        # Find portfolios for the investor
        investor_portfolios = []
        for portfolio in portfolios.values():
            if portfolio.get("investor_id") == investor_id:
                portfolio_with_holdings = portfolio.copy()
                
                # Get holdings for this portfolio
                holdings = []
                for holding in portfolio_holdings.values():
                    if holding.get("portfolio_id") == portfolio.get("portfolio_id"):
                        holding_with_instrument = holding.copy()
                        
                        # Add instrument details
                        instrument_id = holding.get("instrument_id")
                        if instrument_id and str(instrument_id) in instruments:
                            holding_with_instrument["instrument"] = instruments[str(instrument_id)]
                        
                        holdings.append(holding_with_instrument)
                
                portfolio_with_holdings["holdings"] = holdings
                investor_portfolios.append(portfolio_with_holdings)
        
        return json.dumps(investor_portfolios)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_investor_portfolio",
                "description": "Fetch portfolio and holdings for a specific investor",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"}
                    },
                    "required": ["investor_id"]
                }
            }
        }
