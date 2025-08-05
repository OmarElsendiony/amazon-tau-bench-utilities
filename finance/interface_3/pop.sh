#!/bin/bash

# Create directory for tools
mkdir -p financial_tools
cd financial_tools

# Read APIs (10 tools)

# 1. FindUser
cat > find_user.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class FindUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Optional[Dict[str, Any]] = None) -> str:
        users = data.get("users", {})
        results = []
        
        if filters is None:
            filters = {}
        
        for user in users.values():
            # Apply filters
            if filters.get("user_id") and str(user.get("user_id")) != str(filters["user_id"]):
                continue
            if filters.get("email") and user.get("email", "").lower() != filters["email"].lower():
                continue
            if filters.get("role") and user.get("role") != filters["role"]:
                continue
            if filters.get("status") and user.get("status") != filters["status"]:
                continue
            if filters.get("first_name") and filters["first_name"].lower() not in user.get("first_name", "").lower():
                continue
            if filters.get("last_name") and filters["last_name"].lower() not in user.get("last_name", "").lower():
                continue
                
            results.append(user)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_user",
                "description": "Find users with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to apply",
                            "properties": {
                                "user_id": {"type": "string", "description": "Filter by user ID"},
                                "email": {"type": "string", "description": "Filter by email address"},
                                "role": {"type": "string", "description": "Filter by role (admin, employee)"},
                                "status": {"type": "string", "description": "Filter by status (active, inactive, suspended)"},
                                "first_name": {"type": "string", "description": "Filter by first name (partial match)"},
                                "last_name": {"type": "string", "description": "Filter by last name (partial match)"}
                            }
                        }
                    },
                    "required": []
                }
            }
        }
EOF

# 2. GetFilteredInvestors
cat > get_filtered_investors.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetFilteredInvestors(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Optional[Dict[str, Any]] = None) -> str:
        investors = data.get("investors", {})
        results = []
        
        if filters is None:
            filters = {}
        
        for investor in investors.values():
            # Apply filters
            if filters.get("investor_id") and str(investor.get("investor_id")) != str(filters["investor_id"]):
                continue
            if filters.get("employee_id") and str(investor.get("employee_id")) != str(filters["employee_id"]):
                continue
            if filters.get("name") and filters["name"].lower() not in investor.get("name", "").lower():
                continue
            if filters.get("investor_type") and investor.get("investor_type") != filters["investor_type"]:
                continue
            if filters.get("contact_email") and investor.get("contact_email", "").lower() != filters["contact_email"].lower():
                continue
            if filters.get("accreditation_status") and investor.get("accreditation_status") != filters["accreditation_status"]:
                continue
                
            results.append(investor)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_filtered_investors",
                "description": "Get investors with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to apply",
                            "properties": {
                                "investor_id": {"type": "string", "description": "Filter by investor ID"},
                                "employee_id": {"type": "string", "description": "Filter by employee ID"},
                                "name": {"type": "string", "description": "Filter by name (partial match)"},
                                "investor_type": {"type": "string", "description": "Filter by investor type (organization, retail, high_net_worth)"},
                                "contact_email": {"type": "string", "description": "Filter by contact email"},
                                "accreditation_status": {"type": "string", "description": "Filter by accreditation status (accredited, non_accredited)"}
                            }
                        }
                    },
                    "required": []
                }
            }
        }
EOF

# 3. GetInvestorPortfolio
cat > get_investor_portfolio.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetInvestorPortfolio(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str) -> str:
        portfolios = data.get("portfolios", {})
        investors = data.get("investors", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Find portfolio for the investor
        for portfolio in portfolios.values():
            if str(portfolio.get("investor_id")) == str(investor_id):
                return json.dumps(portfolio)
        
        # Return empty result if no portfolio found
        return json.dumps({})

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

# 4. GetPortfolioHoldings
cat > get_portfolio_holdings.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPortfolioHoldings(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], portfolio_id: str) -> str:
        portfolios = data.get("portfolios", {})
        holdings = data.get("portfolio_holdings", {})
        
        # Validate portfolio exists
        if str(portfolio_id) not in portfolios:
            raise ValueError(f"Portfolio {portfolio_id} not found")
        
        results = []
        for holding in holdings.values():
            if str(holding.get("portfolio_id")) == str(portfolio_id):
                results.append(holding)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_portfolio_holdings",
                "description": "Get all holdings for a specific portfolio",
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

