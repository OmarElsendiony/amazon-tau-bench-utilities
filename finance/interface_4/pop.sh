#!/bin/bash

# Create directory for tools
mkdir -p db_tools

# Create IdentifyUser tool
cat > db_tools/identify_user.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class IdentifyUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], email: Optional[str] = None, 
               user_id: Optional[str] = None) -> str:
        users = data.get("users", {})
        
        if not email and not user_id:
            raise ValueError("Either email or user_id must be provided")
        
        for user in users.values():
            if email and user.get("email", "").lower() == email.lower():
                return json.dumps(user)
            if user_id and user.get("user_id") == user_id:
                return json.dumps(user)
        
        raise ValueError("User not found")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "identify_user",
                "description": "Identify a user by email or user ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "description": "User email address"},
                        "user_id": {"type": "string", "description": "User ID"}
                    },
                    "required": []
                }
            }
        }
EOF

# Create GetInvestorWithSubscriptions tool
cat > db_tools/get_investor_with_subscriptions.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvestorWithSubscriptions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], subscription_id: Optional[str] = None,
               name: Optional[str] = None, contact_email: Optional[str] = None,
               employee_id: Optional[str] = None) -> str:
        investors = data.get("investors", {})
        subscriptions = data.get("subscriptions", {})
        results = []
        
        for investor in investors.values():
            # Apply filters
            if name and name.lower() not in investor.get("name", "").lower():
                continue
            if contact_email and investor.get("contact_email", "").lower() != contact_email.lower():
                continue
            if employee_id and investor.get("employee_id") != employee_id:
                continue
            
            # Get investor's subscriptions
            investor_subscriptions = []
            for subscription in subscriptions.values():
                if subscription.get("investor_id") == investor.get("investor_id"):
                    if subscription_id and subscription.get("subscription_id") != subscription_id:
                        continue
                    investor_subscriptions.append(subscription)
            
            # If subscription_id filter is applied and no matching subscription found, skip
            if subscription_id and not investor_subscriptions:
                continue
            
            investor_with_subs = investor.copy()
            investor_with_subs["subscriptions"] = investor_subscriptions
            results.append(investor_with_subs)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_with_subscriptions",
                "description": "Get investors with their subscriptions based on filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {"type": "string", "description": "Filter by subscription ID"},
                        "name": {"type": "string", "description": "Filter by investor name"},
                        "contact_email": {"type": "string", "description": "Filter by contact email"},
                        "employee_id": {"type": "string", "description": "Filter by employee ID"}
                    },
                    "required": []
                }
            }
        }
EOF

# Create GetFunds tool
cat > db_tools/get_funds.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetFunds(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Optional[Dict[str, Any]] = None) -> str:
        funds = data.get("funds", {})
        results = []
        
        if not filters:
            filters = {}
        
        for fund in funds.values():
            # Apply filters
            if filters.get("fund_id") and fund.get("fund_id") != filters["fund_id"]:
                continue
            if filters.get("name") and filters["name"].lower() not in fund.get("name", "").lower():
                continue
            if filters.get("fund_type") and fund.get("fund_type") != filters["fund_type"]:
                continue
            if filters.get("base_currency") and fund.get("base_currency") != filters["base_currency"]:
                continue
            if filters.get("manager_id") and fund.get("manager_id") != filters["manager_id"]:
                continue
            if filters.get("status") and fund.get("status") != filters["status"]:
                continue
            
            results.append(fund)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_funds",
                "description": "Get funds based on filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filters": {
                            "type": "object",
                            "description": "Filters to apply (fund_id, name, fund_type, base_currency, manager_id, status)"
                        }
                    },
                    "required": []
                }
            }
        }
EOF

