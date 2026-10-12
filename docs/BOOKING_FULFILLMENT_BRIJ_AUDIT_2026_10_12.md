# Flight booking escrow / external fulfilment review (2026-10-12)

**Why investigated**: The user previously kept "booking" among alternative real-money opportunities. BRIJ Travel claims customer-funded flight bookings are escrowed in Solana USDC, and an external fulfiller/recipe author can earn per successful paid order without conventional customer outreach. Unlike speculative yields, real customer orders could in principle support valuable rewards. **Finding: genuinely described settlement flow, but unavailable as a viable new operator earning route under $100/Nov 12 constraints.**

## First-party evidence (read-only review)

- [BRIJ Travel overview](https://docs.brij.fi/) describes an escrow order: customer locks USDC for ticket and fee, fulfiller claims with refundable/at-risk deposit, **must front airline charge on its own card**, and only receives released USDC when oracle confirms that a ticket was actually issued.
- [Fulfiller API rules](https://docs.brij.fi/docs/fulfillers) require **whitelisted partner wallet** and signed session, not a permissionless open list anyone can work on. It exposes existing search-intents / orders only to qualified partners. Leaving/failed order can forfeit deposit/standing.
- [Recipes](https://docs.brij.fi/docs/recipes) allow external code but require approved submitted recipe, payout wallet and a submission fee. The **current overview** states 0.01 USDC per review, whereas an older crawled fulfiller FAQ stated **1 USDC**; flag that as version drift and rely on current endpoint before payment.
- [Public bounty explorer](https://docs.brij.fi/bounties) documents settlement/refunds and individual on-chain Solscan links. At observation, recent visible order card top showed **settled 732.47 USDC on September 29, 2026**, but that is the **flight ticket/totals in escrow**, not the fulfiller's profit or reward; other entries were refunded/expired. No current unclaimed **newcomer-eligible** order was shown.
- [Public fulfilment funnel](https://docs.brij.fi/fulfillers) is more decisive: for **trip.com browser tier**, last 30 days **4 assigned, 0 booked, 0 captured**; all-time 18 assigned, 4 booked, 2 ticket-issued. For **us.trip.com**, also last 30d 4 assigned, 0 booked, 0 captured; all-time 18/4/2. The two underlying named domains may represent related supplier channels and must **not** be assumed independent volumes. These metrics are public first-party records, not independently reconstructed Solana transactions.
- The public recipe runner's last-30-day book task had **4/4 errors** for trip.com. Thus even privileged incumbents have operational difficulty, before external card/fronting risk.

## Economic and user access gates

- **Main blocker:** Full supplier fare is fronted with the fulfiller's **own payment card**, while customer USDC remains escrowed until ticket proof. This commonly exceeds the $100 maximum capital; refundable/forfeitable taker deposit adds risk. Do not assume wallet-only automation can issue airline tickets without card credit.
- External access requires *whitelisted* partner status. Signed API session and application onboarding would require user approval. A recipe requires approval and a fee, not automatically a share of all bookings.
- Largest order totals are not worker bounty. Platform commissions, supplier margins, payout timing, dispute/chargeback liability and clearing economics are unknown. Do **not** infer $900 worker income from $732.47 travel escrow.
- Observed last-30d capture volume = **zero for both listed supplier tiers**, so cannot claim repeated, immediate earning potential. No live affordable unclaimed client-funded booking was identified.
- Referral programme (20% of platform fee) is **excluded** because user rejects affiliate/customer-acquisition; rewards vest only after flown travel and exceed deadline unpredictably.

## Decision

**STOP for one-month $100 challenge.** Real USDC settlement architecture and recorded past paid airline tickets may exist, but paid bookings are not freely collectible, current throughput is effectively zero, new-partner whitelisting required, and own-card supplier settlement exceeds capital. This is a useful example of a verified buyer-funded *purchase amount* that is not independent-worker remuneration.

**Capital spent: $0. User earnings: $0.** No BRIJ account, booking, wallet funding, customer data handling, receipt submission or GitHub external PR made.

**Next falsification test for similar future platforms:** verify whether someone without a special partner key and without fronting supplier principal can receive a fixed fee (not full purchase total) from currently open funded orders. If not, reject before writing automation.
