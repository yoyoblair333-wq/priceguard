// PriceGuard web app. Reads the live studionet contract with genlayer-js and lets a visitor
// register a demo purchase and run a consensus price check with a per-browser burner key (testnet only).
import { createClient, createAccount, generatePrivateKey } from "genlayer-js";
import { studionet } from "genlayer-js/chains";

export const CONTRACT = "0xAeD6034E3aB271822c67De82A36B4270B9b4a94E";
const RPC = "https://studio.genlayer.com/api";
const EXPLORER = "https://explorer-studio.genlayer.com";
const KEY = "priceguard.studionet-burner.v1";
const WEI = 10n ** 18n;

const $ = (id) => document.getElementById(id);
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const plain = (v) => {
  if (v instanceof Map) return Object.fromEntries([...v].map(([k, x]) => [k, plain(x)]));
  if (Array.isArray(v)) return v.map(plain);
  if (typeof v === "bigint") return Number(v) <= Number.MAX_SAFE_INTEGER ? Number(v) : v.toString();
  return v;
};
const gen = (wei) => {
  const w = BigInt(wei || 0);
  const whole = w / WEI, frac = (w % WEI).toString().padStart(18, "0").replace(/0+$/, "").slice(0, 4);
  return frac ? `${whole}.${frac} GEN` : `${whole} GEN`;
};
const money = (cents, cur = "USD") => (cur === "EUR" ? "€" : cur === "GBP" ? "£" : "$") + (cents / 100).toFixed(2);

const reader = createClient({ chain: studionet });
let writer = null, account = null;

function burner() {
  let k = localStorage.getItem(KEY);
  if (!k) { k = generatePrivateKey(); localStorage.setItem(KEY, k); }
  account = createAccount(k);
  writer = createClient({ chain: studionet, account });
  $("me").textContent = account.address;
  return account;
}

async function read(fn, args = []) {
  return plain(await reader.readContract({ address: CONTRACT, functionName: fn, args }));
}

async function fund(addr) {
  await fetch(RPC, { method: "POST", headers: { "content-type": "application/json" },
    body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: "sim_fundAccount", params: [addr, 10 * 1e18] }) }).catch(() => {});
}

async function send(fn, args, label) {
  const log = $("log");
  if (!writer) burner();
  log.textContent = `${label}: funding test key…`;
  await fund(account.address);
  log.textContent = `${label}: sending…`;
  try {
    const hash = await writer.writeContract({ address: CONTRACT, functionName: fn, args, value: 0n });
    log.innerHTML = `${esc(label)}: tx <code>${esc(hash)}</code> sent, waiting for validators…`;
    const r = await writer.waitForTransactionReceipt({ hash, status: "ACCEPTED", interval: 4000, retries: 200 });
    const res = r?.consensus_data?.leader_receipt?.[0]?.execution_result ?? r?.result_name ?? "";
    log.innerHTML = `${esc(label)}: tx <code>${esc(hash)}</code> accepted (${esc(res)}).`;
  } catch (e) {
    log.textContent = `${label} failed: ${String(e?.message || e).slice(0, 300)}`;
  }
  await refresh();
}

function planCard(p) {
  return `<article class="card">
    <h3>#${p.id} · ${esc(p.name)}${p.open_demo ? ' <span class="tag ok">open demo</span>' : ""}</h3>
    <dl>
      <dt>Covers</dt><dd>${p.hosts.map(esc).join(", ")}</dd>
      <dt>Terms</dt><dd>${p.coverage_bp / 100}% of the drop · ${p.window_days} days · min drop ${money(p.min_drop_cents)} · cap ${money(p.cap_cents)} per purchase</dd>
      <dt>Pool</dt><dd><b class="ok">${gen(p.balance)}</b> · refunded ${gen(p.paid)} · ${p.purchases} purchase(s)</dd>
    </dl></article>`;
}