# Create GetCommitments tool
cat > db_tools/get_commitments.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetCommitments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Optional[Dict[str, Any]] = None) -> str:
        commitments = data.get("commitments", {})
        results = []
        
        if not filters:
            filters = {}
        
        for commitment in commitments.values():
            # Apply filters
            if filters.get("commitment_id") and commitment.get("commitment_id") != filters["commitment_id"]:
                continue
            if filters.get("fund_id") and commitment.get("fund_id") != filters["fund_id"]:
                continue
            if filters.get("investor_id") and commitment.get("investor_id") != filters["investor_id"]:
                continue
            if filters.get("currency") and commitment.get("currency") != filters["currency"]:
                continue
            if filters.get("status") and commitment.get("status") != filters["status"]:
                continue
            if filters.get("commitment_date") and commitment.get("commitment_date") != filters["commitment_date"]:
                continue
            
            results.append(commitment)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_commitments",
                "description": "Get commitments based on filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filters": {
                            "type": "object",
                            "description": "Filters to apply (commitment_id, fund_id, investor_id, currency, status, commitment_date)"
                        }
                    },
                    "required": []
                }
            }
        }
EOF

# Create GetInvoices tool
cat > db_tools/get_invoices.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvoices(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Optional[Dict[str, Any]] = None) -> str:
        invoices = data.get("invoices", {})
        results = []
        
        if not filters:
            filters = {}
        
        for invoice in invoices.values():
            # Apply filters
            if filters.get("invoice_id") and invoice.get("invoice_id") != filters["invoice_id"]:
                continue
            if filters.get("fund_id") and invoice.get("fund_id") != filters["fund_id"]:
                continue
            if filters.get("investor_id") and invoice.get("investor_id") != filters["investor_id"]:
                continue
            if filters.get("commitment_id") and invoice.get("commitment_id") != filters["commitment_id"]:
                continue
            if filters.get("status") and invoice.get("status") != filters["status"]:
                continue
            if filters.get("currency") and invoice.get("currency") != filters["currency"]:
                continue
            if filters.get("payment_type") and invoice.get("payment_type") != filters["payment_type"]:
                continue
            
            results.append(invoice)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_invoices",
                "description": "Get invoices based on filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filters": {
                            "type": "object",
                            "description": "Filters to apply (invoice_id, fund_id, investor_id, commitment_id, status, currency, payment_type)"
                        }
                    },
                    "required": []
                }
            }
        }
EOF

# Create GetPayments tool
cat > db_tools/get_payments.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetPayments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: Optional[str] = None,
               status: Optional[str] = None) -> str:
        payments = data.get("payments", {})
        results = []
        
        for payment in payments.values():
            if invoice_id and payment.get("invoice_id") != invoice_id:
                continue
            if status and payment.get("status") != status:
                continue
            
            results.append(payment)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_payments",
                "description": "Get payments with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string", "description": "Filter by invoice ID"},
                        "status": {"type": "string", "description": "Filter by payment status (draft, completed, failed)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Create CheckCommitmentFulfillmentStatus tool
cat > db_tools/check_commitment_fulfillment_status.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CheckCommitmentFulfillmentStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_id: str) -> str:
        commitments = data.get("commitments", {})
        
        if str(commitment_id) not in commitments:
            raise ValueError(f"Commitment {commitment_id} not found")
        
        commitment = commitments[str(commitment_id)]
        status = commitment.get("status", "pending")
        
        return json.dumps({"status": status})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "check_commitment_fulfillment_status",
                "description": "Check the fulfillment status of a commitment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {"type": "string", "description": "ID of the commitment"}
                    },
                    "required": ["commitment_id"]
                }
            }
        }
EOF

# Create GetTickets tool
cat > db_tools/get_tickets.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetTickets(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: Optional[str] = None,
               status: Optional[str] = None) -> str:
        tickets = data.get("tickets", {})
        results = []
        
        for ticket in tickets.values():
            if invoice_id and ticket.get("invoice_id") != invoice_id:
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
                        "invoice_id": {"type": "string", "description": "Filter by invoice ID"},
                        "status": {"type": "string", "description": "Filter by ticket status (open, in_review, resolved, closed)"}
                    },
                    "required": []
                }
            }
        }
EOF

# Create RetrieveReports tool
cat > db_tools/retrieve_reports.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RetrieveReports(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Optional[Dict[str, Any]] = None) -> str:
        reports = data.get("reports", {})
        results = []
        
        if not filters:
            filters = {}
        
        for report in reports.values():
            # Apply filters
            if filters.get("report_id") and report.get("report_id") != filters["report_id"]:
                continue
            if filters.get("fund_id") and report.get("fund_id") != filters["fund_id"]:
                continue
            if filters.get("investor_id") and report.get("investor_id") != filters["investor_id"]:
                continue
            if filters.get("report_type") and report.get("report_type") != filters["report_type"]:
                continue
            if filters.get("generated_by") and report.get("generated_by") != filters["generated_by"]:
                continue
            if filters.get("status") and report.get("status") != filters["status"]:
                continue
            
            results.append(report)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_reports",
                "description": "Retrieve reports based on filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filters": {
                            "type": "object",
                            "description": "Filters to apply (report_id, fund_id, investor_id, report_type, generated_by, status)"
                        }
                    },
                    "required": []
                }
            }
        }
