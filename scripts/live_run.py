#!/usr/bin/env python3
"""
live_run.py - deploy PriceGuard to GenLayer studionet and run price checks on real pages.

    python scripts/live_run.py [--contract 0x...] [--skip-demo] [--out docs/live/run.json]

Throwaway keys are created (and funded for free with sim_fundAccount) and kept in
.priceguard/keys.json, which is gitignored. Every value written to the output file is
what the chain returned. Re-running resumes: steps with a tx hash are not sent again.

Real retailer page: Adafruit's Raspberry Pi 4 Model B page (https://www.adafruit.com/product/4296),
which prints the 4 GB price next to the 8 GB price, add-ons and featured products.
The purchases on it are TEST registrations by the run's test issuer (no real receipt);
what the run proves is the consensus reading of the real current price.
Demo store: the PriceGuard Demo Store on GitHub Pages (a clearly labelled demo).
"""

import argparse
import json
import os
import sys
import time

from eth_account import Account
from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet
from genlayer_py.types import TransactionStatus as S

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYS = os.path.join(ROOT, ".priceguard", "keys.json")
WEI = 10**18
WPU = 10**16                     # 1 USD of refund = 0.01 test GEN
EXPLORER = "https://explorer-studio.genlayer.com"
PI = "https://www.adafruit.com/product/4296"
STORE = "https://yoyoblair333-wq.github.io/priceguard/store/"


def say(*a):
    print(*a, flush=True)


def hexs(tx):
    h = tx.hex() if hasattr(tx, "hex") else str(tx)
    return h if h.startswith("0x") else "0x" + h


def jsonable(x):
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    if isinstance(x, (bytes, bytearray)):
        return "0x" + bytes(x).hex()
    if isinstance(x, (str, int, float, bool)) or x is None:
        return x
    return str(x)


def keys():
    os.makedirs(os.path.dirname(KEYS), exist_ok=True)
    if os.path.exists(KEYS):
        with open(KEYS) as fh:
            k = json.load(fh)
    else:
        k = {}
    for role in ("issuer", "buyer", "buyer2"):
        if role not in k:
            k[role] = "0x" + bytes(create_account().key).hex()
    with open(KEYS, "w") as fh:
        json.dump(k, fh)
    return {r: Account.from_key(v) for r, v in k.items()}


def submit(send, attempts=5):
    for i in range(attempts):
        try:
            return send()
        except Exception as e:
            if i == attempts - 1:
                raise
            say(f"  submit failed ({str(e)[:140]}); retrying in 10s")
            time.sleep(10)


def summarize(t):
    cd = t.get("consensus_data") or {}
    votes = sorted((cd.get("votes") or {}).values())
    lr = cd.get("leader_receipt")
    lr = lr[0] if isinstance(lr, list) and lr else (lr or {})
    blob = json.dumps(jsonable(t))
    err = None
    i = blob.find("[EXPECTED]")
    if i >= 0:
        err = blob[i:i + 160].split('"')[0].split("\\")[0]
    return {"status": t.get("status_name"), "result": t.get("result_name"),
            "execution": lr.get("execution_result"), "votes": votes, "error": err}


def wait(client, tx, until=S.ACCEPTED):
    client.wait_for_transaction_receipt(transaction_hash=tx, status=until, interval=5000, retries=360)
    return client.get_transaction(tx)


