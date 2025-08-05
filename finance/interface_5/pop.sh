#!/bin/bash

# Create directory for tools if it doesn't exist
mkdir -p db_tools

# Read APIs (10 tools)

# 1. GetUserInformation
cat > db_tools/get_user_information.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetUserInformation(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str) -> str:
        users = data.get("users", {})
        
        if str(user_id) not in users:
            raise ValueError(f"User {user_id} not found")
        
        user = users[str(user_id)]
        return json.dumps(user)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_information",
                "description": "Retrieve information for a specific user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user to retrieve"}
                    },
                    "required": ["user_id"]
                }
            }
        }
EOF

# 2. ListFundsWithFilter
cat > db_tools/list_funds_with_filter.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ListFundsWithFilter(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: Optional[str] = None, 
               name: Optional[str] = None, fund_type: Optional[str] = None,
               base_currency: Optional[str] = None, status: Optional[str] = None) -> str:
        funds = data.get("funds", {})
        results = []
        
        for fund in funds.values():
            if fund_id and fund.get("fund_id") != fund_id:
                continue
            if name and name.lower() not in fund.get("name", "").lower():
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
                "name": "list_funds_with_filter",
                "description": "List funds with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "name": {"type": "string", "description": "Filter by fund name (partial match)"},
                        "fund_type": {"type": "string", "description": "Filter by fund type (equity, fixed_income, multi_asset, hedge)"},
                        "base_currency": {"type": "string", "description": "Filter by base currency (USD, EUR, GBP, NGN)"},
                        "status": {"type": "string", "description": "Filter by status (open, closed)"}
                    },
                    "required": []
                }
            }
        }
EOF

# 3. RetrieveInvestorWithSubscriptions
cat > db_tools/retrieve_investor_with_subscriptions.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RetrieveInvestorWithSubscriptions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: Optional[str] = None,
               subscription_id: Optional[str] = None, name: Optional[str] = None,
               contact_email: Optional[str] = None, employee_id: Optional[str] = None) -> str:
        investors = data.get("investors", {})
        subscriptions = data.get("subscriptions", {})
        
        # Find matching investors
        matching_investors = []
        for investor in investors.values():
            if investor_id and investor.get("investor_id") != investor_id:
                continue
            if name and name.lower() not in investor.get("name", "").lower():
                continue
            if contact_email and investor.get("contact_email") != contact_email:
                continue
            if employee_id and investor.get("employee_id") != employee_id:
                continue
            matching_investors.append(investor)
        
        # Add subscriptions to each matching investor
        results = []
        for investor in matching_investors:
            investor_with_subs = investor.copy()
            investor_subs = []
            
            for subscription in subscriptions.values():
                if subscription.get("investor_id") == investor.get("investor_id"):
                    if subscription_id and subscription.get("subscription_id") != subscription_id:
                        continue
                    investor_subs.append(subscription)
            
            investor_with_subs["subscriptions"] = investor_subs
            results.append(investor_with_subs)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_investor_with_subscriptions",
                "description": "Retrieve investors with their subscriptions using various filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "subscription_id": {"type": "string", "description": "Filter by subscription ID"},
                        "name": {"type": "string", "description": "Filter by investor name (partial match)"},
                        "contact_email": {"type": "string", "description": "Filter by contact email"},
                        "employee_id": {"type": "string", "description": "Filter by employee ID"}
                    },
                    "required": []
                }
            }
        }
EOF

# 4. ListCommitments
cat > db_tools/list_commitments.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ListCommitments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_id: Optional[str] = None,
               investor_id: Optional[str] = None, fund_id: Optional[str] = None,
               amount: Optional[str] = None, commitment_date: Optional[str] = None) -> str:
        commitments = data.get("commitments", {})
        results = []
        
        for commitment in commitments.values():
            if commitment_id and commitment.get("commitment_id") != commitment_id:
                continue
            if investor_id and commitment.get("investor_id") != investor_id:
                continue
            if fund_id and commitment.get("fund_id") != fund_id:
                continue
            if amount and str(commitment.get("commitment_amount")) != str(amount):
                continue
            if commitment_date and commitment.get("commitment_date") != commitment_date:
                continue
            results.append(commitment)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_commitments",
                "description": "List commitments with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {"type": "string", "description": "Filter by commitment ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "amount": {"type": "string", "description": "Filter by commitment amount"},
                        "commitment_date": {"type": "string", "description": "Filter by commitment date"}
                    },
                    "required": []
                }
            }
        }
