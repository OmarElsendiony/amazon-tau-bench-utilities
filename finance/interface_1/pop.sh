#!/bin/bash

# Create individual tool files with their content

# Read APIs
cat << 'EOF' > get_user.py
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_user(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: Optional[str] = None, 
               email: Optional[str] = None, first_name: Optional[str] = None, 
               last_name: Optional[str] = None) -> str:
        users = data.get("users", {})
        
        for user in users.values():
            if user_id and user.get("user_id") != user_id:
                continue
            if email and user.get("email", "").lower() != email.lower():
                continue
            if first_name and first_name.lower() not in user.get("first_name", "").lower():
                continue
            if last_name and last_name.lower() not in user.get("last_name", "").lower():
                continue
            return json.dumps(user)
        
        raise ValueError("User not found")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user",
                "description": "Get user details by ID, email, or name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User ID"},
                        "email": {"type": "string", "description": "User email"},
                        "first_name": {"type": "string", "description": "User first name"},
                        "last_name": {"type": "string", "description": "User last name"}
                    },
                    "required": []
                }
            }
        }
EOF

cat << 'EOF' > get_investors.py
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_investors(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], employee_id: Optional[str] = None,
               investor_type: Optional[str] = None, accreditation_status: Optional[str] = None,
               name: Optional[str] = None) -> str:
        investors = data.get("investors", {})
        results = []
        
        for investor in investors.values():
            if employee_id and investor.get("employee_id") != employee_id:
                continue
            if investor_type and investor.get("investor_type") != investor_type:
                continue
            if accreditation_status and investor.get("accreditation_status") != accreditation_status:
                continue
            if name and name.lower() not in investor.get("name", "").lower():
                continue
            results.append(investor)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investors",
                "description": "Get investors with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "Filter by employee ID"},
                        "investor_type": {"type": "string", "description": "Filter by investor type (organization, retail, high_net_worth)"},
                        "accreditation_status": {"type": "string", "description": "Filter by accreditation status (accredited, non_accredited)"},
                        "name": {"type": "string", "description": "Filter by investor name (partial match)"}
                    },
                    "required": []
                }
            }
        }
EOF

cat << 'EOF' > get_funds.py
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_funds(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_type: Optional[str] = None,
               base_currency: Optional[str] = None, manager_id: Optional[str] = None,
               status: Optional[str] = None, name: Optional[str] = None) -> str:
        funds = data.get("funds", {})
        results = []
        
        for fund in funds.values():
            if fund_type and fund.get("fund_type") != fund_type:
                continue
            if base_currency and fund.get("base_currency") != base_currency:
                continue
            if manager_id and fund.get("manager_id") != manager_id:
                continue
            if status and fund.get("status") != status:
                continue
            if name and name.lower() not in fund.get("name", "").lower():
                continue
            results.append(fund)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_funds",
                "description": "Get funds with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_type": {"type": "string", "description": "Filter by fund type (equity, fixed_income, multi_asset, hedge)"},
                        "base_currency": {"type": "string", "description": "Filter by base currency (USD, EUR, GBP, NGN)"},
                        "manager_id": {"type": "string", "description": "Filter by manager ID"},
                        "status": {"type": "string", "description": "Filter by status (open, closed)"},
                        "name": {"type": "string", "description": "Filter by fund name (partial match)"}
                    },
                    "required": []
                }
            }
        }
EOF

cat << 'EOF' > get_investor_portfolio.py
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class get_investor_portfolio(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str) -> str:
        portfolios = data.get("portfolios", {})
        
        for portfolio in portfolios.values():
            if portfolio.get("investor_id") == investor_id:
                return json.dumps(portfolio)
        
        raise ValueError(f"Portfolio for investor {investor_id} not found")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_portfolio",
                "description": "Get portfolio for a specific investor",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"}
                    },
                    "required": ["investor_id"]
                }
            }
        }
EOF

