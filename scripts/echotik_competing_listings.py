#!/usr/bin/env python3
"""Transparent comparison among the 50 collected listings, NOT marketplace competition."""
import json
import re
from pathlib import Path
root=Path("data")
rank=json.loads((root/"echotik-product-rankings.json").read_text())
detail=json.loads((root/"echotik-competition-evidence.json").read_text())
items=rank.get("data",{}).get("data",[])
families={
 "leggings":r"\b(legging|tights|yoga pants)\b",
 "jeans":r"\b(jeans|denim)\b",
 "sweater":r"\b(sweater|cardigan|pullover)\b",
 "jacket":r"\b(jacket|puffer|coat)\b",
 "shoes":r"\b(shoes|sneaker|clogs|boots|sandals)\b",
 "pants":r"\b(pants|trousers|sweatpants)\b",
 "bag":r"\b(handbag|purse|tote)\b",
 "dress":r"\b(dress|skirt)\b",
}
def categories(name):
 return {k for k,v in families.items() if re.search(v,name,re.I)}
out={"source":"Same-day EchoTik 50-product ranking sample only","sample_size":len(items),
 "marketwide_competing_listings_count":None,"products":{}}
for pid in detail.get("requested_product_ids",[]):
 p=next((x for x in items if str(x.get("product_id"))==pid),None)
 if not p: continue
 cats=categories(str(p.get("product_name","")))
 peers=[x for x in items if str(x.get("product_id"))!=pid and cats.intersection(categories(str(x.get("product_name",""))))]
 out["products"][pid]={"shared_broad_category":sorted(cats),
  "other_listings_in_ranking_sample":len(peers),
  "sample_peer_product_ids":[str(x.get("product_id")) for x in peers[:20]],
  "equivalent_listings_verified":None,
  "note":"Broad keyword overlap within top-50 ranking only; not a count of comparable competing marketplace listings"}
(root/"echotik-listing-overlap.json").write_text(json.dumps(out,indent=2)+"\n")
print("Listing overlap checked",len(out["products"]),"products in",len(items),"ranked listings")