EOF

# Create GetCommitmentFulfillmentPercentage tool
cat > db_tools/get_commitment_fulfillment_percentage.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool
from decimal import Decimal

class GetCommitmentFulfillmentPercentage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_id: str) -> str:
        commitments = data.get("commitments", {})
        invoices = data.get("invoices", {})
        payments = data.get("payments", {})
        
        if str(commitment_id) not in commitments:
            raise ValueError(f"Commitment {commitment_id} not found")
        
        commitment = commitments[str(commitment_id)]
        commitment_amount = Decimal(str(commitment.get("commitment_amount", 0)))
        
        if commitment_amount == 0:
            return json.dumps({"fulfilled_percent": "0.00"})
        
        # Find all invoices for this commitment
        commitment_invoices = []
        for invoice in invoices.values():
            if invoice.get("commitment_id") == commitment_id:
                commitment_invoices.append(invoice)
        
        # Calculate total paid amount
        total_paid = Decimal("0")
        for invoice in commitment_invoices:
            invoice_id = invoice.get("invoice_id")
            for payment in payments.values():
                if (payment.get("invoice_id") == invoice_id and 
                    payment.get("status") == "completed"):
                    total_paid += Decimal(str(payment.get("amount", 0)))
        
        # Calculate percentage
        if commitment_amount > 0:
            percentage = (total_paid / commitment_amount) * 100
            percentage = min(percentage, Decimal("100"))  # Cap at 100%
        else:
            percentage = Decimal("0")
        
        return json.dumps({"fulfilled_percent": str(percentage.quantize(Decimal("0.01")))})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_commitment_fulfillment_percentage",
                "description": "Get the fulfillment percentage of a commitment based on completed payments",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {"type": "string", "description": "ID of the commitment"}
                    },
                    "required": ["commitment_id"]
                }
            }
        }
EOF

# Create CreateReport tool
cat > db_tools/create_report.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateReport(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, investor_id: str,
               report_date: str, report_type: str, generated_by: str,
               export_period_end: str) -> str:
        
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
        timestamp = "2025-10-01T00:00:00"
        
        new_report = {
            "report_id": str(report_id),
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
                "name": "create_report",
                "description": "Create a new report",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "report_date": {"type": "string", "description": "Report date in YYYY-MM-DD format"},
                        "report_type": {"type": "string", "description": "Report type (performance, holding, financial)"},
                        "generated_by": {"type": "string", "description": "ID of the user generating the report"},
                        "export_period_end": {"type": "string", "description": "Export period end date in YYYY-MM-DD format"}
                    },
                    "required": ["fund_id", "investor_id", "report_date", "report_type", "generated_by", "export_period_end"]
                }
            }
        }
EOF

# Create UpdateCommitmentDetails tool
cat > db_tools/update_commitment_details.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateCommitmentDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_id: str,
               commitment_amount: str, status: str) -> str:
        commitments = data.get("commitments", {})
        
        if str(commitment_id) not in commitments:
            raise ValueError(f"Commitment {commitment_id} not found")
        
        # Validate status
        valid_statuses = ["pending", "fulfilled"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        commitment = commitments[str(commitment_id)]
        commitment["commitment_amount"] = commitment_amount
        commitment["status"] = status
        commitment["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(commitment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_commitment_details",
                "description": "Update commitment details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {"type": "string", "description": "ID of the commitment"},
                        "commitment_amount": {"type": "string", "description": "Updated commitment amount"},
                        "status": {"type": "string", "description": "Updated status (pending, fulfilled)"}
                    },
                    "required": ["commitment_id", "commitment_amount", "status"]
                }
            }
        }
EOF

