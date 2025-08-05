#!/bin/bash

# Create directory for tools
mkdir -p db_tools
cd db_tools

# Tool 1: FetchUserByMail
cat > fetch_user_by_mail.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class FetchUserByMail(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], email: str) -> str:
        users = data.get("users", {})
        
        for user in users.values():
            if user.get("email", "").lower() == email.lower():
                return json.dumps(user)
        
        raise ValueError(f"User with email {email} not found")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_user_by_mail",
                "description": "Fetch a user by their email address",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "description": "Email address of the user"}
                    },
                    "required": ["email"]
                }
            }
        }
EOF

# Tool 2: RetrieveFundsWithFilter
cat > retrieve_funds_with_filter.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RetrieveFundsWithFilter(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: Optional[str] = None, manager_id: Optional[str] = None,
               size: Optional[float] = None, fund_type: Optional[str] = None, 
               base_currency: Optional[str] = None, status: Optional[str] = None) -> str:
        funds = data.get("funds", {})
        results = []
        
        for fund in funds.values():
            if name and name.lower() not in fund.get("name", "").lower():
                continue
            if manager_id and fund.get("manager_id") != manager_id:
                continue
            if size and fund.get("size") != size:
                continue
            if fund_type and fund.get("fund_type") != fund_type:
                continue
            if base_currency and fund.get("base_currency") != base_currency:
                continue
            if status and fund.get("status") != status:
                continue
            results.append(fund)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_funds_with_filter",
                "description": "Retrieve funds with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Fund name (partial match)"},
                        "manager_id": {"type": "string", "description": "Manager user ID"},
                        "size": {"type": "number", "description": "Fund size"},
                        "fund_type": {"type": "string", "description": "Fund type (equity, fixed_income, multi_asset, hedge)"},
                        "base_currency": {"type": "string", "description": "Base currency (USD, EUR, GBP, NGN)"},
                        "status": {"type": "string", "description": "Fund status (open, closed)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool 3: FetchInvestorsWithPortfolioHoldings
cat > fetch_investors_with_portfolio_holdings.py << 'EOF'
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
EOF

# Tool 4: FetchInstrumentsWithItsPrice
cat > fetch_instruments_with_its_price.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class FetchInstrumentsWithItsPrice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], ticker: Optional[str] = None, name: Optional[str] = None,
               instrument_type: Optional[str] = None, date: Optional[str] = None,
               price_id: Optional[str] = None, open_price: Optional[float] = None,
               close_price: Optional[float] = None, high_price: Optional[float] = None,
               low_price: Optional[float] = None) -> str:
        instruments = data.get("instruments", {})
        prices = data.get("instrument_prices", {})
        results = []
        
        for instrument in instruments.values():
            if ticker and instrument.get("ticker") != ticker:
                continue
            if name and name.lower() not in instrument.get("name", "").lower():
                continue
            if instrument_type and instrument.get("instrument_type") != instrument_type:
                continue
            
            # Get prices for this instrument
            instrument_prices = []
            for price in prices.values():
                if price.get("instrument_id") != instrument.get("instrument_id"):
                    continue
                if date and price.get("price_date") != date:
                    continue
                if price_id and price.get("price_id") != price_id:
                    continue
                if open_price is not None and price.get("open_price") != open_price:
                    continue
                if close_price is not None and price.get("close_price") != close_price:
                    continue
                if high_price is not None and price.get("high_price") != high_price:
                    continue
                if low_price is not None and price.get("low_price") != low_price:
                    continue
                instrument_prices.append(price)
            
            instrument_with_prices = instrument.copy()
            instrument_with_prices["prices"] = instrument_prices
            results.append(instrument_with_prices)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_instruments_with_its_price",
                "description": "Fetch instruments with their price information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string", "description": "Instrument ticker"},
                        "name": {"type": "string", "description": "Instrument name (partial match)"},
                        "instrument_type": {"type": "string", "description": "Instrument type (stock, bond, derivative, cash, other)"},
                        "date": {"type": "string", "description": "Price date"},
                        "price_id": {"type": "string", "description": "Price record ID"},
                        "open_price": {"type": "number", "description": "Opening price"},
                        "close_price": {"type": "number", "description": "Closing price"},
                        "high_price": {"type": "number", "description": "High price"},
                        "low_price": {"type": "number", "description": "Low price"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool 5: GetFundTradeDetails
cat > get_fund_trade_details.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetFundTradeDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, start_date: Optional[str] = None,
               instrument_id: Optional[str] = None, quantity: Optional[float] = None,
               price: Optional[float] = None, side: Optional[str] = None,
               end_date: Optional[str] = None) -> str:
        trades = data.get("trades", {})
        results = []
        
        for trade in trades.values():
            if trade.get("fund_id") != fund_id:
                continue
            if instrument_id and trade.get("instrument_id") != instrument_id:
                continue
            if quantity is not None and trade.get("quantity") != quantity:
                continue
            if price is not None and trade.get("price") != price:
                continue
            if side and trade.get("side") != side:
                continue
            
            # Date filtering (assuming trade_date is in ISO format)
            trade_date = trade.get("trade_date", "")
            if start_date and trade_date < start_date:
                continue
            if end_date and trade_date > end_date:
                continue
            
            results.append(trade)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_fund_trade_details",
                "description": "Get trade details for a specific fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Fund ID"},
                        "start_date": {"type": "string", "description": "Start date for filtering trades"},
                        "instrument_id": {"type": "string", "description": "Instrument ID"},
                        "quantity": {"type": "number", "description": "Trade quantity"},
                        "price": {"type": "number", "description": "Trade price"},
                        "side": {"type": "string", "description": "Trade side (buy, sell)"},
                        "end_date": {"type": "string", "description": "End date for filtering trades"}
                    },
                    "required": ["fund_id"]
                }
            }
        }