# 5. RetrieveInstruments
cat > retrieve_instruments.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RetrieveInstruments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Optional[Dict[str, Any]] = None) -> str:
        instruments = data.get("instruments", {})
        results = []
        
        if filters is None:
            filters = {}
        
        for instrument in instruments.values():
            # Apply filters
            if filters.get("instrument_id") and str(instrument.get("instrument_id")) != str(filters["instrument_id"]):
                continue
            if filters.get("ticker") and instrument.get("ticker", "").upper() != filters["ticker"].upper():
                continue
            if filters.get("name") and filters["name"].lower() not in instrument.get("name", "").lower():
                continue
            if filters.get("instrument_type") and instrument.get("instrument_type") != filters["instrument_type"]:
                continue
                
            results.append(instrument)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_instruments",
                "description": "Retrieve instruments with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to apply",
                            "properties": {
                                "instrument_id": {"type": "string", "description": "Filter by instrument ID"},
                                "ticker": {"type": "string", "description": "Filter by ticker symbol"},
                                "name": {"type": "string", "description": "Filter by name (partial match)"},
                                "instrument_type": {"type": "string", "description": "Filter by instrument type (stock, bond, derivative, cash, other)"}
                            }
                        }
                    },
                    "required": []
                }
            }
        }
EOF

# 6. RetrieveInstrumentPrices
cat > retrieve_instrument_prices.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool
from datetime import datetime

class RetrieveInstrumentPrices(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_id: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        instruments = data.get("instruments", {})
        prices = data.get("instrument_prices", {})
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            raise ValueError(f"Instrument {instrument_id} not found")
        
        results = []
        for price in prices.values():
            if str(price.get("instrument_id")) != str(instrument_id):
                continue
                
            price_date = price.get("price_date")
            if price_date:
                # Filter by date range if provided
                if start_date and price_date < start_date:
                    continue
                if end_date and price_date > end_date:
                    continue
                    
            results.append(price)
        
        # Sort by date
        results.sort(key=lambda x: x.get("price_date", ""))
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_instrument_prices",
                "description": "Retrieve price history for a specific instrument",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {"type": "string", "description": "ID of the instrument"},
                        "start_date": {"type": "string", "description": "Start date for price range (YYYY-MM-DD format)"},
                        "end_date": {"type": "string", "description": "End date for price range (YYYY-MM-DD format)"}
                    },
                    "required": ["instrument_id"]
                }
            }
        }
EOF

# 7. SummaryOfInstrumentTypesByPrices
cat > summary_of_instrument_types_by_prices.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SummaryOfInstrumentTypesByPrices(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], date: str) -> str:
        instruments = data.get("instruments", {})
        prices = data.get("instrument_prices", {})
        
        # Group instruments by type
        instrument_types = {}
        for instrument in instruments.values():
            inst_type = instrument.get("instrument_type")
            if inst_type not in instrument_types:
                instrument_types[inst_type] = []
            instrument_types[inst_type].append(instrument.get("instrument_id"))
        
        # Find prices for the specific date
        date_prices = {}
        for price in prices.values():
            if price.get("price_date") == date:
                date_prices[str(price.get("instrument_id"))] = price
        
        # Create summary
        results = []
        for inst_type, instrument_ids in instrument_types.items():
            total_instruments = len(instrument_ids)
            instruments_with_prices = 0
            total_close_value = 0.0
            avg_close_price = 0.0
            
            for inst_id in instrument_ids:
                if str(inst_id) in date_prices:
                    instruments_with_prices += 1
                    total_close_value += float(date_prices[str(inst_id)].get("close_price", 0))
            
            if instruments_with_prices > 0:
                avg_close_price = total_close_value / instruments_with_prices
            
            summary = {
                "instrument_type": inst_type,
                "total_instruments": total_instruments,
                "instruments_with_prices": instruments_with_prices,
                "average_close_price": round(avg_close_price, 4),
                "total_close_value": round(total_close_value, 2),
                "date": date
            }
            results.append(summary)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "summary_of_instrument_types_by_prices",
                "description": "Get summary of instrument types with pricing data for a specific date",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date": {"type": "string", "description": "Date for price summary (YYYY-MM-DD format)"}
                    },
                    "required": ["date"]
                }
            }
        }
