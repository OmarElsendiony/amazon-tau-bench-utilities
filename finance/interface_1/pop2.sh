#!/bin/bash

# Create directory for tools if it doesn't exist
mkdir -p tools

# Create CreateNewCommitment tool
cat > tools/create_new_commitment.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateNewCommitment(Tool):
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
            "commitment_id": commitment_id,
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
                "name": "create_new_commitment",
                "description": "Create a new commitment for an investor to a fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "commitment_amount": {"type": "string", "description": "Amount of the commitment"},
                        "currency": {"type": "string", "description": "Currency of the commitment (USD, EUR, GBP, NGN)"},
                        "commitment_date": {"type": "string", "description": "Date of the commitment in YYYY-MM-DD format"}
                    },
                    "required": ["fund_id", "investor_id", "commitment_amount", "currency", "commitment_date"]
                }
            }
        }
EOF

# Create CreatePortfolio tool
cat > tools/create_portfolio.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreatePortfolio(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, base_currency: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        investors = data.get("investors", {})
        portfolios = data.get("portfolios", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Validate currency
        valid_currencies = ["USD", "EUR", "GBP", "NGN"]
        if base_currency not in valid_currencies:
            raise ValueError(f"Invalid currency. Must be one of {valid_currencies}")
        
        portfolio_id = generate_id(portfolios)
        timestamp = "2025-10-01T00:00:00"
        
        new_portfolio = {
            "portfolio_id": portfolio_id,
            "investor_id": investor_id,
            "base_currency": base_currency,
            "status": "active",
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        portfolios[str(portfolio_id)] = new_portfolio
        return json.dumps(new_portfolio)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_portfolio",
                "description": "Create a new portfolio for an investor",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "base_currency": {"type": "string", "description": "Base currency of the portfolio (USD, EUR, GBP, NGN)"}
                    },
                    "required": ["investor_id", "base_currency"]
                }
            }
        }
EOF

# Create SubscribeInvestorToFund tool
cat > tools/subscribe_investor_to_fund.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class SubscribeInvestorToFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, investor_id: str, 
               amount: str, currency: str, request_assigned_to: str, 
               request_date: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        users = data.get("users", {})
        subscriptions = data.get("subscriptions", {})
        
        # Validate fund exists
        if str(fund_id) not in funds:
            raise ValueError(f"Fund {fund_id} not found")
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Validate assigned user exists
        if str(request_assigned_to) not in users:
            raise ValueError(f"User {request_assigned_to} not found")
        
        # Validate currency
        valid_currencies = ["USD", "EUR", "GBP", "NGN"]
        if currency not in valid_currencies:
            raise ValueError(f"Invalid currency. Must be one of {valid_currencies}")
        
        subscription_id = generate_id(subscriptions)
        timestamp = "2025-10-01T00:00:00"
        
        new_subscription = {
            "subscription_id": subscription_id,
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
                "name": "subscribe_investor_to_fund",
                "description": "Subscribe an investor to a fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "ID of the fund"},
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "amount": {"type": "string", "description": "Subscription amount"},
                        "currency": {"type": "string", "description": "Currency of the subscription (USD, EUR, GBP, NGN)"},
                        "request_assigned_to": {"type": "string", "description": "ID of the user assigned to handle the request"},
                        "request_date": {"type": "string", "description": "Date of the subscription request in YYYY-MM-DD format"}
                    },
                    "required": ["fund_id", "investor_id", "amount", "currency", "request_assigned_to", "request_date"]
                }
            }
        }
EOF

# Create PurchaseInstrument tool
cat > tools/purchase_instrument.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class PurchaseInstrument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], portfolio_id: str, instrument_id: str, 
               quantity: str, cost_basis: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        portfolios = data.get("portfolios", {})
        instruments = data.get("instruments", {})
        portfolio_holdings = data.get("portfolio_holdings", {})
        
        # Validate portfolio exists
        if str(portfolio_id) not in portfolios:
            raise ValueError(f"Portfolio {portfolio_id} not found")
        
        # Validate instrument exists
        if str(instrument_id) not in instruments:
            raise ValueError(f"Instrument {instrument_id} not found")
        
        holding_id = generate_id(portfolio_holdings)
        timestamp = "2025-10-01T00:00:00"
        
        new_holding = {
            "holding_id": holding_id,
            "portfolio_id": portfolio_id,
            "instrument_id": instrument_id,
            "quantity": quantity,
            "cost_basis": cost_basis,
            "created_at": timestamp
        }
        
        portfolio_holdings[str(holding_id)] = new_holding
        return json.dumps(new_holding)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "purchase_instrument",
                "description": "Purchase an instrument and add it to a portfolio",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "portfolio_id": {"type": "string", "description": "ID of the portfolio"},
                        "instrument_id": {"type": "string", "description": "ID of the instrument to purchase"},
                        "quantity": {"type": "string", "description": "Quantity of the instrument to purchase"},
                        "cost_basis": {"type": "string", "description": "Cost basis per unit of the instrument"}
                    },
                    "required": ["portfolio_id", "instrument_id", "quantity", "cost_basis"]
                }
            }
        }
EOF

# Create RemoveHolding tool
cat > tools/remove_holding.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RemoveHolding(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], holding_id: str) -> str:
        
        portfolio_holdings = data.get("portfolio_holdings", {})
        
        # Validate holding exists
        if str(holding_id) not in portfolio_holdings:
            raise ValueError(f"Holding {holding_id} not found")
        
        # Remove the holding
        del portfolio_holdings[str(holding_id)]
        
        return json.dumps({"holding_id": int(holding_id)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "remove_holding",
                "description": "Remove a holding from a portfolio",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "holding_id": {"type": "string", "description": "ID of the holding to remove"}
                    },
                    "required": ["holding_id"]
                }
            }
        }