EOF

# Tool 6: GetNAVRecords
cat > get_nav_records.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetNAVRecords(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Dict[str, Any]) -> str:
        nav_records = data.get("nav_records", {})
        results = []
        
        for nav in nav_records.values():
            # Apply filters
            skip_record = False
            for key, value in filters.items():
                if key in nav and nav.get(key) != value:
                    skip_record = True
                    break
            
            if not skip_record:
                results.append(nav)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_nav_records",
                "description": "Get NAV records with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filters": {"type": "object", "description": "Filter criteria for NAV records"}
                    },
                    "required": ["filters"]
                }
            }
        }
EOF

# Tool 7: GetDailyProfitLossByFund
cat > get_daily_profit_loss_by_fund.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetDailyProfitLossByFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, date: str) -> str:
        nav_records = data.get("nav_records", {})
        trades = data.get("trades", {})
        
        # Find NAV records for the fund on the specified date and previous date
        current_nav = None
        previous_nav = None
        
        fund_navs = []
        for nav in nav_records.values():
            if nav.get("fund_id") == fund_id:
                fund_navs.append(nav)
        
        # Sort by date
        fund_navs.sort(key=lambda x: x.get("nav_date", ""))
        
        # Find current and previous NAV
        for i, nav in enumerate(fund_navs):
            if nav.get("nav_date") == date:
                current_nav = nav.get("nav_value", 0)
                if i > 0:
                    previous_nav = fund_navs[i-1].get("nav_value", 0)
                break
        
        if current_nav is None:
            raise ValueError(f"No NAV record found for fund {fund_id} on date {date}")
        
        # Calculate P&L
        if previous_nav is not None:
            pnl = float(current_nav) - float(previous_nav)
        else:
            pnl = 0.0  # First day, no previous data
        
        return json.dumps({"pnl": pnl})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_daily_profit_loss_by_fund",
                "description": "Get daily profit/loss for a fund on a specific date",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Fund ID"},
                        "date": {"type": "string", "description": "Date in YYYY-MM-DD format"}
                    },
                    "required": ["fund_id", "date"]
                }
            }
        }
EOF

# Tool 8: GetFundValuation
cat > get_fund_valuation.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetFundValuation(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, date: str) -> str:
        nav_records = data.get("nav_records", {})
        funds = data.get("funds", {})
        
        # Find NAV record for the fund on the specified date
        nav_value = None
        nav_details = None
        
        for nav in nav_records.values():
            if nav.get("fund_id") == fund_id and nav.get("nav_date") == date:
                nav_value = nav.get("nav_value")
                nav_details = nav
                break
        
        if nav_value is None:
            raise ValueError(f"No NAV record found for fund {fund_id} on date {date}")
        
        # Get fund details
        fund_details = None
        for fund in funds.values():
            if fund.get("fund_id") == fund_id:
                fund_details = fund
                break
        
        result = {
            "valuation": float(nav_value),
            "fund_id": fund_id,
            "nav_details": nav_details
        }
        
        if fund_details:
            result["fund_details"] = fund_details
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_fund_valuation",
                "description": "Get fund valuation for a specific date",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Fund ID"},
                        "date": {"type": "string", "description": "Date in YYYY-MM-DD format"}
                    },
                    "required": ["fund_id", "date"]
                }
            }
        }