EOF

# 5. RetrieveInvoices
cat > db_tools/retrieve_invoices.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RetrieveInvoices(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: Optional[str] = None,
               fund_id: Optional[str] = None, status: Optional[str] = None) -> str:
        invoices = data.get("invoices", {})
        results = []
        
        for invoice in invoices.values():
            if investor_id and invoice.get("investor_id") != investor_id:
                continue
            if fund_id and invoice.get("fund_id") != fund_id:
                continue
            if status and invoice.get("status") != status:
                continue
            results.append(invoice)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_invoices",
                "description": "Retrieve invoices with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "status": {"type": "string", "description": "Filter by status (issued, paid)"}
                    },
                    "required": []
                }
            }
        }
EOF

# 6. GetPaymentHistory
cat > db_tools/get_payment_history.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetPaymentHistory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: Optional[str] = None,
               investor_id: Optional[str] = None, fund_id: Optional[str] = None) -> str:
        payments = data.get("payments", {})
        invoices = data.get("invoices", {})
        results = []
        
        # Get relevant invoice IDs based on filters
        relevant_invoice_ids = set()
        
        if invoice_id:
            relevant_invoice_ids.add(invoice_id)
        else:
            for invoice in invoices.values():
                if investor_id and invoice.get("investor_id") != investor_id:
                    continue
                if fund_id and invoice.get("fund_id") != fund_id:
                    continue
                relevant_invoice_ids.add(invoice.get("invoice_id"))
        
        # Filter payments by relevant invoices
        for payment in payments.values():
            if payment.get("invoice_id") in relevant_invoice_ids:
                results.append(payment)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_payment_history",
                "description": "Get payment history with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string", "description": "Filter by invoice ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "fund_id": {"type": "string", "description": "Filter by fund ID"}
                    },
                    "required": []
                }
            }
        }
EOF

# 7. GetTickets
cat > db_tools/get_tickets.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetTickets(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], ticket_id: Optional[str] = None,
               invoice_id: Optional[str] = None, type: Optional[str] = None,
               status: Optional[str] = None) -> str:
        tickets = data.get("tickets", {})
        results = []
        
        for ticket in tickets.values():
            if ticket_id and ticket.get("ticket_id") != ticket_id:
                continue
            if invoice_id and ticket.get("invoice_id") != invoice_id:
                continue
            if type and ticket.get("type") != type:
                continue
            if status and ticket.get("status") != status:
                continue
            results.append(ticket)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_tickets",
                "description": "Get tickets with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticket_id": {"type": "string", "description": "Filter by ticket ID"},
                        "invoice_id": {"type": "string", "description": "Filter by invoice ID"},
                        "type": {"type": "string", "description": "Filter by type (missing_payment, overpayment, underpayment, mismatched_amount, invoice_duplicate, manual_follow_up)"},
                        "status": {"type": "string", "description": "Filter by status (open, in_review, resolved, closed)"}
                    },
                    "required": []
                }
            }
        }
EOF

# 8. GetReports
cat > db_tools/get_reports.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetReports(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: Optional[str] = None,
               investor_id: Optional[str] = None, report_type: Optional[str] = None,
               report_date: Optional[str] = None) -> str:
        reports = data.get("reports", {})
        results = []
        
        for report in reports.values():
            if fund_id and report.get("fund_id") != fund_id:
                continue
            if investor_id and report.get("investor_id") != investor_id:
                continue
            if report_type and report.get("report_type") != report_type:
                continue
            if report_date and report.get("report_date") != report_date:
                continue
            results.append(report)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_reports",
                "description": "Get reports with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "report_type": {"type": "string", "description": "Filter by report type (performance, holding, financial)"},
                        "report_date": {"type": "string", "description": "Filter by report date"}
                    },
                    "required": []
                }
            }
        }
EOF

# 9. FetchInvestorPortfolio
cat > db_tools/fetch_investor_portfolio.py << 'EOF'
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
EOF