EOF

# 8. RetrieveReports
cat > retrieve_reports.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RetrieveReports(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: Optional[str] = None, investor_id: Optional[str] = None, report_type: Optional[str] = None) -> str:
        reports = data.get("reports", {})
        results = []
        
        for report in reports.values():
            # Apply filters
            if fund_id and str(report.get("fund_id")) != str(fund_id):
                continue
            if investor_id and str(report.get("investor_id")) != str(investor_id):
                continue
            if report_type and report.get("report_type") != report_type:
                continue
                
            results.append(report)
        
        # Sort by report date (newest first)
        results.sort(key=lambda x: x.get("report_date", ""), reverse=True)
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_reports",
                "description": "Retrieve reports with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "report_type": {"type": "string", "description": "Filter by report type (performance, holding, financial)"}
                    },
                    "required": []
                }
            }
        }
EOF

# 9. GetNotifications
cat > get_notifications.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetNotifications(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], recipient_id: Optional[str] = None, status: Optional[str] = None) -> str:
        notifications = data.get("notifications", {})
        users = data.get("users", {})
        results = []
        
        for notification in notifications.values():
            # Apply filters
            if recipient_id:
                # Find user by ID to get email
                user_email = None
                for user in users.values():
                    if str(user.get("user_id")) == str(recipient_id):
                        user_email = user.get("email")
                        break
                
                if not user_email or notification.get("email") != user_email:
                    continue
                    
            if status and notification.get("status") != status:
                continue
                
            results.append(notification)
        
        # Sort by created date (newest first)
        results.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_notifications",
                "description": "Get notifications with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "recipient_id": {"type": "string", "description": "Filter by recipient user ID"},
                        "status": {"type": "string", "description": "Filter by status (pending, sent, failed)"}
                    },
                    "required": []
                }
            }
        }
EOF

# 10. FetchInvoices
cat > fetch_invoices.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class FetchInvoices(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: Optional[str] = None, investor_id: Optional[str] = None, status: Optional[str] = None) -> str:
        invoices = data.get("invoices", {})
        results = []
        
        for invoice in invoices.values():
            # Apply filters
            if fund_id and str(invoice.get("fund_id")) != str(fund_id):
                continue
            if investor_id and str(invoice.get("investor_id")) != str(investor_id):
                continue
            if status and invoice.get("status") != status:
                continue
                
            results.append(invoice)
        
        # Sort by invoice date (newest first)
        results.sort(key=lambda x: x.get("invoice_date", ""), reverse=True)
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_invoices",
                "description": "Fetch invoices with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "status": {"type": "string", "description": "Filter by status (issued, paid)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Write APIs (10 tools)

# 11. AddNewInstrument
cat > add_new_instrument.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddNewInstrument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], ticker: str, name: str, instrument_type: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        instruments = data.get("instruments", {})
        
        # Validate instrument type
        valid_types = ["stock", "bond", "derivative", "cash", "other"]
        if instrument_type not in valid_types:
            raise ValueError(f"Invalid instrument type. Must be one of {valid_types}")
        
        # Check if ticker already exists
        for instrument in instruments.values():
            if instrument.get("ticker", "").upper() == ticker.upper():
                raise ValueError(f"Instrument with ticker {ticker} already exists")
        
        instrument_id = generate_id(instruments)
        
        new_instrument = {
            "instrument_id": instrument_id,
            "ticker": ticker.upper(),
            "name": name,
            "instrument_type": instrument_type
        }
        
        instruments[str(instrument_id)] = new_instrument
        return json.dumps(new_instrument)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_new_instrument",
                "description": "Add a new financial instrument",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {"type": "string", "description": "Ticker symbol of the instrument"},
                        "name": {"type": "string", "description": "Name of the instrument"},
                        "instrument_type": {"type": "string", "description": "Type of instrument (stock, bond, derivative, cash, other)"}
                    },
                    "required": ["ticker", "name", "instrument_type"]
                }
            }
        }
