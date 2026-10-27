"""Shared fail-closed gate. This module makes no network or account changes."""
from datetime import datetime, timezone, timedelta
from urllib.parse import urlsplit
import math

ACCOUNT = "@maya._.finds"
SOURCES = {"TIKTOK_CREATOR_UI", "TIKTOK_OFFICIAL_CREATOR_API"}

def evaluate(record, product_id, now=None):
    now = now or datetime.now(timezone.utc)
    if not isinstance(record, dict):
        return "UNAVAILABLE", "No account evidence"
    if (record.get("account") != ACCOUNT or record.get("region") != "US"
            or record.get("product_id") != str(product_id)
            or record.get("source_type") not in SOURCES):
        return "UNAVAILABLE", "Missing or mismatched account, product, region or source"
    try:
        source = urlsplit(record.get("source", ""))
        host = source.hostname or ""
        if source.scheme != "https" or not (host == "tiktok.com" or host.endswith(".tiktok.com") or host == "tiktokshop.com" or host.endswith(".tiktokshop.com")):
            raise ValueError("source")
        stamp = datetime.fromisoformat(record["checked_at_utc"].replace("Z", "+00:00"))
        age = now - stamp
        if stamp.tzinfo is None or not timedelta(0) <= age < timedelta(hours=48):
            raise ValueError("timestamp")
    except (ValueError, TypeError, KeyError):
        return "UNAVAILABLE", "Missing, stale or future-dated account evidence"
    evidence = record.get("evidence", {})
    if not isinstance(evidence, dict) or not evidence.get("observation") or evidence.get("exact_product_id_confirmed") is not True or evidence.get("account_identity_confirmed") is not True:
        return "UNAVAILABLE", "Exact listing and signed-in account not established"
    status = record.get("verification_status")
    if status not in ("VERIFIED", "PARTIALLY VERIFIED"):
        return "UNAVAILABLE", "No completed verification"
    commission = record.get("commission_rate")
    price = record.get("price")
    numeric = lambda x: type(x) in (int, float) and math.isfinite(x)
    complete = (record.get("eligibility") in ("ELIGIBLE", "INELIGIBLE")
                and numeric(commission) and 0 <= commission <= 1
                and isinstance(price, dict) and price.get("currency") == "USD"
                and numeric(price.get("amount")) and price["amount"] > 0
                and record.get("availability") in ("IN_STOCK", "OUT_OF_STOCK")
                and record.get("add_to_showcase_status") in ("ENABLED", "DISABLED", "ALREADY_ADDED")
                and bool(record.get("availability_scope")))
    if status == "VERIFIED" and complete:
        return "VERIFIED", "All required fields observed; time-limited snapshot"
    return "PARTIALLY VERIFIED", "Account evidence exists; one or more required fields missing"

def eligible_status(record, product_id, now=None):
    status, _ = evaluate(record, product_id, now)
    return record["eligibility"] if status == "VERIFIED" else "UNVERIFIED"
