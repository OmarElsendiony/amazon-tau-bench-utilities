import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FetchInvestorsWithPortfolioHoldings(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Dict[str, Any]) -> str:
        investors = data.get("investors", {})
        portfolios = data.get("portfolios", {})
        holdings = data.get("portfolio_holdings", {})
        instruments = data.get("instruments", {})
        results = []
        
        for investor in investors.values():
            # Apply filters to investors
            skip_investor = False
            for key, value in filters.items():
                if key in investor and investor.get(key) != value:
                    skip_investor = True
                    break
            
            if skip_investor:
                continue
            
            # Get investor's portfolios
            investor_portfolios = []
            for portfolio in portfolios.values():
                if portfolio.get("investor_id") == investor.get("investor_id"):
                    # Get holdings for this portfolio
                    portfolio_holdings = []
                    for holding in holdings.values():
                        if holding.get("portfolio_id") == portfolio.get("portfolio_id"):
                            # Enrich holding with instrument info
                            instrument_id = holding.get("instrument_id")
                            if instrument_id and str(instrument_id) in instruments:
                                holding_with_instrument = holding.copy()
                                holding_with_instrument["instrument"] = instruments[str(instrument_id)]
                                portfolio_holdings.append(holding_with_instrument)
                            else:
                                portfolio_holdings.append(holding)
                    
                    portfolio_with_holdings = portfolio.copy()
                    portfolio_with_holdings["holdings"] = portfolio_holdings
                    investor_portfolios.append(portfolio_with_holdings)
            
            investor_with_portfolios = investor.copy()
            investor_with_portfolios["portfolios"] = investor_portfolios
            results.append(investor_with_portfolios)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_investors_with_portfolio_holdings",
                "description": "Fetch investors with their portfolio holdings",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filters": {"type": "object", "description": "Filter criteria for investors"}
                    },
                    "required": ["filters"]
                }
            }
        }