EOF

# 12. AddNewInstrumentPrice
cat > add_new_instrument_price.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddNewInstrumentPrice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_id: str, price_date: str, 
               open_price: float, high_price: float, low_price: float, close_price: float) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        instruments = data.get("instruments", {})
        prices = data.get("instrument_prices", {})
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            raise ValueError(f"Instrument {instrument_id} not found")
        
        # Validate price logic
        if high_price < max(open_price, close_price, low_price):
            raise ValueError("High price must be >= open, close, and low prices")
        if low_price > min(open_price, close_price, high_price):
            raise ValueError("Low price must be <= open, close, and high prices")
        
        # Check if price already exists for this instrument and date
        for price in prices.values():
            if (str(price.get("instrument_id")) == str(instrument_id) and 
                price.get("price_date") == price_date):
                raise ValueError(f"Price already exists for instrument {instrument_id} on {price_date}")
        
        price_id = generate_id(prices)
        
        new_price = {
            "price_id": price_id,
            "instrument_id": instrument_id,
            "price_date": price_date,
            "open_price": open_price,
            "high_price": high_price,
            "low_price": low_price,
            "close_price": close_price
        }
        
        prices[str(price_id)] = new_price
        return json.dumps(new_price)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_new_instrument_price",
                "description": "Add new price data for an instrument",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {"type": "string", "description": "ID of the instrument"},
                        "price_date": {"type": "string", "description": "Date of the price data (YYYY-MM-DD)"},
                        "open_price": {"type": "number", "description": "Opening price"},
                        "high_price": {"type": "number", "description": "Highest price"},
                        "low_price": {"type": "number", "description": "Lowest price"},
                        "close_price": {"type": "number", "description": "Closing price"}
                    },
                    "required": ["instrument_id", "price_date", "open_price", "high_price", "low_price", "close_price"]
                }
            }
        }
EOF

# 13. GenerateReport
cat > generate_report.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GenerateReport(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, investor_id: str, report_date: str, 
               report_type: str, generated_by: str, export_period_end: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        users = data.get("users", {})
        reports = data.get("reports", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Validate user exists
        if str(generated_by) not in users:
            raise ValueError(f"User {generated_by} not found")
        
        # Validate report type
        valid_types = ["performance", "holding", "financial"]
        if report_type not in valid_types:
            raise ValueError(f"Invalid report type. Must be one of {valid_types}")
        
        report_id = generate_id(reports)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_report = {
            "report_id": report_id,
            "fund_id": fund_id,
            "investor_id": investor_id,
            "report_date": report_date,
            "report_type": report_type,
            "generated_by": generated_by,
            "status": "pending",
            "created_at": timestamp,
            "export_period_end": export_period_end
        }
        
        reports[str(report_id)] = new_report
        return json.dumps(new_report)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "generate_report",
                "description": "Generate a new report for a fund and investor",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "report_date": {"type": "string", "description": "Date of the report (YYYY-MM-DD)"},
                        "report_type": {"type": "string", "description": "Type of report (performance, holding, financial)"},
                        "generated_by": {"type": "string", "description": "ID of the user generating the report"},
                        "export_period_end": {"type": "string", "description": "End date of the export period (YYYY-MM-DD)"}
                    },
                    "required": ["fund_id", "investor_id", "report_date", "report_type", "generated_by", "export_period_end"]
                }
            }
        }
EOF

# Create directory for tools if it doesn't exist
mkdir -p db_tools