EOF

# Tool 9: RetrieveSubscriptions
cat > retrieve_subscriptions.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RetrieveSubscriptions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: Optional[str] = None, 
               fund_id: Optional[str] = None) -> str:
        subscriptions = data.get("subscriptions", {})
        results = []
        
        for subscription in subscriptions.values():
            if investor_id and subscription.get("investor_id") != investor_id:
                continue
            if fund_id and subscription.get("fund_id") != fund_id:
                continue
            results.append(subscription)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_subscriptions",
                "description": "Retrieve subscriptions with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "Investor ID"},
                        "fund_id": {"type": "string", "description": "Fund ID"}
                    },
                    "required": []
                }
            }
        }
EOF

# Tool 10: FindReports
cat > find_reports.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FindReports(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Dict[str, Any]) -> str:
        reports = data.get("reports", {})
        results = []
        
        for report in reports.values():
            # Apply filters
            skip_report = False
            for key, value in filters.items():
                if key in report and report.get(key) != value:
                    skip_report = True
                    break
            
            if not skip_report:
                results.append(report)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_reports",
                "description": "Find reports with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filters": {"type": "object", "description": "Filter criteria for reports"}
                    },
                    "required": ["filters"]
                }
            }
        }
EOF

# Tool 11: AddNewUser
cat > add_new_user.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddNewUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], first_name: str, last_name: str, email: str,
               role: str, timezone: str, status: str = "active") -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        
        # Validate role
        valid_roles = ["admin", "employee"]
        if role not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of {valid_roles}")
        
        # Validate status
        valid_statuses = ["active", "inactive", "suspended"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Check if email already exists
        for user in users.values():
            if user.get("email", "").lower() == email.lower():
                raise ValueError(f"User with email {email} already exists")
        
        user_id = generate_id(users)
        timestamp = "2025-10-01T00:00:00"
        
        new_user = {
            "user_id": str(user_id),
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "role": role,
            "timezone": timezone,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        users[str(user_id)] = new_user
        return json.dumps(new_user)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_new_user",
                "description": "Add a new user to the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "first_name": {"type": "string", "description": "User's first name"},
                        "last_name": {"type": "string", "description": "User's last name"},
                        "email": {"type": "string", "description": "User's email address"},
                        "role": {"type": "string", "description": "User role (admin, employee)"},
                        "timezone": {"type": "string", "description": "User's timezone"},
                        "status": {"type": "string", "description": "User status (active, inactive, suspended), defaults to active"}
                    },
                    "required": ["first_name", "last_name", "email", "role", "timezone"]
                }
            }
        }
EOF

# Tool 12: CreateNewFund
cat > create_new_fund.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateNewFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: str, fund_type: str, base_currency: str,
               manager_id: str, size: float, status: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        users = data.get("users", {})
        
        # Validate manager exists
        if str(manager_id) not in users:
            raise ValueError(f"Manager with ID {manager_id} not found")
        
        # Validate fund_type
        valid_fund_types = ["equity", "fixed_income", "multi_asset", "hedge"]
        if fund_type not in valid_fund_types:
            raise ValueError(f"Invalid fund type. Must be one of {valid_fund_types}")
        
        # Validate base_currency
        valid_currencies = ["USD", "EUR", "GBP", "NGN"]
        if base_currency not in valid_currencies:
            raise ValueError(f"Invalid base currency. Must be one of {valid_currencies}")
        
        # Validate status
        valid_statuses = ["open", "closed"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        fund_id = generate_id(funds)
        timestamp = "2025-10-01T00:00:00"
        
        new_fund = {
            "fund_id": str(fund_id),
            "name": name,
            "fund_type": fund_type,
            "base_currency": base_currency,
            "manager_id": str(manager_id),
            "size": size,
            "status": status,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        funds[str(fund_id)] = new_fund
        return json.dumps(new_fund)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_new_fund",
                "description": "Create a new fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Fund name"},
                        "fund_type": {"type": "string", "description": "Fund type (equity, fixed_income, multi_asset, hedge)"},
                        "base_currency": {"type": "string", "description": "Base currency (USD, EUR, GBP, NGN)"},
                        "manager_id": {"type": "string", "description": "Manager user ID"},
                        "size": {"type": "number", "description": "Fund size"},
                        "status": {"type": "string", "description": "Fund status (open, closed)"}
                    },
                    "required": ["name", "fund_type", "base_currency", "manager_id", "size", "status"]
                }
            }
        }
