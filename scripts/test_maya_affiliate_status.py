import copy
import unittest
from datetime import datetime, timezone, timedelta
from maya_affiliate_status import evaluate, eligible_status

class VerificationGateTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 27, 20, tzinfo=timezone.utc)
        self.record = dict(product_id="123", account="@maya._.finds", region="US",
            source_type="TIKTOK_CREATOR_UI", source="https://shop.tiktok.com/",
            checked_at_utc=self.now.isoformat(), verification_status="VERIFIED",
            eligibility="ELIGIBLE", commission_rate=0.1,
            price={"amount": 20, "currency": "USD"}, availability="IN_STOCK",
            availability_scope="Displayed blue / size M", add_to_showcase_status="ENABLED",
            evidence={"observation": "Synthetic unit test, never account evidence",
                      "exact_product_id_confirmed": True, "account_identity_confirmed": True})

    def test_complete_and_ineligible_are_distinct(self):
        self.assertEqual(eligible_status(self.record, "123", self.now), "ELIGIBLE")
        self.record["eligibility"] = "INELIGIBLE"
        self.assertEqual(evaluate(self.record, "123", self.now)[0], "VERIFIED")
        self.assertEqual(eligible_status(self.record, "123", self.now), "INELIGIBLE")

    def test_time_boundaries(self):
        for hours in (-1, 48, 49):
            self.record["checked_at_utc"] = (self.now - timedelta(hours=hours)).isoformat()
            self.assertEqual(eligible_status(self.record, "123", self.now), "UNVERIFIED")

    def test_identity_and_source(self):
        for field, value in (("account", "@someone_else"), ("product_id", "124"),
                             ("region", "GB"), ("source_type", "ECHOTIK"),
                             ("source", "https://tiktok.com.evil.example/")):
            record = copy.deepcopy(self.record)
            record[field] = value
            self.assertEqual(eligible_status(record, "123", self.now), "UNVERIFIED")

    def test_missing_fields_remain_partial(self):
        for field in ("price", "commission_rate", "availability", "add_to_showcase_status"):
            record = copy.deepcopy(self.record)
            record[field] = None
            self.assertEqual(evaluate(record, "123", self.now)[0], "PARTIALLY VERIFIED")
            self.assertEqual(eligible_status(record, "123", self.now), "UNVERIFIED")

    def test_no_search_only_approval(self):
        self.record["evidence"]["exact_product_id_confirmed"] = False
        self.assertEqual(evaluate(self.record, "123", self.now)[0], "UNAVAILABLE")

    def test_bad_numeric_fields(self):
        for value in (True, float("nan"), 10, -1):
            self.record["commission_rate"] = value
            self.assertEqual(eligible_status(self.record, "123", self.now), "UNVERIFIED")

if __name__ == "__main__":
    unittest.main()
