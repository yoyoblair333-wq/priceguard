# PriceGuard

**Price protection that pays out on GenLayer validator consensus.**

Credit cards used to refund you when something you bought got cheaper within 60 to 90 days. Most issuers dropped the benefit because every claim meant a person comparing a receipt with a product page. PriceGuard turns that check into one GenLayer round. Validators read the product page, agree on today's price to the cent for that exact item and variant, and plain code refunds the drop from the issuer's pool.

- Live app: https://yoyoblair333-wq.github.io/priceguard/
- Live contract (studionet): `0xAeD6034E3aB271822c67De82A36B4270B9b4a94E`
- Live evidence: [docs/LIVE_EVIDENCE.md](docs/LIVE_EVIDENCE.md) (raw: [docs/live/run.json](docs/live/run.json))

## Who it is for

- **Card programs, fintechs and retailers** that want to offer price protection again without a claims desk.
- **Shoppers**, who get the difference without filing anything: anyone can trigger the check.

## How it works

1. **Open a plan.** The issuer calls `open_plan` with:
   - the coverage share (e.g. 100 % of the drop);
   - the protection window (e.g. 60 days);
   - the retail sites it covers;
   - a minimum drop and a cap per purchase.

   The attached value funds the pool.
2. **Register purchases.** The issuer registers purchases it has seen a receipt for: buyer, product page (on a covered site), item, variant, currency, price paid and date. On a demo plan anyone may register their own purchase.
3. **Check (consensus).** Anyone calls `check` inside the window, once per purchase every 12 hours. Validators agree on `{status, price_cents}`.
4. **Payout (plain code).**
   - The refund is `min(coverage × (paid − lowest price seen), cap)`, and only if the drop is at least the minimum. What was already paid is subtracted.
   - A deeper drop later pays only the extra difference. The same drop never pays twice. A price that rises again never claws anything back.
   - Accounting is in **wei actually paid**. If the pool was short and paid only part of a refund, a later refill pays only the remainder: cumulative credit for a purchase can never exceed its entitlement (regression: `TestPartialPoolRefill` — a 2-cent drop at 1,000 wei/USD is 20 wei; 5 wei paid, pool refilled, total stays 20).
   - The refund goes to the buyer's balance at once, and the buyer calls `withdraw`.

## How consensus is used

Each validator, on **its own** fetch of the product page:

1. Reduces the HTML to text itself. Script contents are dropped, so prices in tracking code can't count. JavaScript-only pages fall back to a render.
2. Checks that every word of the item name is on the page; otherwise the page is `UNREADABLE`.
3. Asks its model for the current selling price of that item and variant. The prompt rules out the struck-through "was" price, other sizes or memory versions, add-ons and "you may also like" products, member or coupon prices, financing instalments and shipping. The page sits between random fences and is declared untrusted.
4. Reduces the answer with **deterministic code**: the price must be **printed on this validator's copy of the page**, as a whole number, with the purchase currency's sign or code right next to it. `$1120.00` never certifies `120.00`, and a bare `120.00 points` does not count. A wrong currency or a price that isn't on the page becomes `AMBIGUOUS`.

```json
{"status": "PRICED | UNAVAILABLE | AMBIGUOUS | UNREADABLE", "price_cents": 12000}
```

The validator accepts the leader only if this record is **exactly equal** to its own, to the cent. There is no tolerance band. Out of stock, unclear and unreadable all pay nothing (fail closed).

## Live run (studionet)

The real page is Adafruit's [Raspberry Pi 4 Model B page](https://www.adafruit.com/product/4296). It prints the 4 GB price next to the 8 GB price, plus eight add-on prices and featured products. The purchases on it are **test registrations** made by the run's test issuer, with no real receipt. What the run proves is the consensus reading of the real current price. The demo store is the [PriceGuard Demo Store](https://yoyoblair333-wq.github.io/priceguard/store/), a clearly labelled demo page.

| # | Purchase | Validators read | Refund |
|---|---|---|---|
| 1 | Pi 4, **4 GB**, paid $135.00 | **PRICED $120.00** (quote: `4GB $120.00`) | **$15.00** |
| 2 | Pi 4, **8 GB**, same page, paid $199.00 | **PRICED $190.00** (`8GB $190.00`), not the 4 GB price | **$9.00** |
| 3 | Pi 4, 4 GB, paid $120.00 | PRICED $120.00 | $0, no drop |
| 4 | Demo lamp, Matte Black, paid $89.00 | **PRICED $69.00**. Ignored: the "Was $89.00", the $62.10 member price, the $17.25 instalments and the $99 brass finish | **$20.00** |
| 5 | Demo headphones, paid $149.00 | **UNAVAILABLE** (sold out), even though $149.00 is printed | $0 |

All rounds reached consensus (MAJORITY_AGREE). Refunds are paid in test GEN at 0.01 GEN per USD; the buyers withdrew theirs. Transaction hashes, votes and the state read back from the chain are in [docs/LIVE_EVIDENCE.md](docs/LIVE_EVIDENCE.md).

## State design

- **Plan:** issuer, name, covered hosts, `coverage_bp`, `window_days`, `min_drop_cents`, `cap_cents`, `wei_per_usd`, `open_demo`, and the pool's `balance` and `paid`.
- **Purchase:** plan, buyer, canonical URL, item, variant, currency, `paid_cents`, `purchased_on`, `lowest_cents`, `credited_cents`, `credited_wei`, checks, and the last record and detail. The full history of every check (time, record, detail, cents credited) is kept as well.
- One registration per buyer, page and variant. A host is covered only if it is the plan's host or a subdomain of it (`evilshop.example.com.attacker.io` is not). The pool can never go negative: if it runs dry, a refund is paid up to what is left.

## Quickstart

```bash
pip install -r requirements-dev.txt
genvm-lint check contracts/price_guard.py
pytest tests/direct -q                      # 59 direct-mode tests (real GenVM SDK, web + model mocked)
python scripts/live_run.py                  # deploy + real price checks on studionet (free test GEN)
python scripts/evidence.py                  # re-render docs/LIVE_EVIDENCE.md from chain data
cd web && npm install && npm run build      # rebuild docs/app.js (the GitHub Pages app)
```

## Try it in the browser

1. Open https://yoyoblair333-wq.github.io/priceguard/ and click **Create / load test key**. This makes a studionet burner key in your browser, funded by the free faucet.
2. Keep the prefilled demo lamp ("paid" $89.00, a few days ago) and click **Register purchase**.
3. Click **Check price** on your purchase. Validators read the demo store page, agree on $69.00 and refund the $20.00 drop to your test key.
4. Click **Withdraw**.

## Honest scope

- The price paid is attested by the issuer, who saw the receipt. The contract proves the **current** price.
- One page per purchase. Retailers that block bots or render prices only in JavaScript may read as `UNREADABLE`, which pays nothing.
- Testnet only. Not affiliated with any retailer. MIT licence.
