
import re

from policy_rules import get_active_rules, POLICY_RULES, FAQ_RULES


def detect_topic(question):
    question = question.lower()

    if "refund" in question or "fee back" in question:
        return "refund_mdr"

    if "chargeback" in question:
        return "chargeback_deadline"

    if "pending" in question and "settlement" in question:
        return "pending_settlement"

    if "close my account" in question or "account closure" in question:
        return "account_closure_notice"

    if "daily limit" in question or "twice in one day" in question:
        return "daily_limit"

    if "insurance" in question or "capital markets" in question:
        return "enhanced_limit"

    if "maximum amount" in question or "transaction limit" in question:
        return "transaction_limit"

    if "card" in question:
        return "card_settlement"

    if "settlement" in question or "receive my money" in question:
        return "upi_settlement"

    if "mdr cap" in question or "upper limit on the fee" in question:
        return "mdr_cap"

    if "small merchant" in question:
        return "small_merchant_mdr"

    if "large merchant" in question:
        return "large_merchant_mdr"

    if "gst" in question:
        return "gst"

    if "mdr" in question or "fee" in question:
        return "large_merchant_mdr"

    return None


def find_rules(question, as_of_date="2026-08-15"):
    topic = detect_topic(question)

    if topic is None:
        return []

    return get_active_rules(topic, as_of_date)