# 10. RetrieveNotifications
cat > db_tools/retrieve_notifications.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RetrieveNotifications(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Dict[str, Any]) -> str:
        notifications = data.get("notifications", {})
        results = []
        
        for notification in notifications.values():
            match = True
            
            for key, value in filters.items():
                if key in notification and notification[key] != value:
                    match = False
                    break
            
            if match:
                results.append(notification)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_notifications",
                "description": "Retrieve notifications with filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filters": {
                            "type": "object",
                            "description": "Dictionary of filters to apply (email, type, class, reference_id, status)",
                            "properties": {
                                "email": {"type": "string", "description": "Filter by email"},
                                "type": {"type": "string", "description": "Filter by type (alert, report, reminder, subscription_update)"},
                                "class": {"type": "string", "description": "Filter by class (funds, investors, portfolios, trades, invoices, reports, documents, subscriptions, commitments)"},
                                "reference_id": {"type": "string", "description": "Filter by reference ID"},
                                "status": {"type": "string", "description": "Filter by status (pending, sent, failed)"}
                            }
                        }
                    },
                    "required": ["filters"]
                }
            }
        }
EOF

# Write APIs (10 tools)

# 11. CreateFund
cat > db_tools/create_fund.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: str, fund_type: str, base_currency: str,
               manager_id: str, size: str, status: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        users = data.get("users", {})
        
        # Validate manager exists
        if str(manager_id) not in users:
            raise ValueError(f"Manager {manager_id} not found")
        
        # Validate fund_type
        valid_fund_types = ["equity", "fixed_income", "multi_asset", "hedge"]
        if fund_type not in valid_fund_types:
            raise ValueError(f"Invalid fund_type. Must be one of {valid_fund_types}")
        
        # Validate base_currency
        valid_currencies = ["USD", "EUR", "GBP", "NGN"]
        if base_currency not in valid_currencies:
            raise ValueError(f"Invalid base_currency. Must be one of {valid_currencies}")
        
        # Validate status
        valid_statuses = ["open", "closed"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        fund_id = generate_id(funds)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_fund = {
            "fund_id": str(fund_id),
            "name": name,
            "fund_type": fund_type,
            "base_currency": base_currency,
            "manager_id": manager_id,
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
                "name": "create_fund",
                "description": "Create a new fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Fund name"},
                        "fund_type": {"type": "string", "description": "Fund type (equity, fixed_income, multi_asset, hedge)"},
                        "base_currency": {"type": "string", "description": "Base currency (USD, EUR, GBP, NGN)"},
                        "manager_id": {"type": "string", "description": "ID of the fund manager"},
                        "size": {"type": "string", "description": "Fund size"},
                        "status": {"type": "string", "description": "Fund status (open, closed)"}
                    },
                    "required": ["name", "fund_type", "base_currency", "manager_id", "size", "status"]
                }
            }
        }
EOF

# 12. RecordPayment
cat > db_tools/record_payment.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RecordPayment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: str, payment_date: str,
               amount: str, payment_method: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        payments = data.get("payments", {})
        invoices = data.get("invoices", {})
        
        # Validate invoice exists
        if str(invoice_id) not in invoices:
            raise ValueError(f"Invoice {invoice_id} not found")
        
        # Validate payment_method
        valid_methods = ["wire", "cheque", "credit_card", "bank_transfer"]
        if payment_method not in valid_methods:
            raise ValueError(f"Invalid payment_method. Must be one of {valid_methods}")
        
        payment_id = generate_id(payments)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_payment = {
            "payment_id": str(payment_id),
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
                "name": "record_payment",
                "description": "Record a new payment for an invoice",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string", "description": "ID of the invoice"},
                        "payment_date": {"type": "string", "description": "Payment date"},
                        "amount": {"type": "string", "description": "Payment amount"},
                        "payment_method": {"type": "string", "description": "Payment method (wire, cheque, credit_card, bank_transfer)"}
                    },
                    "required": ["invoice_id", "payment_date", "amount", "payment_method"]
                }
            }
        }
EOF