class Run:
    def __init__(self, path):
        self.path = path
        self.s = json.load(open(path)) if os.path.exists(path) else {}
        self.s.setdefault("network", "studionet (chain 61999, https://studio.genlayer.com/api)")
        self.s.setdefault("steps", [])

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w") as fh:
            json.dump(jsonable(self.s), fh, indent=1)
            fh.write("\n")

    def do(self, client, label, send):
        for st in self.s["steps"]:
            if st["step"] == label and st.get("tx"):
                say(f"[skip] {label}: {st['tx']}")
                return st
        say(f"[send] {label}")
        tx = hexs(submit(send))
        st = {"step": label, "tx": tx, "sent_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        self.s["steps"].append(st)
        self.save()
        t = wait(client, tx)
        st.update(summarize(t))
        self.save()
        say(f"  {tx} {st['status']} {st['result']} exec={st['execution']} votes={st['votes']} err={st['error']}")
        return st


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--contract")
    ap.add_argument("--skip-demo", action="store_true")
    ap.add_argument("--out", default=os.path.join(ROOT, "docs", "live", "run.json"))
    a = ap.parse_args()
    k = keys()
    run = Run(a.out)
    cl = {r: create_client(chain=studionet, account=acct) for r, acct in k.items()}
    run.s["roles"] = {r: acct.address for r, acct in k.items()}
    for r, acct in k.items():
        if not run.s.get("funded_" + r):
            cl[r].fund_account(acct.address, 20 * WEI)
            run.s["funded_" + r] = True
    run.save()
    iss = cl["issuer"]
    addr = a.contract or run.s.get("contract")
    if not addr:
        code = open(os.path.join(ROOT, "contracts", "price_guard.py"), encoding="utf-8").read()
        st = run.do(iss, "deploy", lambda: iss.deploy_contract(code=code, args=[]))
        t = iss.get_transaction(st["tx"])
        addr = (t.get("data") or {}).get("contract_address") or t.get("recipient") or t.get("to_address")
        run.s["contract"] = addr
        run.save()
    run.s["explorer"] = f"{EXPLORER}/address/{addr}"
    say("contract", addr)

    def read(fn, args=None):
        return iss.read_contract(address=addr, function_name=fn, args=args or [])

    def w(role, label, fn, args, value=0):
        c = cl[role]
        return run.do(c, label, lambda: c.write_contract(address=addr, function_name=fn, args=args, value=value))

    b1, b2 = run.s["roles"]["buyer"], run.s["roles"]["buyer2"]
    if read("stats")["plans"] < 1:
        w("issuer", "open_plan #1 (100 % of the drop, 60 days, adafruit.com, min $1, cap $50; fund 2 GEN)", "open_plan",
          ["PriceGuard Test Card", ["adafruit.com"], 10_000, 60, 100, 5_000, WPU, False], value=2 * WEI)
    purchases = [
        ("purchase #1: Pi 4 4 GB paid $135.00 (test registration)", [1, b1, PI, "Raspberry Pi 4 Model B - 4 GB RAM", "4GB", "USD", 13_500, "2026-11-10"]),
        ("purchase #2: Pi 4 8 GB paid $199.00 (test registration, same page)", [1, b2, PI, "Raspberry Pi 4 Model B - 4 GB RAM", "8GB", "USD", 19_900, "2026-11-10"]),
        ("purchase #3: Pi 4 4 GB paid $120.00, no drop (test registration)", [1, b2, PI, "Raspberry Pi 4 Model B - 4 GB RAM", "4GB", "USD", 12_000, "2026-11-12"]),
    ]
    for i, (label, args) in enumerate(purchases):
        if read("stats")["purchases"] < i + 1:
            w("issuer", "register " + label, "register_purchase", args)
    for i in range(len(purchases)):
        if read("get_purchase", [i + 1])["checks"] < 1:
            w("buyer", f"check #{i + 1} (consensus price read)", "check", [i + 1])
    if not a.skip_demo:
        if read("stats")["plans"] < 2:
            w("issuer", "open_plan #2 demo (open to anyone, PriceGuard Demo Store; fund 2 GEN)", "open_plan",
              ["PriceGuard Demo Plan", ["yoyoblair333-wq.github.io"], 10_000, 60, 100, 5_000, WPU, True], value=2 * WEI)
        demo = [("buyer", "purchase #4: demo lamp paid $89.00, page now $69.00 sale",
                 [2, b1, STORE + "desk-lamp.html", "Arc LED Desk Lamp", "Matte Black", "USD", 8_900, "2026-11-15"]),
                ("buyer2", "purchase #5: demo headphones paid $149.00, now sold out",
                 [2, b2, STORE + "headphones.html", "Quiet One Wireless Headphones", "", "USD", 14_900, "2026-11-15"])]
        for j, (role, label, args) in enumerate(demo):
            if read("stats")["purchases"] < 4 + j:
                w(role, "register " + label, "register_purchase", args)
        for cid in (4, 5):
            if read("get_purchase", [cid])["checks"] < 1:
                w("buyer", f"check #{cid} (consensus price read)", "check", [cid])
    n = read("stats")["purchases"]
    run.s["purchases"] = {str(i): read("get_purchase", [i]) for i in range(1, n + 1)}
    for role in ("buyer", "buyer2"):
        bal = int(read("balance_of", [run.s["roles"][role]]))
        run.s["balance_before_withdraw_" + role] = str(bal)
        if bal > 0:
            w(role, f"withdraw ({role})", "withdraw", [])
    run.s["plans"] = {str(i): read("get_plan", [i]) for i in range(1, read("stats")["plans"] + 1)}
    run.s["stats"] = read("stats")
    for st in run.s["steps"]:
        try:
            st["latest"] = summarize(iss.get_transaction(st["tx"]))
        except Exception as e:
            st["latest"] = {"error": str(e)[:120]}
    run.s["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    run.save()
    say("wrote", a.out)


if __name__ == "__main__":
    main()