def ask(question, as_of_date="2026-08-15"):
    original_question = question
    question = question.lower()
    topic = detect_topic(question)

    if topic is None:
        return {
            "answer": "I cannot answer this from the available policy rules.",
            "citations": [],
            "status": "CANNOT_ANSWER",
        }

    # Calculate fees when the question includes an amount
    # and identifies the merchant as small or large.
    amount_match = re.search(
        r"(?:₹|rs\.?\s*)\s*([\d,]+)|([\d,]+)\s*(?:rupees|inr)",
        question,
    )

    if amount_match and (
        "large merchant" in question or "small merchant" in question
    ):
        amount_text = amount_match.group(1) or amount_match.group(2)
        amount = float(amount_text.replace(",", ""))

        merchant_type = (
            "small" if "small merchant" in question else "large"
        )

        fees = calculate_mdr(amount, merchant_type, as_of_date)

        if fees is None:
            return {
                "answer": "I cannot calculate this fee.",
                "citations": [],
                "status": "CANNOT_ANSWER",
            }

        citations = [
            "Master 2.2",
            "Circular C / Master 2.3",
            "Master 2.4",
        ]

        if merchant_type == "small":
            citations[0] = "Circular B / Master 2.1"

        return {
            "answer": (
                f"For a ₹{amount:,.2f} transaction, "
                f"MDR is ₹{fees['mdr']:.2f}, "
                f"GST is ₹{fees['gst']:.2f}, "
                f"and the total fee is ₹{fees['total_fee']:.2f}."
            ),
            "citations": citations,
            "status": "ANSWERED",
        }

    if topic == "refund_mdr":
        if as_of_date >= "2026-09-01":
            answer = (
                "No. From 1 September 2026, MDR is not returned "
                "on refunded transactions."
            )
            citations = [
                "policy_master_v1.md, clause 3.2",
                "circular_2026_08_amendment.md, section D",
            ]
        else:
            answer = (
                "Yes. If the refund is initiated within 24 hours, "
                "the MDR is reversed in full."
            )
            citations = [
                "policy_master_v1.md, clauses 3.2 and 3.3"
            ]

    elif topic == "upi_settlement":
        answer = (
            "UPI settles by 11:59 PM on the same day for merchants "
            "with an active Instant Settlement add-on. Others receive "
            "settlement on the next working day."
        )
        citations = [
            "circular_2026_08_amendment.md, section A",
            "policy_master_v1.md, clause 1.1",
        ]

    elif topic == "card_settlement":
        answer = "Card transactions settle in two working days (T+2)."
        citations = ["policy_master_v1.md, clause 1.2"]

    elif topic == "mdr_cap":
        answer = (
            "The FAQ says there is no upper limit on the fee. "
            "That is incorrect under the policy effective 1 August 2026: "
            "the cap is ₹15 for merchants with monthly volume up to "
            "₹10 lakh and ₹25 for merchants above ₹10 lakh."
        )
        citations = [
            "merchant_faq_2026-03.md, section: What do I pay on a UPI transaction?",
            "circular_2026_08_amendment.md, section C",
            
        ]
        status = "CONFLICT_RESOLVED"

    elif topic == "small_merchant_mdr":
        rate = 0.25 if as_of_date >= "2026-08-01" else 0.30
        answer = (
            f"The UPI MDR rate for small merchants is {rate:.2f}% "
            "for monthly volume up to ₹10 lakh."
        )
        citations = [
            "policy_master_v1.md, clause 2.1",
            "circular_2026_08_amendment.md, section B",
        ]

    elif topic == "large_merchant_mdr":
        answer = (
            "The UPI MDR rate is 0.50% for merchants with monthly "
            "volume above ₹10 lakh, subject to the applicable cap."
        )
        citations = [
            "policy_master_v1.md, clauses 2.2 and 2.3",
            "circular_2026_08_amendment.md, section C",
        ]

    elif topic == "gst":
        answer = (
            "GST is 18% of the MDR amount and is not included "
            "in the MDR cap."
        )
        citations = ["policy_master_v1.md, clause 2.4"]

    elif topic == "daily_limit":
        answer = (
            "The daily limit per customer account is ₹1,00,000 "
            "or the limit set by the customer's own bank, "
            "whichever is lower. Therefore, two payments of ₹1,00,000 "
            "cannot both be made if they exceed that daily limit."
        )
        citations = [
            "policy_master_v1.md, clauses 4.1 and 4.3",
            "circular_2026_08_amendment.md, section E",
        ]

    elif topic == "transaction_limit":
        answer = "The per-transaction UPI limit is ₹1,00,000."
        citations = ["policy_master_v1.md, clause 4.1"]

    elif topic == "enhanced_limit":
        answer = (
            "Eligible Insurance and Capital Markets merchants may "
            "accept up to ₹2,00,000 per transaction if they have "
            "completed enhanced KYC."
        )
        citations = [
            "policy_master_v1.md, clauses 4.2 and 4.4"
        ]

    elif topic == "account_closure_notice":
        answer = (
            "A merchant may close the account with 30 days' "
            "written notice."
        )
        citations = ["policy_master_v1.md, clause 5.1"]

    elif topic == "pending_settlement":
        answer = (
            "Pending settlements are released within 10 working "
            "days of account closure, after deducting outstanding dues."
        )
        citations = ["policy_master_v1.md, clause 5.2"]

    elif topic == "chargeback_deadline":
        answer = (
            "The customer's bank must raise chargeback disputes "
            "within 120 days."
        )
        citations = ["policy_master_v1.md, clause 3.4"]

    else:
        return {
            "answer": "I cannot answer this from the available policy rules.",
            "citations": [],
            "status": "CANNOT_ANSWER",
        }

    return {
        "answer": answer,
        "citations": citations,
        "status": status if topic == "mdr_cap" else "ANSWERED",
    }


def calculate_mdr(amount, merchant_type, as_of_date="2026-08-15"):
    if amount < 0:
        return None

    if merchant_type == "small":
        rate = 0.0025 if as_of_date >= "2026-08-01" else 0.003
        cap = 15

    elif merchant_type == "large":
        rate = 0.005
        cap = 25 if as_of_date >= "2026-08-01" else 15

    else:
        return None

    mdr = min(amount * rate, cap)
    gst = mdr * 0.18

    return {
        "transaction_amount": amount,
        "mdr": round(mdr, 2),
        "gst": round(gst, 2),
        "total_fee": round(mdr + gst, 2),
    }