# Create AddNewHolding tool
cat > db_tools/add_new_holding.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class AddNewHolding(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], portfolio_id: str, instrument_id: str, 
               quantity: str, cost_basis: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        portfolios = data.get("portfolios", {})
        instruments = data.get("instruments", {})
        holdings = data.get("portfolio_holdings", {})
        
        # Validate portfolio exists
        if str(portfolio_id) not in portfolios:
            raise ValueError(f"Portfolio {portfolio_id} not found")
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            raise ValueError(f"Instrument {instrument_id} not found")
        
        holding_id = generate_id(holdings)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_holding = {
            "holding_id": holding_id,
            "portfolio_id": portfolio_id,
            "instrument_id": instrument_id,
            "quantity": quantity,
            "cost_basis": cost_basis,
            "created_at": timestamp
        }
        
        holdings[str(holding_id)] = new_holding
        return json.dumps(new_holding)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_new_holding",
                "description": "Add a new holding to a portfolio",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "portfolio_id": {"type": "string", "description": "ID of the portfolio"},
                        "instrument_id": {"type": "string", "description": "ID of the instrument"},
                        "quantity": {"type": "string", "description": "Quantity of the holding"},
                        "cost_basis": {"type": "string", "description": "Cost basis of the holding"}
                    },
                    "required": ["portfolio_id", "instrument_id", "quantity", "cost_basis"]
                }
            }
        }
EOF

# Create DeleteHolding tool
cat > db_tools/delete_holding.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class DeleteHolding(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], holding_id: str) -> str:
        holdings = data.get("portfolio_holdings", {})
        
        # Validate holding exists
        if str(holding_id) not in holdings:
            raise ValueError(f"Holding {holding_id} not found")
        
        deleted_holding = holdings[str(holding_id)]
        del holdings[str(holding_id)]
        
        return json.dumps(deleted_holding)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_holding",
                "description": "Delete a holding from a portfolio",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "holding_id": {"type": "string", "description": "ID of the holding to delete"}
                    },
                    "required": ["holding_id"]
                }
            }
        }
EOF

# Create AddPayment tool
cat > db_tools/add_payment.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class AddPayment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: str, payment_date: str, 
               amount: str, payment_method: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        invoices = data.get("invoices", {})
        payments = data.get("payments", {})
        
        # Validate invoice exists
        if str(invoice_id) not in invoices:
            raise ValueError(f"Invoice {invoice_id} not found")
        
        # Validate payment method
        valid_methods = ["wire", "cheque", "credit_card", "bank_transfer"]
        if payment_method not in valid_methods:
            raise ValueError(f"Invalid payment method. Must be one of {valid_methods}")
        
        payment_id = generate_id(payments)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_payment = {
            "payment_id": payment_id,
            "invoice_id": invoice_id,
            "payment_date": payment_date,
            "amount": amount,
            "payment_method": payment_method,
            "status": "completed",
            "created_at": timestamp
        }
        
        payments[str(payment_id)] = new_payment
        return json.dumps(new_payment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_payment",
                "description": "Add a payment for an invoice",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string", "description": "ID of the invoice"},
                        "payment_date": {"type": "string", "description": "Payment date in ISO format"},
                        "amount": {"type": "string", "description": "Payment amount"},
                        "payment_method": {"type": "string", "description": "Payment method (wire, cheque, credit_card, bank_transfer)"}
                    },
                    "required": ["invoice_id", "payment_date", "amount", "payment_method"]
                }
            }
        }
EOF

# Create UpdateInstrument tool
cat > db_tools/update_instrument.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class UpdateInstrument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_id: str, ticker: Optional[str] = None, 
               name: Optional[str] = None, instrument_type: Optional[str] = None) -> str:
        instruments = data.get("instruments", {})
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            raise ValueError(f"Instrument {instrument_id} not found")
        
        # Validate instrument type if provided
        if instrument_type:
            valid_types = ["stock", "bond", "derivative", "cash", "other"]
            if instrument_type not in valid_types:
                raise ValueError(f"Invalid instrument type. Must be one of {valid_types}")
        
        instrument = instruments[str(instrument_id)]
        
        # Update fields if provided
        if ticker is not None:
            instrument["ticker"] = ticker
        if name is not None:
            instrument["name"] = name
        if instrument_type is not None:
            instrument["instrument_type"] = instrument_type
        
        return json.dumps(instrument)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_instrument",
                "description": "Update an instrument's information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {"type": "string", "description": "ID of the instrument"},
                        "ticker": {"type": "string", "description": "Instrument ticker symbol"},
                        "name": {"type": "string", "description": "Instrument name"},
                        "instrument_type": {"type": "string", "description": "Type of instrument (stock, bond, derivative, cash, other)"}
                    },
                    "required": ["instrument_id"]
                }
            }
        }
