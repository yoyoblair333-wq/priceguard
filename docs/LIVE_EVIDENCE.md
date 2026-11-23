# Live evidence (GenLayer studionet)

Rendered by `scripts/evidence.py` from [`docs/live/run.json`](live/run.json), which `scripts/live_run.py` wrote from chain data. Studionet is a test network: GEN here has no value. All keys are throwaway test keys.

| Item | Value |
|---|---|
| Contract | `0xAeD6034E3aB271822c67De82A36B4270B9b4a94E` |
| Explorer | https://explorer-studio.genlayer.com/address/0xAeD6034E3aB271822c67De82A36B4270B9b4a94E |
| Network | studionet (chain 61999, https://studio.genlayer.com/api) |
| issuer (throwaway key) | `0xF73f87dABA85ACc440Adc57580eF5d309c03f79d` |
| buyer (throwaway key) | `0x0fF851cd935eD160C048c7312Dcda0ef97Be82AF` |
| buyer2 (throwaway key) | `0x59C124c3A5D2D47B7EE49D2d89D10A28ac629147` |

## Transactions

| Step | Tx | Status | Consensus | Execution | Validator votes |
|---|---|---|---|---|---|
| deploy | `0x1f505d0b11d67d6bdb855838b3fc29679eeeb4ce18303f52bdf2f162d7c5d626` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| open_plan #1 (100 % of the drop, 60 days, adafruit.com, min $1, cap $50; fund 2 GEN) | `0x85ff821a0dcdf6027aca3a0103826cacad70cbc9e3dbdb4853e9d386615b6699` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| register purchase #1: Pi 4 4 GB paid $135.00 (test registration) | `0x1189b389864e925593805de06ff760dfc13d76311d8a7b8a4b3e96bb10b03963` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| register purchase #2: Pi 4 8 GB paid $199.00 (test registration, same page) | `0xc20b536b58103270b45f6f4b6e1979fad37e2729b041170da5fd1d8ed4a46ce8` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| register purchase #3: Pi 4 4 GB paid $120.00, no drop (test registration) | `0x49b4cff0560df186397740e3be9d1c9bc6d8f838afa1e25ce0361d49972b2460` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| check #1 (consensus price read) | `0x3ea8411db20514a7022986e66399477df990037995f73877663ea46c4d725e93` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| check #2 (consensus price read) | `0xeb9165e104f2b3e4a325a6f3555ee4cb28e8b36ae2019c129b8ec87c09c7eb61` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| check #3 (consensus price read) | `0xc45c150120d55688fce31da74ad53a5f3907120e43de2b32562f55ca11e75259` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| withdraw (buyer) | `0x5d53eebf1bbff80c96e26ebbf47976a05676dbf5bbdae0886add8ebd9c338561` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| withdraw (buyer2) | `0x048ee305d4381fb7d71730900e76f4722a3792ff4026f5b159d60df885d84a6d` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| open_plan #2 demo (open to anyone, PriceGuard Demo Store; fund 2 GEN) | `0x69f4141e6f538ccc5f55c5607ce89c7c7e03e13ccf23eb4ccb20aadc3d0bf8c1` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, agree, agree |
| register purchase #4: demo lamp paid $89.00, page now $69.00 sale | `0x7bcd744571bf188f810d2676d5b0c374b87161f7185e8cd4b63c0dca23747553` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| register purchase #5: demo headphones paid $149.00, now sold out | `0x272208a2e25b468ca48f2489cc51e5542aa474fb5c0702079202542eeef7f0ca` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| check #4 (consensus price read) | `0x9e5ba90dfc6d2936ba7bc86b920e943aa3a1f5d6c310b080667e6f25e6026cfb` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| check #5 (consensus price read) | `0xbbbb62aa222310596a5b070adb0f10ba3162b10fe20f1b889ebdf831a006f237` | FINALIZED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, idle, idle |
| withdraw (buyer, demo-store refund) | `0xd06c3b015c62d827437512a67c4aa4dc5fb434abd8f5569726de10c1e7fddbd1` | ACCEPTED | MAJORITY_AGREE | SUCCESS | agree, agree, agree, agree, agree |

## State read back from the contract

### purchases

```json
{
 "1": {
  "buyer": "0x0fF851cd935eD160C048c7312Dcda0ef97Be82AF",
  "checks": 1,
  "credited_cents": 1500,
  "credited_wei": "150000000000000000",
  "currency": "USD",
  "history": [
   {
    "at": "2026-11-23T04:48:41Z",
    "credited_cents": 1500,
    "detail": {
     "currency": "USD",
     "model_price": "120.00",
     "model_status": "PRICED",
     "quote": "4GB $120.00"
    },
    "record": {
     "price_cents": 12000,
     "status": "PRICED"
    }
   }
  ],
  "id": 1,
  "item": "Raspberry Pi 4 Model B - 4 GB RAM",
  "last_check": "2026-11-23T04:48:41Z",
  "last_detail": {
   "currency": "USD",
   "model_price": "120.00",
   "model_status": "PRICED",
   "quote": "4GB $120.00"
  },
  "last_record": {
   "price_cents": 12000,
   "status": "PRICED"
  },
  "lowest_cents": 12000,
  "paid_cents": 13500,
  "plan_id": 1,
  "purchased_on": "2026-11-10",
  "registered_at": "2026-11-23T04:48:13Z",
  "url": "https://www.adafruit.com/product/4296",
  "variant": "4GB",
  "window_ends": "2027-01-10T00:00:00Z"
 },
 "2": {
  "buyer": "0x59C124c3A5D2D47B7EE49D2d89D10A28ac629147",
  "checks": 1,
  "credited_cents": 900,
  "credited_wei": "90000000000000000",
  "currency": "USD",
  "history": [
   {
    "at": "2026-11-23T04:48:56Z",
    "credited_cents": 900,
    "detail": {
     "currency": "USD",
     "model_price": "190.00",
     "model_status": "PRICED",
     "quote": "4GB $120.00 8GB $190.00 In stock"
    },
    "record": {
     "price_cents": 19000,
     "status": "PRICED"
    }
   }
  ],
  "id": 2,
  "item": "Raspberry Pi 4 Model B - 4 GB RAM",
  "last_check": "2026-11-23T04:48:56Z",
  "last_detail": {
   "currency": "USD",
   "model_price": "190.00",
   "model_status": "PRICED",
   "quote": "4GB $120.00 8GB $190.00 In stock"
  },
  "last_record": {
   "price_cents": 19000,
   "status": "PRICED"
  },
  "lowest_cents": 19000,
  "paid_cents": 19900,
  "plan_id": 1,
  "purchased_on": "2026-11-10",
  "registered_at": "2026-11-23T04:48:22Z",
  "url": "https://www.adafruit.com/product/4296",
  "variant": "8GB",
  "window_ends": "2027-01-10T00:00:00Z"
 },
 "3": {
  "buyer": "0x59C124c3A5D2D47B7EE49D2d89D10A28ac629147",
  "checks": 1,
  "credited_cents": 0,
  "credited_wei": "0",
  "currency": "USD",
  "history": [
   {
    "at": "2026-11-23T04:49:21Z",
    "credited_cents": 0,
    "detail": {
     "currency": "USD",
     "model_price": "120.00",
     "model_status": "PRICED",
     "quote": "Raspberry Pi 4 Model B - 4 GB RAM Product ID: 4296 $120.00"
    },
    "record": {
     "price_cents": 12000,
     "status": "PRICED"
    }
   }
  ],
  "id": 3,
  "item": "Raspberry Pi 4 Model B - 4 GB RAM",
  "last_check": "2026-11-23T04:49:21Z",
  "last_detail": {
   "currency": "USD",
   "model_price": "120.00",
   "model_status": "PRICED",
   "quote": "Raspberry Pi 4 Model B - 4 GB RAM Product ID: 4296 $120.00"
  },
  "last_record": {
   "price_cents": 12000,
   "status": "PRICED"
  },
  "lowest_cents": 12000,
  "paid_cents": 12000,
  "plan_id": 1,
  "purchased_on": "2026-11-12",
  "registered_at": "2026-11-23T04:48:32Z",
  "url": "https://www.adafruit.com/product/4296",
  "variant": "4GB",
  "window_ends": "2027-01-12T00:00:00Z"
 },
 "4": {
  "buyer": "0x0fF851cd935eD160C048c7312Dcda0ef97Be82AF",
  "checks": 1,
  "credited_cents": 2000,
  "credited_wei": "200000000000000000",
  "currency": "USD",
  "history": [
   {
    "at": "2026-11-23T04:52:39Z",
    "credited_cents": 2000,
    "detail": {
     "currency": "USD",
     "model_price": "69.00",
     "model_status": "PRICED",
     "quote": "Colour: Matte Black Was $89.00 $69.00 Holiday sale In stock."
    },
    "record": {
     "price_cents": 6900,
     "status": "PRICED"
    }
   }
  ],
  "id": 4,
  "item": "Arc LED Desk Lamp",
  "last_check": "2026-11-23T04:52:39Z",
  "last_detail": {
   "currency": "USD",
   "model_price": "69.00",
   "model_status": "PRICED",
   "quote": "Colour: Matte Black Was $89.00 $69.00 Holiday sale In stock."
  },
  "last_record": {
   "price_cents": 6900,
   "status": "PRICED"
  },
  "lowest_cents": 6900,
  "paid_cents": 8900,
  "plan_id": 2,
  "purchased_on": "2026-11-15",
  "registered_at": "2026-11-23T04:52:20Z",
  "url": "https://yoyoblair333-wq.github.io/priceguard/store/desk-lamp.html",
  "variant": "Matte Black",
  "window_ends": "2027-01-15T00:00:00Z"
 },
 "5": {
  "buyer": "0x59C124c3A5D2D47B7EE49D2d89D10A28ac629147",
  "checks": 1,
  "credited_cents": 0,
  "credited_wei": "0",
  "currency": "USD",
  "history": [
   {
    "at": "2026-11-23T04:52:59Z",
    "credited_cents": 0,
    "detail": {
     "currency": "USD",
     "model_price": "149.00",
     "model_status": "UNAVAILABLE",
     "quote": "SKU Q1-WL $149.00 Sold out."
    },
    "record": {
     "price_cents": 0,
     "status": "UNAVAILABLE"
    }
   }
  ],
  "id": 5,
  "item": "Quiet One Wireless Headphones",
  "last_check": "2026-11-23T04:52:59Z",
  "last_detail": {
   "currency": "USD",
   "model_price": "149.00",
   "model_status": "UNAVAILABLE",
   "quote": "SKU Q1-WL $149.00 Sold out."
  },
  "last_record": {
   "price_cents": 0,
   "status": "UNAVAILABLE"
  },
  "lowest_cents": 14900,
  "paid_cents": 14900,
  "plan_id": 2,
  "purchased_on": "2026-11-15",
  "registered_at": "2026-11-23T04:52:30Z",
  "url": "https://yoyoblair333-wq.github.io/priceguard/store/headphones.html",
  "variant": "",
  "window_ends": "2027-01-15T00:00:00Z"
 }
}
```

### balance_before_withdraw_buyer

```json
"200000000000000000"
```

### balance_before_withdraw_buyer2

```json
"0"
```

### plans

```json
{
 "1": {
  "balance": "1760000000000000000",
  "cap_cents": 5000,
  "coverage_bp": 10000,
  "created_at": "2026-11-23T04:48:04Z",
  "hosts": [
   "adafruit.com"
  ],
  "id": 1,
  "issuer": "0xF73f87dABA85ACc440Adc57580eF5d309c03f79d",
  "min_drop_cents": 100,
  "name": "PriceGuard Test Card",
  "open_demo": false,
  "paid": "240000000000000000",
  "purchases": 3,
  "wei_per_usd": "10000000000000000",
  "window_days": 60
 },
 "2": {
  "balance": "1800000000000000000",
  "cap_cents": 5000,
  "coverage_bp": 10000,
  "created_at": "2026-11-23T04:52:10Z",
  "hosts": [
   "yoyoblair333-wq.github.io"
  ],
  "id": 2,
  "issuer": "0xF73f87dABA85ACc440Adc57580eF5d309c03f79d",
  "min_drop_cents": 100,
  "name": "PriceGuard Demo Plan",
  "open_demo": true,
  "paid": "200000000000000000",
  "purchases": 2,
  "wei_per_usd": "10000000000000000",
  "window_days": 60
 }
}
```

### stats

```json
{
 "check_gap_hours": 12,
 "currencies": [
  "AUD",
  "CAD",
  "EUR",
  "GBP",
  "USD"
 ],
 "max_checks": 20,
 "owner": "0xF73f87dABA85ACc440Adc57580eF5d309c03f79d",
 "plans": 2,
 "purchases": 5,
 "schema": "priceguard.v1",
 "statuses": [
  "PRICED",
  "UNAVAILABLE",
  "AMBIGUOUS",
  "UNREADABLE"
 ]
}
```

### balance_after_final_withdraw_buyer

```json
"0"
```

Run finished at 2026-11-23T04:53:38Z.