EOF

# Tool 13: AddNewTradeForFund
cat > add_new_trade_for_fund.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddNewTradeForFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, instrument_id: str,
               trade_date: str, quantity: float, price: float, side: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        trades = data.get("trades", {})
        funds = data.get("funds", {})
        instruments = data.get("instruments", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund with ID {fund_id} not found")
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            raise ValueError(f"Instrument with ID {instrument_id} not found")
        
        # Validate side
        valid_sides = ["buy", "sell"]
        if side not in valid_sides:
            raise ValueError(f"Invalid side. Must be one of {valid_sides}")
        
        trade_id = generate_id(trades)
        timestamp = "2025-10-01T00:00:00"
        
        new_trade = {
            "trade_id": str(trade_id),
            "fund_id": str(fund_id),
            "instrument_id": str(instrument_id),
            "trade_date": trade_date,
            "quantity": quantity,
            "price": price,
            "side": side,
            "status": "executed",
            "created_at": timestamp
        }
        
        trades[str(trade_id)] = new_trade
        return json.dumps(new_trade)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_new_trade_for_fund",
                "description": "Add a new trade for a fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Fund ID"},
                        "instrument_id": {"type": "string", "description": "Instrument ID"},
                        "trade_date": {"type": "string", "description": "Trade date in ISO format"},
                        "quantity": {"type": "number", "description": "Trade quantity"},
                        "price": {"type": "number", "description": "Trade price"},
                        "side": {"type": "string", "description": "Trade side (buy, sell)"}
                    },
                    "required": ["fund_id", "instrument_id", "trade_date", "quantity", "price", "side"]
                }
            }
        }
EOF

# Tool 14: AssignUserToHandleInvestorOrFund
cat > assign_user_to_handle_investor_or_fund.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AssignUserToHandleInvestorOrFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, investor_id: Optional[str] = None,
               fund_id: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        investors = data.get("investors", {})
        funds = data.get("funds", {})
        
        # Validate user exists
        if str(user_id) not in users:
            raise ValueError(f"User with ID {user_id} not found")
        
        if investor_id:
            # Validate investor exists
            if str(investor_id) not in investors:
                raise ValueError(f"Investor with ID {investor_id} not found")
            
            # Update investor's employee_id
            investors[str(investor_id)]["employee_id"] = str(user_id)
            return json.dumps(investors[str(investor_id)])
        
        elif fund_id:
            # Validate fund exists
            if str(fund_id) not in funds:
                raise ValueError(f"Fund with ID {fund_id} not found")
            
            # Update fund's manager_id
            funds[str(fund_id)]["manager_id"] = str(user_id)
            funds[str(fund_id)]["updated_at"] = "2025-10-01T00:00:00"
            return json.dumps(funds[str(fund_id)])
        
        else:
            raise ValueError("Either investor_id or fund_id must be provided")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "assign_user_to_handle_investor_or_fund",
                "description": "Assign a user to handle an investor or fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User ID to assign"},
                        "investor_id": {"type": "string", "description": "Investor ID (optional)"},
                        "fund_id": {"type": "string", "description": "Fund ID (optional)"}
                    },
                    "required": ["user_id"]
                }
            }
        }
EOF

# Tool 15: CreateNAVRecord
cat > create_nav_record.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateNAVRecord(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, nav_date: str, 
               nav_value: float, currency: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        nav_records = data.get("nav_records", {})
        funds = data.get("funds", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund with ID {fund_id} not found")
        
        # Validate currency
        valid_currencies = ["USD", "EUR", "GBP", "NGN"]
        if currency not in valid_currencies:
            raise ValueError(f"Invalid currency. Must be one of {valid_currencies}")
        
        nav_id = generate_id(nav_records)
        timestamp = "2025-10-01T00:00:00"
        
        new_nav = {
            "nav_id": str(nav_id),
            "fund_id": str(fund_id),
            "nav_date": nav_date,
            "nav_value": nav_value,
            "currency": currency,
            "updated_at": timestamp
        }
        
        nav_records[str(nav_id)] = new_nav
        return json.dumps(new_nav)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_nav_record",
                "description": "Create a new NAV record for a fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Fund ID"},
                        "nav_date": {"type": "string", "description": "NAV date in YYYY-MM-DD format"},
                        "nav_value": {"type": "number", "description": "NAV value"},
                        "currency": {"type": "string", "description": "Currency (USD, EUR, GBP, NGN)"}
                    },
                    "required": ["fund_id", "nav_date", "nav_value", "currency"]
                }
            }
        }