function row(c, now) {
  const r = c.last_record, d = c.last_detail || {};
  const next = c.last_check ? new Date(Date.parse(c.last_check) + 12 * 3600e3).toISOString().slice(0, 19) + "Z" : "";
  let act = "";
  if (now >= c.window_ends) act = '<span class="muted">window closed</span>';
  else if (!next || now >= next) act = `<button data-act="check" data-id="${c.id}">Check price</button>`;
  else act = `<span class="muted">next check ${esc(next.slice(5, 16).replace("T", " "))} UTC</span>`;
  const cls = !r ? "" : r.status === "PRICED" ? "ok" : "no";
  return `<tr>
    <td>#${c.id}</td>
    <td><a href="${esc(c.url)}" target="_blank" rel="noopener">${esc(c.item)}</a>${c.variant ? ` <span class="tag">${esc(c.variant)}</span>` : ""}<br><span class="muted">plan #${c.plan_id} · bought ${esc(c.purchased_on)}</span></td>
    <td>${money(c.paid_cents, c.currency)}</td>
    <td>${r ? `<b class="${cls}">${esc(r.status)}</b>${r.status === "PRICED" ? " " + money(r.price_cents, c.currency) : ""}` : "-"}${d.quote ? `<br><q>${esc(d.quote.slice(0, 80))}</q>` : ""}${d.why ? `<br><span class="muted">${esc(d.why)}</span>` : ""}<br><span class="muted">${c.checks} check(s)</span></td>
    <td>${money(c.lowest_cents, c.currency)}</td>
    <td class="ok">${money(c.credited_cents, c.currency)}<br><span class="muted">${gen(c.credited_wei)}</span></td>
    <td>${act}</td></tr>`;
}

async function refresh() {
  try {
    const [stats, plans, pur] = await Promise.all([read("stats"), read("list_plans"), read("list_purchases")]);
    $("stats").textContent = `${stats.plans} plan(s) · ${stats.purchases} purchase(s) · one check per purchase every ${stats.check_gap_hours} h`;
    $("plans").innerHTML = plans.map(planCard).join("") || "<p class='muted'>No plans yet.</p>";
    const now = new Date().toISOString().slice(0, 19) + "Z";
    $("purchases").innerHTML = pur.map((c) => row(c, now)).join("") || "<tr><td colspan=7 class='muted'>No purchases yet.</td></tr>";
    const cur = $("plan").value;
    $("plan").innerHTML = plans.filter((p) => p.open_demo).map((p) => `<option value="${p.id}">#${p.id} ${esc(p.name)}</option>`).join("");
    if (cur) $("plan").value = cur;
    if (account) {
      const bal = await read("balance_of", [account.address]);
      $("bal").textContent = gen(bal);
      $("withdraw").disabled = BigInt(bal) <= 0n;
    }
  } catch (e) {
    $("stats").textContent = "Could not read the contract: " + String(e?.message || e).slice(0, 200);
  }
}

document.addEventListener("click", (ev) => {
  const b = ev.target.closest("button[data-act]");
  if (b) send(b.dataset.act, [Number(b.dataset.id)], `${b.dataset.act} #${b.dataset.id}`);
});
$("buyform").addEventListener("submit", (ev) => {
  ev.preventDefault();
  if (!account) burner();
  const f = new FormData(ev.target);
  send("register_purchase", [Number(f.get("plan")), account.address, f.get("url"), f.get("item"), f.get("variant") || "", "USD",
    Math.round(Number(f.get("paid")) * 100), f.get("day")], "register purchase");
});
$("wallet").addEventListener("click", () => { burner(); refresh(); });
$("withdraw").addEventListener("click", () => send("withdraw", [], "withdraw"));
$("addr").innerHTML = `<a href="${EXPLORER}/address/${CONTRACT}" target="_blank" rel="noopener"><code>${CONTRACT}</code></a>`;
document.querySelector('input[name="day"]').value = new Date(Date.now() - 3 * 86400e3).toISOString().slice(0, 10);
if (localStorage.getItem(KEY)) burner();
refresh();
setInterval(refresh, 30000);