# 13. CreateInvestor
cat > db_tools/create_investor.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateInvestor(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: str, employee_id: str,
               investor_type: str, contact_email: str, accreditation_status: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        investors = data.get("investors", {})
        users = data.get("users", {})
        
        # Validate employee exists
        if str(employee_id) not in users:
            raise ValueError(f"Employee {employee_id} not found")
        
        # Validate investor_type
        valid_types = ["organization", "retail", "high_net_worth"]
        if investor_type not in valid_types:
            raise ValueError(f"Invalid investor_type. Must be one of {valid_types}")
        
        # Validate accreditation_status
        valid_statuses = ["accredited", "non_accredited"]
        if accreditation_status not in valid_statuses:
            raise ValueError(f"Invalid accreditation_status. Must be one of {valid_statuses}")
        
        investor_id = generate_id(investors)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_investor = {
            "investor_id": str(investor_id),
            "employee_id": employee_id,
            "name": name,
            "investor_type": investor_type,
            "contact_email": contact_email,
            "accreditation_status": accreditation_status,
            "created_at": timestamp
        }
        
        investors[str(investor_id)] = new_investor
        return json.dumps(new_investor)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_investor",
                "description": "Create a new investor",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Investor name"},
                        "employee_id": {"type": "string", "description": "ID of the managing employee"},
                        "investor_type": {"type": "string", "description": "Investor type (organization, retail, high_net_worth)"},
                        "contact_email": {"type": "string", "description": "Contact email"},
                        "accreditation_status": {"type": "string", "description": "Accreditation status (accredited, non_accredited)"}
                    },
                    "required": ["name", "employee_id", "investor_type", "contact_email", "accreditation_status"]
                }
            }
        }
EOF

# 14. CreateInvoice
cat > db_tools/create_invoice.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateInvoice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, investor_id: str,
               commitment_id: Optional[str], invoice_date: str, due_date: str,
               amount: str, currency: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        invoices = data.get("invoices", {})
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        commitments = data.get("commitments", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Validate commitment if provided
        if commitment_id and str(commitment_id) not in commitments:
            raise ValueError(f"Commitment {commitment_id} not found")
        
        # Validate currency
        valid_currencies = ["USD", "EUR", "GBP", "NGN"]
        if currency not in valid_currencies:
            raise ValueError(f"Invalid currency. Must be one of {valid_currencies}")
        
        invoice_id = generate_id(invoices)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_invoice = {
            "invoice_id": str(invoice_id),
            "fund_id": fund_id,
            "investor_id": investor_id,
            "commitment_id": commitment_id,
            "invoice_date": invoice_date,
            "due_date": due_date,
            "amount": amount,
            "payment_type": "manual",
            "currency": currency,
            "status": "issued",
            "updated_at": timestamp
        }
        
        invoices[str(invoice_id)] = new_invoice
        return json.dumps(new_invoice)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_invoice",
                "description": "Create a new invoice",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "commitment_id": {"type": "string", "description": "ID of the commitment (optional)"},
                        "invoice_date": {"type": "string", "description": "Invoice date"},
                        "due_date": {"type": "string", "description": "Due date"},
                        "amount": {"type": "string", "description": "Invoice amount"},
                        "currency": {"type": "string", "description": "Currency (USD, EUR, GBP, NGN)"}
                    },
                    "required": ["fund_id", "investor_id", "invoice_date", "due_date", "amount", "currency"]
                }
            }
        }
EOF