EOF

# Tool 16: UpdateNAVRecords
cat > update_nav_records.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateNAVRecords(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], nav_id: str, nav_value: float, currency: str) -> str:
        nav_records = data.get("nav_records", {})
        
        # Validate NAV record exists
        if str(nav_id) not in nav_records:
            raise ValueError(f"NAV record with ID {nav_id} not found")
        
        # Validate currency
        valid_currencies = ["USD", "EUR", "GBP", "NGN"]
        if currency not in valid_currencies:
            raise ValueError(f"Invalid currency. Must be one of {valid_currencies}")
        
        # Update NAV record
        nav_records[str(nav_id)]["nav_value"] = nav_value
        nav_records[str(nav_id)]["currency"] = currency
        nav_records[str(nav_id)]["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(nav_records[str(nav_id)])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_nav_records",
                "description": "Update an existing NAV record",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "nav_id": {"type": "string", "description": "NAV record ID"},
                        "nav_value": {"type": "number", "description": "New NAV value"},
                        "currency": {"type": "string", "description": "Currency (USD, EUR, GBP, NGN)"}
                    },
                    "required": ["nav_id", "nav_value", "currency"]
                }
            }
        }
EOF

# Tool 17: UpdateFundDetails
cat > update_fund_details.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateFundDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, name: str, fund_type: str,
               base_currency: str, size: float, status: str) -> str:
        funds = data.get("funds", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund with ID {fund_id} not found")
        
        # Validate fund_type
        valid_fund_types = ["equity", "fixed_income", "multi_asset", "hedge"]
        if fund_type not in valid_fund_types:
            raise ValueError(f"Invalid fund type. Must be one of {valid_fund_types}")
        
        # Validate base_currency
        valid_currencies = ["USD", "EUR", "GBP", "NGN"]
        if base_currency not in valid_currencies:
            raise ValueError(f"Invalid base currency. Must be one of {valid_currencies}")
        
        # Validate status
        valid_statuses = ["open", "closed"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Update fund details
        funds[str(fund_id)]["name"] = name
        funds[str(fund_id)]["fund_type"] = fund_type
        funds[str(fund_id)]["base_currency"] = base_currency
        funds[str(fund_id)]["size"] = size
        funds[str(fund_id)]["status"] = status
        funds[str(fund_id)]["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(funds[str(fund_id)])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_fund_details",
                "description": "Update fund details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Fund ID"},
                        "name": {"type": "string", "description": "Fund name"},
                        "fund_type": {"type": "string", "description": "Fund type (equity, fixed_income, multi_asset, hedge)"},
                        "base_currency": {"type": "string", "description": "Base currency (USD, EUR, GBP, NGN)"},
                        "size": {"type": "number", "description": "Fund size"},
                        "status": {"type": "string", "description": "Fund status (open, closed)"}
                    },
                    "required": ["fund_id", "name", "fund_type", "base_currency", "size", "status"]
                }
            }
        }
EOF

# Tool 18: UpdateInstrumentPrice
cat > update_instrument_price.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateInstrumentPrice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_id: str, price_date: str,
               open_price: float, high_price: float, low_price: float, 
               close_price: float) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        instrument_prices = data.get("instrument_prices", {})
        instruments = data.get("instruments", {})
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            raise ValueError(f"Instrument with ID {instrument_id} not found")
        
        # Check if price record exists for this instrument and date
        existing_price_id = None
        for price_id, price in instrument_prices.items():
            if (price.get("instrument_id") == str(instrument_id) and 
                price.get("price_date") == price_date):
                existing_price_id = price_id
                break
        
        if existing_price_id:
            # Update existing price record
            instrument_prices[existing_price_id]["open_price"] = open_price
            instrument_prices[existing_price_id]["high_price"] = high_price
            instrument_prices[existing_price_id]["low_price"] = low_price
            instrument_prices[existing_price_id]["close_price"] = close_price
            return json.dumps(instrument_prices[existing_price_id])
        else:
            # Create new price record
            price_id = generate_id(instrument_prices)
            new_price = {
                "price_id": str(price_id),
                "instrument_id": str(instrument_id),
                "price_date": price_date,
                "open_price": open_price,
                "high_price": high_price,
                "low_price": low_price,
                "close_price": close_price
            }
            instrument_prices[str(price_id)] = new_price
            return json.dumps(new_price)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_instrument_price",
                "description": "Update or create instrument price record",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {"type": "string", "description": "Instrument ID"},
                        "price_date": {"type": "string", "description": "Price date in YYYY-MM-DD format"},
                        "open_price": {"type": "number", "description": "Opening price"},
                        "high_price": {"type": "number", "description": "High price"},
                        "low_price": {"type": "number", "description": "Low price"},
                        "close_price": {"type": "number", "description": "Closing price"}
                    },
                    "required": ["instrument_id", "price_date", "open_price", "high_price", "low_price", "close_price"]
                }
            }
        }