EOF

# Create UpdateInvestorDetails tool
cat > tools/update_investor_details.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateInvestorDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, name: str, 
               contact_email: str, accreditation_status: str) -> str:
        
        investors = data.get("investors", {})
        
        # Validate investor exists
        if str(investor_id) not in investors:
            raise ValueError(f"Investor {investor_id} not found")
        
        # Validate accreditation status
        valid_statuses = ["accredited", "non_accredited"]
        if accreditation_status not in valid_statuses:
            raise ValueError(f"Invalid accreditation status. Must be one of {valid_statuses}")
        
        # Update investor details
        investor = investors[str(investor_id)]
        investor["name"] = name
        investor["contact_email"] = contact_email
        investor["accreditation_status"] = accreditation_status
        
        return json.dumps(investor)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_investor_details",
                "description": "Update investor details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "ID of the investor"},
                        "name": {"type": "string", "description": "New name of the investor"},
                        "contact_email": {"type": "string", "description": "New contact email of the investor"},
                        "accreditation_status": {"type": "string", "description": "New accreditation status (accredited, non_accredited)"}
                    },
                    "required": ["investor_id", "name", "contact_email", "accreditation_status"]
                }
            }
        }
EOF

# Create UpdateInvestorPortfolioHolding tool
cat > tools/update_investor_portfolio_holding.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateInvestorPortfolioHolding(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], holding_id: str, quantity: str, 
               cost_basis: str) -> str:
        
        portfolio_holdings = data.get("portfolio_holdings", {})
        
        # Validate holding exists
        if str(holding_id) not in portfolio_holdings:
            raise ValueError(f"Holding {holding_id} not found")
        
        # Update holding details
        holding = portfolio_holdings[str(holding_id)]
        holding["quantity"] = quantity
        holding["cost_basis"] = cost_basis
        
        return json.dumps(holding)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_investor_portfolio_holding",
                "description": "Update quantity and cost basis of a portfolio holding",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "holding_id": {"type": "string", "description": "ID of the holding"},
                        "quantity": {"type": "string", "description": "New quantity of the holding"},
                        "cost_basis": {"type": "string", "description": "New cost basis per unit of the holding"}
                    },
                    "required": ["holding_id", "quantity", "cost_basis"]
                }
            }
        }
EOF

# Create UpdateSubscription tool
cat > tools/update_subscription.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateSubscription(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], subscription_id: str, amount: str, 
               status: str) -> str:
        
        subscriptions = data.get("subscriptions", {})
        
        # Validate subscription exists
        if str(subscription_id) not in subscriptions:
            raise ValueError(f"Subscription {subscription_id} not found")
        
        # Validate status
        valid_statuses = ["pending", "approved", "cancelled"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        
        timestamp = "2025-10-01T00:00:00"
        
        # Update subscription details
        subscription = subscriptions[str(subscription_id)]
        subscription["amount"] = amount
        subscription["status"] = status
        subscription["updated_at"] = timestamp
        
        # Set approval date if status is approved
        if status == "approved":
            subscription["approval_date"] = timestamp.split("T")[0]  # Extract date part
        
        return json.dumps(subscription)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_subscription",
                "description": "Update subscription amount and status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {"type": "string", "description": "ID of the subscription"},
                        "amount": {"type": "string", "description": "New subscription amount"},
                        "status": {"type": "string", "description": "New subscription status (pending, approved, cancelled)"}
                    },
                    "required": ["subscription_id", "amount", "status"]
                }
            }
        }
EOF

# Create SendNotification tool
cat > tools/send_notification.py << 'EOF'
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class SendNotification(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], type: str, reference_id: str,
               recipient_id: Optional[str] = None, email: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        notifications = data.get("notifications", {})
        users = data.get("users", {})
        
        # Validate at least one recipient method is provided
        if not recipient_id and not email:
            raise ValueError("Either recipient_id or email must be provided")
        
        # If recipient_id is provided, validate user exists and get email
        recipient_email = email
        if recipient_id:
            if str(recipient_id) not in users:
                raise ValueError(f"User {recipient_id} not found")
            recipient_email = users[str(recipient_id)].get("email")
        
        # Validate notification type
        valid_types = ["alert", "report", "reminder", "subscription_update"]
        if type not in valid_types:
            raise ValueError(f"Invalid notification type. Must be one of {valid_types}")
        
        notification_id = generate_id(notifications)
        timestamp = "2025-10-01T00:00:00"
        
        new_notification = {
            "notification_id": notification_id,
            "email": recipient_email,
            "type": type,
            "class": "subscriptions",  # Default class based on common use case
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
                "name": "send_notification",
                "description": "Send a notification to a user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "recipient_id": {"type": "string", "description": "ID of the recipient user (optional if email is provided)"},
                        "email": {"type": "string", "description": "Email address of the recipient (optional if recipient_id is provided)"},
                        "type": {"type": "string", "description": "Type of notification (alert, report, reminder, subscription_update)"},
                        "reference_id": {"type": "string", "description": "ID of the related record"}
                    },
                    "required": ["type", "reference_id"]
                }
            }
        }
EOF

echo "All tool files have been created successfully in the 'tools' directory!"
echo "Generated files:"
echo "- tools/create_new_commitment.py"
echo "- tools/create_portfolio.py"
echo "- tools/subscribe_investor_to_fund.py"
echo "- tools/purchase_instrument.py"
echo "- tools/remove_holding.py"
echo "- tools/update_investor_details.py"
echo "- tools/update_investor_portfolio_holding.py"
echo "- tools/update_subscription.py"
echo "- tools/send_notification.py"