# 15. SubmitTicket
cat > db_tools/submit_ticket.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class SubmitTicket(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: Optional[str], issue_date: str,
               type: str, status: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        tickets = data.get("tickets", {})
        invoices = data.get("invoices", {})
        
        # Validate invoice if provided
        if invoice_id and str(invoice_id) not in invoices:
            raise ValueError(f"Invoice {invoice_id} not found")
        
        # Validate type
        valid_types = ["missing_payment", "overpayment", "underpayment", "mismatched_amount", "invoice_duplicate", "manual_follow_up"]
        if type not in valid_types:
            raise ValueError(f"Invalid type. Must be one of {valid_types}")
        
        # Validate status
        valid_statuses = ["open", "in_review", "resolved", "closed"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        ticket_id = generate_id(tickets)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_ticket = {
            "ticket_id": str(ticket_id),
            "invoice_id": invoice_id,
            "issue_date": issue_date,
            "type": type,
            "status": status,
            "assigned_to": None,
            "resolution_date": None,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        tickets[str(ticket_id)] = new_ticket
        return json.dumps(new_ticket)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "submit_ticket",
                "description": "Submit a new ticket",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string", "description": "ID of the related invoice (optional)"},
                        "issue_date": {"type": "string", "description": "Issue date"},
                        "type": {"type": "string", "description": "Ticket type (missing_payment, overpayment, underpayment, mismatched_amount, invoice_duplicate, manual_follow_up)"},
                        "status": {"type": "string", "description": "Ticket status (open, in_review, resolved, closed)"}
                    },
                    "required": ["issue_date", "type", "status"]
                }
            }
        }
EOF

# 16. AddSubscription
cat > db_tools/add_subscription.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddSubscription(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, investor_id: str,
               amount: str, currency: str, request_assigned_to: str,
               request_date: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        subscriptions = data.get("subscriptions", {})
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        users = data.get("users", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Validate user exists
        if str(request_assigned_to) not in users:
            raise ValueError(f"User {request_assigned_to} not found")
        
        # Validate currency
        valid_currencies = ["USD", "EUR", "GBP", "NGN"]
        if currency not in valid_currencies:
            raise ValueError(f"Invalid currency. Must be one of {valid_currencies}")
        
        subscription_id = generate_id(subscriptions)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_subscription = {
            "subscription_id": str(subscription_id),
            "fund_id": fund_id,
            "investor_id": investor_id,
            "amount": amount,
            "currency": currency,
            "status": "pending",
            "request_assigned_to": request_assigned_to,
            "request_date": request_date,
            "approval_date": None,
            "updated_at": timestamp
        }
        
        subscriptions[str(subscription_id)] = new_subscription
        return json.dumps(new_subscription)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_subscription",
                "description": "Add a new subscription",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "amount": {"type": "string", "description": "Subscription amount"},
                        "currency": {"type": "string", "description": "Currency (USD, EUR, GBP, NGN)"},
                        "request_assigned_to": {"type": "string", "description": "ID of the user assigned to handle the request"},
                        "request_date": {"type": "string", "description": "Request date"}
                    },
                    "required": ["fund_id", "investor_id", "amount", "currency", "request_assigned_to", "request_date"]
                }
            }
        }
EOF

# 17. DeleteInvoice
cat > db_tools/delete_invoice.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteInvoice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: str) -> str:
        invoices = data.get("invoices", {})
        
        # Validate invoice exists
        if str(invoice_id) not in invoices:
            raise ValueError(f"Invoice {invoice_id} not found")
        
        deleted_invoice = invoices[str(invoice_id)].copy()
        del invoices[str(invoice_id)]
        
        return json.dumps({"deleted_invoice": deleted_invoice, "status": "deleted"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_invoice",
                "description": "Delete an invoice",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string", "description": "ID of the invoice to delete"}
                    },
                    "required": ["invoice_id"]
                }
            }
        }
EOF

# 18. ModifySubscription
cat > db_tools/modify_subscription.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ModifySubscription(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], subscription_id: str,
               amount: Optional[str] = None, currency: Optional[str] = None,
               status: Optional[str] = None) -> str:
        subscriptions = data.get("subscriptions", {})
        
        # Validate subscription exists
        if str(subscription_id) not in subscriptions:
            raise ValueError(f"Subscription {subscription_id} not found")
        
        subscription = subscriptions[str(subscription_id)]
        
        # Validate currency if provided
        if currency:
            valid_currencies = ["USD", "EUR", "GBP", "NGN"]
            if currency not in valid_currencies:
                raise ValueError(f"Invalid currency. Must be one of {valid_currencies}")
        
        # Validate status if provided
        if status:
            valid_statuses = ["pending", "approved", "cancelled"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Update fields
        if amount:
            subscription["amount"] = amount
        if currency:
            subscription["currency"] = currency
        if status:
            subscription["status"] = status
            if status == "approved":
                subscription["approval_date"] = "2025-10-01"
        
        subscription["updated_at"] = "2025-10-01T00:00:00ZZ"
        
        return json.dumps(subscription)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_subscription",
                "description": "Modify an existing subscription",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {"type": "string", "description": "ID of the subscription to modify"},
                        "amount": {"type": "string", "description": "New subscription amount (optional)"},
                        "currency": {"type": "string", "description": "New currency (USD, EUR, GBP, NGN) (optional)"},
                        "status": {"type": "string", "description": "New status (pending, approved, cancelled) (optional)"}
                    },
                    "required": ["subscription_id"]
                }
            }
        }