cat << 'EOF' > get_subscriptions.py
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_subscriptions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: Optional[str] = None,
               investor_id: Optional[str] = None, status: Optional[str] = None,
               currency: Optional[str] = None, request_assigned_to: Optional[str] = None) -> str:
        subscriptions = data.get("subscriptions", {})
        results = []
        
        for subscription in subscriptions.values():
            if fund_id and subscription.get("fund_id") != fund_id:
                continue
            if investor_id and subscription.get("investor_id") != investor_id:
                continue
            if status and subscription.get("status") != status:
                continue
            if currency and subscription.get("currency") != currency:
                continue
            if request_assigned_to and subscription.get("request_assigned_to") != request_assigned_to:
                continue
            results.append(subscription)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_subscriptions",
                "description": "Get subscriptions with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "status": {"type": "string", "description": "Filter by status (pending, approved, cancelled)"},
                        "currency": {"type": "string", "description": "Filter by currency (USD, EUR, GBP, NGN)"},
                        "request_assigned_to": {"type": "string", "description": "Filter by assigned user ID"}
                    },
                    "required": []
                }
            }
        }
EOF

cat << 'EOF' > get_investor_portfolio_holdings.py
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class get_investor_portfolio_holdings(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], portfolio_id: str) -> str:
        portfolio_holdings = data.get("portfolio_holdings", {})
        results = []
        
        for holding in portfolio_holdings.values():
            if holding.get("portfolio_id") == portfolio_id:
                results.append(holding)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_portfolio_holdings",
                "description": "Get holdings for a specific portfolio",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "portfolio_id": {"type": "string", "description": "ID of the portfolio"}
                    },
                    "required": ["portfolio_id"]
                }
            }
        }
EOF

cat << 'EOF' > get_instruments.py
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_instruments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], ticker: Optional[str] = None,
               name: Optional[str] = None, instrument_type: Optional[str] = None) -> str:
        instruments = data.get("instruments", {})
        results = []
        
        for instrument in instruments.values():
            if ticker and instrument.get("ticker", "").lower() != ticker.lower():
                continue
            if name and name.lower() not in instrument.get("name", "").lower():
                continue
            if instrument_type and instrument.get("instrument_type") != instrument_type:
                continue
            results.append(instrument)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_instruments",
                "description": "Get instruments with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string", "description": "Filter by ticker symbol"},
                        "name": {"type": "string", "description": "Filter by instrument name (partial match)"},
                        "instrument_type": {"type": "string", "description": "Filter by instrument type (stock, bond, derivative, cash, other)"}
                    },
                    "required": []
                }
            }
        }
EOF

cat << 'EOF' > get_portfolio_status_by_date.py
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class get_portfolio_status_by_date(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], portfolio_id: str, date: str) -> str:
        portfolio_holdings = data.get("portfolio_holdings", {})
        instrument_prices = data.get("instrument_prices", {})
        
        total_value = 0.0
        
        for holding in portfolio_holdings.values():
            if holding.get("portfolio_id") != portfolio_id:
                continue
            
            instrument_id = holding.get("instrument_id")
            quantity = float(holding.get("quantity", 0))
            
            # Find the price for the given date
            price = None
            for price_record in instrument_prices.values():
                if (price_record.get("instrument_id") == instrument_id and 
                    price_record.get("price_date") == date):
                    price = float(price_record.get("close_price", 0))
                    break
            
            if price is not None:
                total_value += quantity * price
        
        return json.dumps({"portfolio_value": round(total_value, 2)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_portfolio_status_by_date",
                "description": "Get portfolio value for a specific date",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "portfolio_id": {"type": "string", "description": "ID of the portfolio"},
                        "date": {"type": "string", "description": "Date in YYYY-MM-DD format"}
                    },
                    "required": ["portfolio_id", "date"]
                }
            }
        }
EOF