# Create UpdateInvoice tool
cat > db_tools/update_invoice.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateInvoice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: str,
               amount: str, due_date: str, status: str) -> str:
        invoices = data.get("invoices", {})
        
        if str(invoice_id) not in invoices:
            raise ValueError(f"Invoice {invoice_id} not found")
        
        # Validate status
        valid_statuses = ["issued", "paid"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        invoice = invoices[str(invoice_id)]
        invoice["amount"] = amount
        invoice["due_date"] = due_date
        invoice["status"] = status
        invoice["updated_at"] = "2025-10-01T00:00:00"
        
        return json.dumps(invoice)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_invoice",
                "description": "Update invoice details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string", "description": "ID of the invoice"},
                        "amount": {"type": "string", "description": "Updated amount"},
                        "due_date": {"type": "string", "description": "Updated due date in YYYY-MM-DD format"},
                        "status": {"type": "string", "description": "Updated status (issued, paid)"}
                    },
                    "required": ["invoice_id", "amount", "due_date", "status"]
                }
            }
        }
EOF

# Create UpdatePaymentDetails tool
cat > db_tools/update_payment_details.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdatePaymentDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], payment_id: str,
               amount: str, payment_method: str, status: str) -> str:
        payments = data.get("payments", {})
        
        if str(payment_id) not in payments:
            raise ValueError(f"Payment {payment_id} not found")
        
        # Validate payment method
        valid_methods = ["wire", "cheque", "credit_card", "bank_transfer"]
        if payment_method not in valid_methods:
            raise ValueError(f"Invalid payment method. Must be one of {valid_methods}")
        
        # Validate status
        valid_statuses = ["draft", "completed", "failed"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        payment = payments[str(payment_id)]
        payment["amount"] = amount
        payment["payment_method"] = payment_method
        payment["status"] = status
        
        return json.dumps(payment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_payment_details",
                "description": "Update payment details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "payment_id": {"type": "string", "description": "ID of the payment"},
                        "amount": {"type": "string", "description": "Updated amount"},
                        "payment_method": {"type": "string", "description": "Updated payment method (wire, cheque, credit_card, bank_transfer)"},
                        "status": {"type": "string", "description": "Updated status (draft, completed, failed)"}
                    },
                    "required": ["payment_id", "amount", "payment_method", "status"]
                }
            }
        }
EOF

# Create SendEmailNotification tool
cat > db_tools/send_email_notification.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SendEmailNotification(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], email: str, class_name: str,
               reference_id: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        notifications = data.get("notifications", {})
        
        # Validate class
        valid_classes = ["funds", "investors", "portfolios", "trades", "invoices", 
                        "reports", "documents", "subscriptions", "commitments"]
        if class_name not in valid_classes:
            raise ValueError(f"Invalid class. Must be one of {valid_classes}")
        
        notification_id = generate_id(notifications)
        timestamp = "2025-10-01T00:00:00"
        
        new_notification = {
            "notification_id": str(notification_id),
            "email": email,
            "type": "alert",
            "class": class_name,
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
                "name": "send_email_notification",
                "description": "Send an email notification",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "description": "Email address to send notification to"},
                        "class_name": {"type": "string", "description": "Notification class (funds, investors, portfolios, trades, invoices, reports, documents, subscriptions, commitments)"},
                        "reference_id": {"type": "string", "description": "Reference ID for the notification"}
                    },
                    "required": ["email", "class_name", "reference_id"]
                }
            }
        }
EOF

echo "All 20 database tools have been created successfully!"
echo "Files created in db_tools/ directory:"

# ls -la db_tools/Commitment tool
cat > db_tools/create_commitment.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateCommitment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, investor_id: str,
               commitment_amount: str, currency: str, commitment_date: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        commitments = data.get("commitments", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Validate currency
        valid_currencies = ["USD", "EUR", "GBP", "NGN"]
        if currency not in valid_currencies:
            raise ValueError(f"Invalid currency. Must be one of {valid_currencies}")
        
        commitment_id = generate_id(commitments)
        timestamp = "2025-10-01T00:00:00"
        
        new_commitment = {
            "commitment_id": str(commitment_id),
            "fund_id": fund_id,
            "investor_id": investor_id,
            "commitment_amount": commitment_amount,
            "currency": currency,
            "commitment_date": commitment_date,
            "status": "pending",
            "updated_at": timestamp
        }
        
        commitments[str(commitment_id)] = new_commitment
        return json.dumps(new_commitment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_commitment",
                "description": "Create a new commitment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "commitment_amount": {"type": "string", "description": "Commitment amount"},
                        "currency": {"type": "string", "description": "Currency (USD, EUR, GBP, NGN)"},
                        "commitment_date": {"type": "string", "description": "Commitment date in YYYY-MM-DD format"}
                    },
                    "required": ["fund_id", "investor_id", "commitment_amount", "currency", "commitment_date"]
                }
            }
        }