EOF

# Tool 19: UpdateTradeForFund
cat > update_trade_for_fund.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateTradeForFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], trade_id: str, quantity: float, 
               price: float, status: str) -> str:
        trades = data.get("trades", {})
        
        # Validate trade exists
        if str(trade_id) not in trades:
            raise ValueError(f"Trade with ID {trade_id} not found")
        
        # Validate status
        valid_statuses = ["executed", "pending", "failed"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Update trade
        trades[str(trade_id)]["quantity"] = quantity
        trades[str(trade_id)]["price"] = price
        trades[str(trade_id)]["status"] = status
        
        return json.dumps(trades[str(trade_id)])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_trade_for_fund",
                "description": "Update an existing trade",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "trade_id": {"type": "string", "description": "Trade ID"},
                        "quantity": {"type": "number", "description": "Updated trade quantity"},
                        "price": {"type": "number", "description": "Updated trade price"},
                        "status": {"type": "string", "description": "Trade status (executed, pending, failed)"}
                    },
                    "required": ["trade_id", "quantity", "price", "status"]
                }
            }
        }
EOF

# Tool 20: NotifyUser
cat > notify_user.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class NotifyUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, email: str, 
               type: str, reference_id: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        notifications = data.get("notifications", {})
        users = data.get("users", {})
        
        # Validate user exists
        if str(user_id) not in users:
            raise ValueError(f"User with ID {user_id} not found")
        
        # Validate notification type
        valid_types = ["alert", "report", "reminder", "subscription_update"]
        if type not in valid_types:
            raise ValueError(f"Invalid type. Must be one of {valid_types}")
        
        notification_id = generate_id(notifications)
        timestamp = "2025-10-01T00:00:00"
        
        new_notification = {
            "notification_id": str(notification_id),
            "email": email,
            "type": type,
            "class": "funds",  # Default class, could be made configurable
            "reference_id": str(reference_id),
            "status": "pending",
            "sent_at": None,
            "created_at": timestamp
        }
        
        notifications[str(notification_id)] = new_notification
        return json.dumps(new_notification)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "notify_user",
                "description": "Create a notification for a user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User ID to notify"},
                        "email": {"type": "string", "description": "Email address for notification"},
                        "type": {"type": "string", "description": "Notification type (alert, report, reminder, subscription_update)"},
                        "reference_id": {"type": "string", "description": "Reference ID for the notification"}
                    },
                    "required": ["user_id", "email", "type", "reference_id"]
                }
            }
        }
EOF

echo "All 20 database tools have been created successfully!"
echo "Files created:"
echo "1. fetch_user_by_mail.py"
echo "2. retrieve_funds_with_filter.py"
echo "3. fetch_investors_with_portfolio_holdings.py"
echo "4. fetch_instruments_with_its_price.py"
echo "5. get_fund_trade_details.py"
echo "6. get_nav_records.py"
echo "7. get_daily_profit_loss_by_fund.py"
echo "8. get_fund_valuation.py"
echo "9. retrieve_subscriptions.py"
echo "10. find_reports.py"
echo "11. add_new_user.py"
echo "12. create_new_fund.py"
echo "13. add_new_trade_for_fund.py"
echo "14. assign_user_to_handle_investor_or_fund.py"
echo "15. create_nav_record.py"
echo "16. update_nav_records.py"
echo "17. update_fund_details.py"
echo "18. update_instrument_price.py"
echo "19. update_trade_for_fund.py"
echo "20. notify_user.py"