cat << 'EOF' > get_instruments_prices.py
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_instruments_prices(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_id: Optional[str] = None,
               price_date: Optional[str] = None, ticker: Optional[str] = None) -> str:
        instrument_prices = data.get("instrument_prices", {})
        instruments = data.get("instruments", {})
        results = []
        
        for price in instrument_prices.values():
            if instrument_id and price.get("instrument_id") != instrument_id:
                continue
            if price_date and price.get("price_date") != price_date:
                continue
            
            # If ticker filter is provided, need to check instrument data
            if ticker:
                instrument = None
                for inst in instruments.values():
                    if inst.get("instrument_id") == price.get("instrument_id"):
                        instrument = inst
                        break
                if not instrument or instrument.get("ticker", "").lower() != ticker.lower():
                    continue
            
            # Merge instrument data with price data
            instrument_with_price = dict(price)
            for inst in instruments.values():
                if inst.get("instrument_id") == price.get("instrument_id"):
                    instrument_with_price.update(inst)
                    break
            
            results.append(instrument_with_price)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_instruments_prices",
                "description": "Get instrument prices with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {"type": "string", "description": "Filter by instrument ID"},
                        "price_date": {"type": "string", "description": "Filter by price date (YYYY-MM-DD)"},
                        "ticker": {"type": "string", "description": "Filter by ticker symbol"}
                    },
                    "required": []
                }
            }
        }
EOF

cat << 'EOF' > get_commitments.py
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_commitments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: Optional[str] = None,
               investor_id: Optional[str] = None, status: Optional[str] = None,
               currency: Optional[str] = None) -> str:
        commitments = data.get("commitments", {})
        results = []
        
        for commitment in commitments.values():
            if fund_id and commitment.get("fund_id") != fund_id:
                continue
            if investor_id and commitment.get("investor_id") != investor_id:
                continue
            if status and commitment.get("status") != status:
                continue
            if currency and commitment.get("currency") != currency:
                continue
            results.append(commitment)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_commitments",
                "description": "Get commitments with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "status": {"type": "string", "description": "Filter by status (pending, fulfilled)"},
                        "currency": {"type": "string", "description": "Filter by currency (USD, EUR, GBP, NGN)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Write APIs
cat << 'EOF' > onboard_new_investor.py
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class onboard_new_investor(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: str, employee_id: str,
               investor_type: str, contact_email: str, accreditation_status: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        investors = data.get("investors", {})
        users = data.get("users", {})
        
        # Validate employee exists
        if str(employee_id) not in users:
            raise ValueError(f"Employee {employee_id} not found")
        
        # Validate investor_type
        valid_types = ["organization", "retail", "high_net_worth"]
        if investor_type not in valid_types:
            raise ValueError(f"Invalid investor type. Must be one of {valid_types}")
        
        # Validate accreditation_status
        valid_statuses = ["accredited", "non_accredited"]
        if accreditation_status not in valid_statuses:
            raise ValueError(f"Invalid accreditation status. Must be one of {valid_statuses}")
        
        investor_id = generate_id(investors)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_investor = {
            "investor_id": investor_id,
            "employee_id": employee_id,
            "name": name,
            "investor_type": investor_type,
            "contact_email": contact_email,
            "accreditation_status": accreditation_status,
            "created_at": timestamp
        }
        
        investors[investor_id] = new_investor
        return json.dumps(new_investor)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "onboard_new_investor",
                "description": "Onboard a new investor",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Investor name"},
                        "employee_id": {"type": "string", "description": "Employee ID handling the investor"},
                        "investor_type": {"type": "string", "description": "Type of investor (organization, retail, high_net_worth)"},
                        "contact_email": {"type": "string", "description": "Contact email address"},
                        "accreditation_status": {"type": "string", "description": "Accreditation status (accredited, non_accredited)"}
                    },
                    "required": ["name", "employee_id", "investor_type", "contact_email", "accreditation_status"]
                }
            }
        }
EOF