EOF

# Create UpdateInstrumentPrice tool
cat > db_tools/update_instrument_price.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class UpdateInstrumentPrice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], price_id: str, open_price: Optional[str] = None, 
               high_price: Optional[str] = None, low_price: Optional[str] = None, 
               close_price: Optional[str] = None) -> str:
        prices = data.get("instrument_prices", {})
        
        # Validate price record exists
        if str(price_id) not in prices:
            raise ValueError(f"Price record {price_id} not found")
        
        price_record = prices[str(price_id)]
        
        # Update fields if provided
        if open_price is not None:
            price_record["open_price"] = open_price
        if high_price is not None:
            price_record["high_price"] = high_price
        if low_price is not None:
            price_record["low_price"] = low_price
        if close_price is not None:
            price_record["close_price"] = close_price
        
        return json.dumps(price_record)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_instrument_price",
                "description": "Update instrument price information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "price_id": {"type": "string", "description": "ID of the price record"},
                        "open_price": {"type": "string", "description": "Opening price"},
                        "high_price": {"type": "string", "description": "High price"},
                        "low_price": {"type": "string", "description": "Low price"},
                        "close_price": {"type": "string", "description": "Closing price"}
                    },
                    "required": ["price_id"]
                }
            }
        }
EOF

# Create UpdateReport tool
cat > db_tools/update_report.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class UpdateReport(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], report_id: str, status: str) -> str:
        reports = data.get("reports", {})
        
        # Validate report exists
        if str(report_id) not in reports:
            raise ValueError(f"Report {report_id} not found")
        
        # Validate status
        valid_statuses = ["pending", "completed", "failed"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        report = reports[str(report_id)]
        report["status"] = status
        report["updated_at"] = "2025-10-01T00:00:00ZZ"
        
        return json.dumps(report)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_report",
                "description": "Update a report's status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "report_id": {"type": "string", "description": "ID of the report"},
                        "status": {"type": "string", "description": "Report status (pending, completed, failed)"}
                    },
                    "required": ["report_id", "status"]
                }
            }
        }
EOF

# Create EmailUser tool
cat > db_tools/email_user.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class EmailUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, class_: str, reference_id: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        notifications = data.get("notifications", {})
        
        # Validate user exists
        if str(user_id) not in users:
            raise ValueError(f"User {user_id} not found")
        
        # Validate class
        valid_classes = ["funds", "investors", "portfolios", "trades", "invoices", 
                        "reports", "documents", "subscriptions", "commitments"]
        if class_ not in valid_classes:
            raise ValueError(f"Invalid class. Must be one of {valid_classes}")
        
        user = users[str(user_id)]
        user_email = user.get("email")
        
        notification_id = generate_id(notifications)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_notification = {
            "notification_id": notification_id,
            "email": user_email,
            "type": "alert",
            "class": class_,
            "reference_id": reference_id,
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
                "name": "email_user",
                "description": "Send an email notification to a user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user to email"},
                        "class": {"type": "string", "description": "Class of notification (funds, investors, portfolios, trades, invoices, reports, documents, subscriptions, commitments)"},
                        "reference_id": {"type": "string", "description": "Reference ID for the notification"}
                    },
                    "required": ["user_id", "class", "reference_id"]
                }
            }
        }
EOF

echo "All database tools have been created successfully!"
echo "Files created:"
echo "- db_tools/add_new_holding.py"
echo "- db_tools/delete_holding.py"
echo "- db_tools/add_payment.py"
echo "- db_tools/update_instrument.py"
echo "- db_tools/update_instrument_price.py"
echo "- db_tools/update_report.py"
echo "- db_tools/email_user.py"