EOF

# Create IssueInvoice tool
cat > db_tools/issue_invoice.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class IssueInvoice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, investor_id: str,
               commitment_id: str, invoice_date: str, due_date: str,
               amount: str, currency: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        commitments = data.get("commitments", {})
        invoices = data.get("invoices", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Validate commitment exists
        if str(commitment_id) not in commitments:
            raise ValueError(f"Commitment {commitment_id} not found")
        
        # Validate currency
        valid_currencies = ["USD", "EUR", "GBP", "NGN"]
        if currency not in valid_currencies:
            raise ValueError(f"Invalid currency. Must be one of {valid_currencies}")
        
        invoice_id = generate_id(invoices)
        timestamp = "2025-10-01T00:00:00"
        
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
                "name": "issue_invoice",
                "description": "Issue a new invoice",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "commitment_id": {"type": "string", "description": "ID of the commitment"},
                        "invoice_date": {"type": "string", "description": "Invoice date in YYYY-MM-DD format"},
                        "due_date": {"type": "string", "description": "Due date in YYYY-MM-DD format"},
                        "amount": {"type": "string", "description": "Invoice amount"},
                        "currency": {"type": "string", "description": "Currency (USD, EUR, GBP, NGN)"}
                    },
                    "required": ["fund_id", "investor_id", "commitment_id", "invoice_date", "due_date", "amount", "currency"]
                }
            }
        }
EOF

# Create RegisterPayment tool
cat > db_tools/register_payment.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RegisterPayment(Tool):
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
        timestamp = "2025-10-01T00:00:00"
        
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
                "name": "register_payment",
                "description": "Register a new payment",
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

# Create DeleteCommitment tool
cat > db_tools/delete_commitment.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteCommitment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_id: str) -> str:
        commitments = data.get("commitments", {})
        
        if str(commitment_id) not in commitments:
            raise ValueError(f"Commitment {commitment_id} not found")
        
        deleted_commitment = commitments.pop(str(commitment_id))
        return json.dumps(deleted_commitment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_commitment",
                "description": "Delete a commitment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {"type": "string", "description": "ID of the commitment to delete"}
                    },
                    "required": ["commitment_id"]
                }
            }
        }
EOF

# Create CreateTicket tool
cat > db_tools/create_ticket.py << 'EOF'
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateTicket(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], invoice_id: str, issue_date: str,
               type: str, status: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        invoices = data.get("invoices", {})
        tickets = data.get("tickets", {})
        
        # Validate invoice exists
        if str(invoice_id) not in invoices:
            raise ValueError(f"Invoice {invoice_id} not found")
        
        # Validate type
        valid_types = ["missing_payment", "overpayment", "underpayment", 
                      "mismatched_amount", "invoice_duplicate", "manual_follow_up"]
        if type not in valid_types:
            raise ValueError(f"Invalid type. Must be one of {valid_types}")
        
        # Validate status
        valid_statuses = ["open", "in_review", "resolved", "closed"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        ticket_id = generate_id(tickets)
        timestamp = "2025-10-01T00:00:00"
        
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
                "name": "create_ticket",
                "description": "Create a new ticket",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "invoice_id": {"type": "string", "description": "ID of the invoice"},
                        "issue_date": {"type": "string", "description": "Issue date in ISO format"},
                        "type": {"type": "string", "description": "Ticket type (missing_payment, overpayment, underpayment, mismatched_amount, invoice_duplicate, manual_follow_up)"},
                        "status": {"type": "string", "description": "Ticket status (open, in_review, resolved, closed)"}
                    },
                    "required": ["invoice_id", "issue_date", "type", "status"]
                }
            }
        }
EOF

# Create Create