EOF

# 19. UpdateTicket
cat > db_tools/update_ticket.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateTicket(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], ticket_id: str,
               status: Optional[str] = None, resolution_date: Optional[str] = None,
               assigned_to: Optional[str] = None) -> str:
        tickets = data.get("tickets", {})
        users = data.get("users", {})
        
        # Validate ticket exists
        if str(ticket_id) not in tickets:
            raise ValueError(f"Ticket {ticket_id} not found")
        
        ticket = tickets[str(ticket_id)]
        
        # Validate status if provided
        if status:
            valid_statuses = ["open", "in_review", "resolved", "closed"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        # Validate assigned user if provided
        if assigned_to and str(assigned_to) not in users:
            raise ValueError(f"User {assigned_to} not found")
        
        # Update fields
        if status:
            ticket["status"] = status
        if resolution_date:
            ticket["resolution_date"] = resolution_date
        if assigned_to:
            ticket["assigned_to"] = assigned_to
        
        ticket["updated_at"] = "2025-10-01T00:00:00ZZ"
        
        return json.dumps(ticket)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_ticket",
                "description": "Update an existing ticket",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticket_id": {"type": "string", "description": "ID of the ticket to update"},
                        "status": {"type": "string", "description": "New status (open, in_review, resolved, closed) (optional)"},
                        "resolution_date": {"type": "string", "description": "Resolution date (optional)"},
                        "assigned_to": {"type": "string", "description": "ID of the user to assign the ticket to (optional)"}
                    },
                    "required": ["ticket_id"]
                }
            }
        }
EOF

# 20. SendUpdatesViaEmail
cat > db_tools/send_updates_via_email.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class SendUpdatesViaEmail(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], email: str, subject: str,
               message_body: str, reference_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        notifications = data.get("notifications", {})
        
        notification_id = generate_id(notifications)
        timestamp = "2025-10-01T00:00:00ZZ"
        
        new_notification = {
            "notification_id": str(notification_id),
            "email": email,
            "type": "alert",
            "class": "reports",
            "reference_id": reference_id,
            "status": "sent",
            "sent_at": timestamp,
            "created_at": timestamp,
            "subject": subject,
            "message_body": message_body
        }
        
        notifications[str(notification_id)] = new_notification
        return json.dumps(new_notification)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "send_updates_via_email",
                "description": "Send email updates/notifications",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "description": "Recipient email address"},
                        "subject": {"type": "string", "description": "Email subject"},
                        "message_body": {"type": "string", "description": "Email message body"},
                        "reference_id": {"type": "string", "description": "Optional reference ID for tracking"}
                    },
                    "required": ["email", "subject", "message_body"]
                }
            }
        }
EOF

echo "All 20 database tools have been created successfully!"
echo "Files created in db_tools/ directory:"
echo "Read APIs:"
echo "  - get_user_information.py"
echo "  - list_funds_with_filter.py"
echo "  - retrieve_investor_with_subscriptions.py"
echo "  - list_commitments.py"
echo "  - retrieve_invoices.py"
echo "  - get_payment_history.py"
echo "  - get_tickets.py"
echo "  - get_reports.py"
echo "  - fetch_investor_portfolio.py"
echo "  - retrieve_notifications.py"
echo ""
echo "Write APIs:"
echo "  - create_fund.py"
echo "  - record_payment.py"
echo "  - create_investor.py"
echo "  - create_invoice.py"
echo "  - submit_ticket.py"
echo "  - add_subscription.py"
echo "  - delete_invoice.py"
echo "  - modify_subscription.py"
echo "  - update_ticket.py"
echo "  - send_updates_via_email.py"