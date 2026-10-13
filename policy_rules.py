
POLICY_RULES = [
    # Settlement
    {
        "id": "SET-01",
        "clause": "Master 1.1",
        "topic": "upi_settlement",
        "valid_from": "2026-01-01",
        "valid_until": "2026-07-31",
        "precedence": 2,
    },
    {
        "id": "SET-02",
        "clause": "Circular A / Master 1.1",
        "topic": "upi_settlement",
        "valid_from": "2026-08-01",
        "valid_until": None,
        "precedence": 1,
    },
    {
        "id": "SET-03",
        "clause": "Master 1.2",
        "topic": "card_settlement",
        "valid_from": "2026-01-01",
        "valid_until": None,
        "precedence": 2,
    },
    {
        "id": "SET-04",
        "clause": "Master 1.3",
        "topic": "holiday_settlement",
        "valid_from": "2026-01-01",
        "valid_until": None,
        "precedence": 2,
    },

    # Merchant Discount Rate (MDR) and GST
    {
        "id": "MDR-01",
        "clause": "Master 2.1",
        "topic": "small_merchant_mdr",
        "valid_from": "2026-01-01",
        "valid_until": "2026-07-31",
        "precedence": 2,
    },
    {
        "id": "MDR-02",
        "clause": "Circular B / Master 2.1",
        "topic": "small_merchant_mdr",
        "valid_from": "2026-08-01",
        "valid_until": None,
        "precedence": 1,
    },
    {
        "id": "MDR-03",
        "clause": "Master 2.2",
        "topic": "large_merchant_mdr",
        "valid_from": "2026-01-01",
        "valid_until": None,
        "precedence": 2,
    },
    {
        "id": "MDR-04",
        "clause": "Master 2.3",
        "topic": "mdr_cap",
        "valid_from": "2026-01-01",
        "valid_until": "2026-07-31",
        "precedence": 2,
    },
    {
        "id": "MDR-05",
        "clause": "Circular C / Master 2.3",
        "topic": "mdr_cap",
        "valid_from": "2026-08-01",
        "valid_until": None,
        "precedence": 1,
    },
    {
        "id": "MDR-06",
        "clause": "Master 2.4",
        "topic": "gst",
        "valid_from": "2026-01-01",
        "valid_until": None,
        "precedence": 2,
    },

    # Refunds and chargebacks
    {
        "id": "REF-01",
        "clause": "Master 3.1",
        "topic": "refund_window",
        "valid_from": "2026-01-01",
        "valid_until": None,
        "precedence": 2,
    },
    {
        "id": "REF-02",
        "clause": "Master 3.2",
        "topic": "refund_mdr",
        "valid_from": "2026-01-01",
        "valid_until": "2026-08-31",
        "precedence": 2,
    },
    {
        "id": "REF-03",
        "clause": "Master 3.3",
        "topic": "refund_mdr",
        "valid_from": "2026-01-01",
        "valid_until": "2026-08-31",
        "precedence": 2,
    },
    {
        "id": "REF-04",
        "clause": "Circular D / Master 3.2",
        "topic": "refund_mdr",
        "valid_from": "2026-09-01",
        "valid_until": None,
        "precedence": 1,
    },
    {
        "id": "REF-05",
        "clause": "Master 3.4",
        "topic": "chargeback_deadline",
        "valid_from": "2026-01-01",
        "valid_until": None,
        "precedence": 2,
    },

    # Transaction and daily limits
    {
        "id": "LIM-01",
        "clause": "Master 4.1",
        "topic": "transaction_limit",
        "valid_from": "2026-01-01",
        "valid_until": None,
        "precedence": 2,
    },
    {
        "id": "LIM-02",
        "clause": "Master 4.2 and 4.4",
        "topic": "enhanced_limit",
        "valid_from": "2026-01-01",
        "valid_until": None,
        "precedence": 2,
    },
    {
        "id": "LIM-03",
        "clause": "Master 4.3",
        "topic": "daily_limit",
        "valid_from": "2026-01-01",
        "valid_until": "2026-07-31",
        "precedence": 2,
    },
    {
        "id": "LIM-04",
        "clause": "Circular E / Master 4.3",
        "topic": "daily_limit",
        "valid_from": "2026-08-01",
        "valid_until": None,
        "precedence": 1,
    },

    # Account closure
    {
        "id": "ACC-01",
        "clause": "Master 5.1",
        "topic": "account_closure_notice",
        "valid_from": "2026-01-01",
        "valid_until": None,
        "precedence": 2,
    },
    {
        "id": "ACC-02",
        "clause": "Master 5.2",
        "topic": "pending_settlement",
        "valid_from": "2026-01-01",
        "valid_until": None,
        "precedence": 2,
    },
]

# Kept separate because the FAQ may conflict with official policy.
FAQ_RULES = [
    {
        "id": "FAQ-01",
        "clause": "FAQ: When will I get my UPI money?",
        "topic": "upi_settlement",
        "valid_from": "2026-03-12",
        "valid_until": None,
        "precedence": 3,
    },
    {
        "id": "FAQ-02",
        "clause": "FAQ: What do I pay on a UPI transaction?",
        "topic": "mdr",
        "valid_from": "2026-03-12",
        "valid_until": None,
        "precedence": 3,
    },
    {
        "id": "FAQ-03",
        "clause": "FAQ: Refund fee reversal",
        "topic": "refund_mdr",
        "valid_from": "2026-03-12",
        "valid_until": None,
        "precedence": 3,
    },
    {
        "id": "FAQ-04",
        "clause": "FAQ: Maximum payment amount",
        "topic": "transaction_limit",
        "valid_from": "2026-03-12",
        "valid_until": None,
        "precedence": 3,
    },
    {
        "id": "FAQ-05",
        "clause": "FAQ: Account closure",
        "topic": "account_closure",
        "valid_from": "2026-03-12",
        "valid_until": None,
        "precedence": 3,
    },
]

def get_active_rules(topic, as_of_date):
    active_rules = []

    for rule in POLICY_RULES:
        if rule["topic"] != topic:
            continue

        if rule["valid_from"] > as_of_date:
            continue

        if rule["valid_until"] is not None:
            if rule["valid_until"] < as_of_date:
                continue

        active_rules.append(rule)

    return active_rules
