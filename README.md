# GigShield 🛡️
### AI-Powered Parametric Income Protection for Food Delivery Workers
### Team ZenVyte | Guidewire DEVTrails 2026

> GigShield is an AI-powered parametric micro-insurance platform that automatically compensates food delivery workers when external disruptions such as heavy rain, extreme heat, pollution, or government restrictions prevent them from earning income.

> *"A delivery worker is stuck during a Chennai thunderstorm. They didn't file a claim. They didn't call anyone. Their phone just buzzed — ₹160 credited. GigShield works so they don't have to."*

---

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Our Solution](#our-solution)
3. [Why GigShield Is Innovative](#why-gigshield-is-innovative)
4. [Delivery Worker Persona](#delivery-worker-persona)
5. [Parametric Triggers](#parametric-triggers)
6. [Weekly Premium Model](#weekly-premium-model)
7. [AI/ML Architecture](#aiml-architecture)
8. [Smart Validation Layer](#smart-validation-layer)
9. [Zero-Touch Claim Flow](#zero-touch-claim-flow)
10. [Platform & Tech Stack](#platform--tech-stack)
11. [System Architecture](#system-architecture)
12. [Dashboards](#dashboards)
13. [Coverage Scope & Exclusions](#coverage-scope--exclusions)
14. [Financial & Business Model](#financial--business-model)
15. [45-Day Development Roadmap](#45-day-development-roadmap)
16. [Strategy Video](#strategy-video)

---

## Problem Statement

India's food delivery ecosystem runs on the backs of hundreds of thousands of gig workers delivering for platforms like **Zomato** and **Swiggy**. These workers are entirely dependent on daily deliveries for their income — there is no salary, no paid leave, and no safety net.

External disruptions — heavy monsoon rain, extreme heat, cyclone alerts, air quality emergencies, government-declared curfews — can bring delivery activity to a complete halt. When that happens, a food delivery worker loses **₹300–₹650 in a single evening**, with no recourse and no compensation.

**The numbers:**
- **5 crore+** gig workers in India with zero income protection
- **₹300–₹650** lost per disruption event per worker
- **0** traditional insurance products covering short-term gig income loss
- **Weeks** to process a manual insurance claim today

**The gap:** Traditional insurance products do not cover short-term income disruption for gig workers. Filing a manual claim is too complex, too slow, and too uncertain for someone who needs money today, not next month.

**GigShield exists to close that gap** — through automated, parametric micro-insurance that pays out before the worker even has to ask.

---

## Our Solution

GigShield is an **AI-powered parametric micro-insurance platform** built exclusively for food delivery partners on Zomato and Swiggy.

### ⚡ How GigShield Works (At a Glance)

#### User → AI Risk Score → Weekly Plan → Monitor Data → Trigger → Auto Claim → Payout 

Instead of requiring manual claim submission, GigShield:

- Continuously monitors verified external data sources (IMD, CPCB, government alerts) cross-validated with satellite and radar-based private weather APIs
- Applies disruption detection at **micro-zone level (2–5 km radius)** rather than city or pincode level, ensuring granular accuracy
- Automatically detects when a disruption threshold is crossed **and persists for 15–30 minutes** in a worker's delivery zone
- Verifies the worker's GPS location, behavioral signals, and fraud score in real time
- Triggers an instant partial income top-up — with near real-time payout processing and zero human intervention

The worker's only job is to subscribe to a weekly plan. Everything else is automated.

**Key differentiators:**
- Every trigger is independently verifiable through government or third-party APIs — no platform data, no subjective metrics
- Multi-source data validation prevents false triggers from API delays or outages
- Micro-zone precision (2–5 km) avoids city-level inaccuracies — rain in one street doesn't incorrectly trigger payouts 5 km away
- Time-based confirmation window (15–30 min) eliminates brief weather spikes from triggering payouts
- ML-driven dynamic zone-based pricing makes the model financially sustainable
- Predictive disruption alerts warn workers 24–48 hours before an event
- Zero-touch claim experience — no forms, no uploads, no waiting
- GigShield operates as a technology distribution platform — all policies underwritten by a licensed IRDAI insurer partner
- Actuarially grounded pricing model maintaining 50–72% loss ratio across all plans

---

## Why GigShield Is Innovative

GigShield introduces a new insurance model tailored specifically for gig economy workers.

Key innovations include:

- **Parametric Insurance Model** — payouts triggered by objective external data instead of manual claims
- **Zero-Touch Claims** — workers never need to file forms or upload documents
- **AI-Driven Risk Pricing** — machine learning assigns optimal plan tiers based on zone risk
- **Micro-Zone Precision** — disruption detection at 2–5 km zone level, not city or pincode level
- **Multi-Source Validation** — cross-validates IMD/CPCB with satellite/radar APIs to handle data delays
- **Time-Based Confirmation** — disruptions must persist 15–30 minutes before triggering payout (no false triggers)
- **Context-Aware Delivery Logic** — compares disruption duration against average delivery time before triggering
- **Anonymized Crowd Signal Validation** — aggregated zone-level behavioral signals from multiple workers improve accuracy without privacy risk
- **Predictive Disruption Alerts** — workers receive warnings 24–48 hours before disruptions
- **Fraud Detection Engine** — anomaly detection protects insurers from fraudulent claims
- **Near Real-Time Micro-Payouts** — automated top-up payouts processed instantly with no human intervention
- **Actuarially Viable Micro-Premiums** — all plans maintain 50–72% annual loss ratio, insurer-partner ready

This transforms insurance from **reactive claims processing** into **proactive financial protection**.

---

## Delivery Worker Persona

### Illustrative Persona — Swiggy Delivery Partner, Chennai

| Attribute | Detail |
|---|---|
| Age | Mid-20s |
| City | Chennai (operates across Velachery, Adyar, T. Nagar zones) |
| Daily Hours | 9am – 9pm |
| Daily Deliveries | 20–28 |
| Daily Earnings | ₹900 – ₹1,300 |
| Weekly Earnings | ₹6,500 – ₹9,000 |
| Hourly Earnings | ₹112 – ₹162/hour |
| Peak Vulnerability | Evening hours (7–10pm) — Chennai's heaviest rainfall window |
| Financial Buffer | None. One disrupted week = missed EMI or skipped meals. |

> Note: This persona is representative of the food delivery partners GigShield is designed to protect across Zomato and Swiggy.

### Disruption Scenario

It's a Tuesday evening in August. A delivery partner is midway through their shift in Velachery. Rainfall crosses 40mm in 2 hours. Restaurants begin closing. The Swiggy app goes quiet. They pull over under a shelter.

**In the old world:** ₹500 lost with no way to recover it.

**With GigShield:** Phone buzzes. *"🌧️ Heavy rain detected in your zone. ₹160 credited to your account. Stay safe."* They didn't do anything. GigShield did.

---

## Parametric Triggers

> **Design Principle:** Every trigger must be an objective, externally verifiable event from a government or accredited third-party source. GigShield does not use platform demand data, traffic metrics, or any subjective signal.

### Trigger Table

| # | Disruption Event | Data Source | Threshold | Confirmation Window | Payout Trigger |
|---|---|---|---|---|---|
| 1 | Heavy Rainfall | OpenWeatherMap API + IMD + Satellite Radar API | Rainfall > 35mm within 3 hours in worker's micro-zone | Persists for 15–30 minutes | Per disruption hour (up to plan cap) |
| 2 | Extreme Heat | IMD API + Private Weather API | Sustained temperature > 43°C for 2+ hours | Persists for 30 minutes | Per disruption hour (up to plan cap) |
| 3 | Severe Air Pollution | CPCB AQI API + OpenAQ | AQI > 300 (Hazardous category) | Confirmed across 2+ sources | Per disruption hour (up to plan cap) |
| 4 | Cyclone / Flood Alert | IMD Disaster Alert Feed + NDMA | Orange or Red alert issued for worker's district | Alert active for 30+ minutes | Full weekly plan cap triggered immediately |
| 5 | Government Curfew / Hartal | NDMA public alert feed + admin-confirmed flag | Section 144 order or state-declared shutdown in worker's zone | Admin-verified flag | Full weekly plan cap triggered immediately |

### Why These Triggers Are Compliant

Each trigger satisfies all three compliance requirements:

1. **Externally verifiable** — sourced from IMD, CPCB, NDMA, or a government-issued order. Not derived from platform data.
2. **Parametric** — defined by a measurable threshold that is either crossed or not. No subjective assessment.
3. **Causally linked to income loss** — each event directly prevents outdoor delivery work, causing loss of hourly wages.

### Time-Based Confirmation

A key safeguard against false triggers: GigShield validates that the disruption condition **persists for 15–30 minutes** before any payout is initiated.

| Scenario | Result |
|---|---|
| Rain for 5 minutes → clears | ❌ No payout — condition did not persist |
| Rain for 30 minutes continuous | ✅ Trigger confirmed — payout initiated |
| AQI spikes briefly, recovers | ❌ No payout — single-source spike |
| AQI confirmed across 2+ sources for 20+ min | ✅ Trigger confirmed |

---

## Smart Validation Layer

While designing GigShield, we identified real-world challenges in relying solely on external data sources. To ensure accuracy, fairness, and reliability, we built a **multi-layer validation approach** on top of the parametric trigger system.

### 1. Multi-Source Data Reliability

**Problem:** External APIs (IMD, CPCB, etc.) may sometimes be delayed, unavailable, or return stale data — a rare but real scenario.

**Solution:**
- Primary source: Government APIs (IMD, CPCB, NDMA)
- Secondary validation: Private satellite and radar-based weather APIs
- Cross-verify disruption signals across at least 2 independent sources before triggering any payout
- If primary API is down, fallback to satellite API — no single point of failure

---

### 2. Micro-Zone Precision (2–5 km Granularity)

**Problem:** Pincode-level or city-level data is too coarse. Rain may be heavy in one neighborhood but absent 3 km away. Using city-wide data creates wrong triggers for workers outside the actual disruption area.

**Solution:**
- Workers are mapped using pincode as a base, then placed into smaller **micro-zones of 2–5 km radius**
- Disruption detection and trigger logic operates at micro-zone level, not city or pincode level
- Each worker's zone centroid is used for precise weather API queries
- Workers at the boundary of a disruption zone receive proportional signal weighting

**Impact:** Prevents workers in unaffected areas from receiving incorrect payouts — and ensures workers in genuinely affected areas are not missed.

---

### 3. Time-Based Confirmation (False Trigger Prevention)

**Problem:** Brief weather spikes (a 5-minute shower, a momentary AQI spike) should not trigger payouts — they don't meaningfully disrupt delivery work.

**Solution:**
- Every disruption trigger is subject to a **15–30 minute persistence check**
- Only after the condition remains at or above the threshold continuously is the payout initiated
- Duration counter starts at first threshold breach; resets if condition drops below threshold

| Duration | Action |
|---|---|
| < 15 minutes | Monitoring — no trigger |
| 15–30 minutes | Confirmation window — alert worker |
| > 30 minutes | Trigger confirmed — claim initiated |

---

### 4. Context-Aware Delivery Time Logic

**Problem:** Not all disruptions meaningfully impact delivery income. A 20-minute disruption has a very different impact from a 3-hour disruption on a worker mid-shift.

**Solution:**
- Compare disruption duration against the worker's average delivery time (estimated at 30–45 minutes per delivery)
- If disruption duration is shorter than average delivery time → low impact, no payout triggered
- If disruption duration significantly exceeds average delivery time → high income impact, payout initiated
- Payout scales proportionally with verified disruption hours, up to the plan cap

---

### 5. Anonymized Zone-Level Crowd Signal Validation

**Problem:** External data alone may not fully capture ground conditions — API data can lag real conditions by 10–20 minutes in rapidly changing weather.

**Solution:**
- In addition to external APIs, GigShield uses **anonymized, aggregated behavioral signals** from multiple active workers in the same micro-zone
- Signals tracked (at zone level, never individual level):
  - Reduced average movement speed across workers in zone
  - Inactivity spikes — multiple workers showing near-zero movement simultaneously
  - Location clustering — workers gathering under shelters
- These signals are **never linked to individual identities** — only zone-level patterns are used
- No platform data (Zomato/Swiggy orders) is accessed or required
- Crowd signal is used as a **secondary confirmation layer**, not as the primary trigger

**Privacy guarantee:** No individual worker is tracked or identified. Behavioral signals are aggregated at zone level and discarded after the disruption window closes.

**Why this works:** If 8 workers in Velachery simultaneously drop to near-zero speed during a rainfall event, it strongly confirms the disruption is real — even if the weather API is lagging by 15 minutes.

---

### Combined Validation Logic

GigShield requires **all five layers** to pass before a claim is approved:

```
Layer 1: External API threshold crossed (IMD / CPCB / NDMA)
       ↓
Layer 2: Cross-verified by secondary source (satellite / radar API)
       ↓
Layer 3: Condition persists 15–30 minutes (time-based confirmation)
       ↓
Layer 4: Worker GPS confirmed inside affected micro-zone
       ↓
Layer 5: Anonymized zone crowd signal confirms disruption (optional boost)
       ↓
       ✅ Claim auto-approved — payout initiated
```

This layered approach ensures:
- High accuracy — multiple independent data points required
- Low false-positive rate — brief spikes filtered out
- Real-world reliability — crowd signals compensate for API lag
- Privacy compliance — no individual tracking, no platform dependency

---

## Weekly Premium Model

### Design Philosophy

GigShield is a **partial income top-up**, not a full income replacement product. This distinction is fundamental to the model's actuarial viability and regulatory simplicity.

A worker earning ₹112/hour who loses 2.5 hours to a rain event loses approximately ₹280. GigShield's Standard plan returns ₹160 of that — covering ~57% of the loss at a weekly cost of ₹79 (the price of roughly 2 deliveries). This is a clear, honest value proposition: partial protection at a price any active delivery worker can afford.

Full income replacement at these premium levels would produce loss ratios exceeding 300%, making the product uninsurable. GigShield's tiered top-up model maintains loss ratios of 50–72% across all plans — within standard parametric insurance underwriting thresholds.

### Actuarial Foundation

**Base assumptions — Chennai food delivery zones (IMD 10-year historical data):**

| Parameter | Value | Basis |
|---|---|---|
| Disruption events/month — monsoon season (Jun–Nov) | 3.0 events | IMD Chennai 10-yr average, conservative |
| Disruption events/month — off-season (Dec–May) | 0.5 events | IMD Chennai historical |
| Annual disruption events per worker | **21 events/year** | (3.0 × 6) + (0.5 × 6) = 21 |
| Average disruption duration | **2.5 hours** | IMD urban rainfall event data — most Chennai events are 1.5–3 hrs |
| Annual disruption hours per worker | **52.5 hours/year** | 21 × 2.5 = 52.5 |
| Worker's average hourly income | ₹112/hour | ₹900/day ÷ 8 working hours |
| Annual income lost per worker (avg) | **₹5,880/year** | 52.5 hrs × ₹112 |
| Weekly income lost (annualised average) | **₹113/week** | ₹5,880 ÷ 52 weeks |

**Target loss ratio:** 65% (industry benchmark for parametric micro-insurance products in India)

```
Viable weekly premium = Expected weekly claim cost ÷ Target Loss Ratio

For Standard plan (targeting ~70% income loss coverage):
  Expected weekly claim cost = ₹113 × 0.70 = ₹79.10
  Viable premium = ₹79.10 ÷ 0.65 ≈ ₹79/week ✓
```

### How GigShield Pays — Hourly Micro-Payout Model

GigShield compensates workers based on **disruption hours**, not full days. This approach:
- Is fairer to workers — most disruptions last 2–4 hours, not a full day
- Is financially sustainable — hourly caps limit worst-case payout exposure
- Aligns with parametric principles — payout is proportional to the verified disruption window

### The 5 Plans

| Plan | Weekly Premium | Hourly Payout | Max Hours/Week | Max Weekly Payout | Target User |
|---|---|---|---|---|---|
| 🌱 Starter | ₹35/week | ₹25/hour | 2 hours | ₹50 | New workers, very low-risk zones |
| 🔵 Basic | ₹55/week | ₹30/hour | 3 hours | ₹90 | Part-time workers, low-risk zones |
| 🟡 Standard | ₹79/week | ₹40/hour | 4 hours | ₹160 | Full-time workers, urban zones |
| 🟠 Premium | ₹109/week | ₹50/hour | 4 hours | ₹200 | High-earning full-time partners |
| 🔴 Elite | ₹149/week | ₹60/hour | 5 hours | ₹300 | Coastal / flood-prone high-risk zones |

### Loss Ratio Proof — All Plans

| Plan | Annual Premium | Expected Annual Claim | Annual Loss Ratio | Heavy Monsoon LR (+40% events) |
|---|---|---|---|---|
| 🌱 Starter | ₹1,820 | ₹1,312 | 72% ✅ | ~85% ✅ |
| 🔵 Basic | ₹2,860 | ₹1,575 | 55% ✅ | ~77% ✅ |
| 🟡 Standard | ₹4,108 | ₹2,100 | 51% ✅ | ~72% ✅ |
| 🟠 Premium | ₹5,668 | ₹2,625 | 46% ✅ | ~65% ✅ |
| 🔴 Elite | ₹7,748 | ₹4,134 | 53% ✅ | ~75% ✅ |

> Elite plan uses a 1.4× disruption frequency multiplier for coastal/flood-prone zones (Royapuram, Foreshore Estate, Marina). Heavy monsoon scenario assumes 40% more disruption events than baseline. All plans remain within insurer-acceptable loss ratios even in worst-case years.

### Worker Affordability Check

| Plan | Weekly Premium | % of Weekly Earnings (₹7,000 avg) | Deliveries to cover it | Weekly protection value |
|---|---|---|---|---|
| 🌱 Starter | ₹35 | 0.5% | ~1 delivery | ₹50 top-up |
| 🔵 Basic | ₹55 | 0.8% | ~1.5 deliveries | ₹90 top-up |
| 🟡 Standard | ₹79 | 1.1% | ~2 deliveries | ₹160 top-up |
| 🟠 Premium | ₹109 | 1.6% | ~3 deliveries | ₹200 top-up |
| 🔴 Elite | ₹149 | 2.1% | ~4 deliveries | ₹300 top-up |

All plans remain under 2.5% of weekly earnings — the affordability threshold for micro-insurance adoption in India. The Standard plan at ₹79/week costs the equivalent of 2 deliveries and protects against a ₹280 income loss in a disruption week.

### Why Weekly Pricing

Gig workers on Zomato/Swiggy operate on a weekly earnings and payout cycle. Daily premiums create friction. Monthly premiums are too large a commitment for workers with variable income. Weekly pricing — small enough to feel negligible (less than the earnings from 1–2 deliveries), meaningful enough to provide real coverage — matches how delivery workers actually think about money.

---

## Demo Scenario

Example demonstration of GigShield in action:

1. Ravi subscribes to the **Standard Plan (₹79/week)** using the GigShield mobile app.
2. GigShield continuously monitors weather data using **OpenWeatherMap + IMD APIs + satellite radar API** (polled every 15 minutes), applied at **Ravi's micro-zone (Velachery, 3 km radius)**.
3. Rainfall in Ravi's micro-zone crosses the **35mm disruption threshold**.
4. GigShield initiates a **15–30 minute time confirmation window** — rainfall must persist to confirm real disruption.
5. Rain persists for 30+ minutes. Secondary source (radar API) confirms. Crowd signal: 7 workers in zone show near-zero movement.
6. The platform verifies Ravi's **GPS location** is within the affected micro-zone.
7. Fraud detection model evaluates the claim — fraud score: **14/100 (clean)**.
8. The claim is automatically approved. Disruption duration verified: **4 hours**.
9. Standard plan payout: **4 hours × ₹40/hour = ₹160**.
10. Insurer partner releases the payout through **Razorpay Sandbox**.

Worker receives notification:
```
🌧️ Heavy rain detected in your zone (Velachery, Chennai).
₹160 credited to your account.
Disruption: 4 hours covered under Standard Plan.
Stay safe, Ravi.
```

---

## Financial & Business Model

### GigShield is a Technology Platform — Not an Insurer

GigShield operates as an **insurance technology distribution platform**, not as the underwriter. This is the same model used by Toffee Insurance, Riskcovry, and Plum in India.

```
Worker pays weekly premium
         ↓
Licensed IRDAI Insurer Partner (e.g., Digit Insurance / Acko)
holds all premium capital and pays all claims
         ↓
GigShield earns a 10% platform distribution fee per active policy
         ↓
GigShield's claims liability: ₹0
```

### GigShield Revenue Per Policy Per Week

| Plan | Weekly Premium | GigShield Fee (10%) | Insurer Net Premium | Insurer Loss Ratio on Net |
|---|---|---|---|---|
| 🌱 Starter | ₹35 | ₹3.50 | ₹31.50 | ~72% ✅ |
| 🔵 Basic | ₹55 | ₹5.50 | ₹49.50 | ~55% ✅ |
| 🟡 Standard | ₹79 | ₹7.90 | ₹71.10 | ~51% ✅ |
| 🟠 Premium | ₹109 | ₹10.90 | ₹98.10 | ~46% ✅ |
| 🔴 Elite | ₹149 | ₹14.90 | ₹134.10 | ~53% ✅ |

> The insurer's net premium (after GigShield's 10% distribution fee) still supports healthy loss ratios at all tiers — making GigShield a commercially attractive partner for IRDAI-licensed insurers.

### Revenue at Scale

| Active Workers | Avg Weekly Fee | Weekly Platform Revenue | Annual Revenue |
|---|---|---|---|
| 1,000 | ₹8.20 | ₹8,200 | ₹42,64,000 |
| 10,000 | ₹8.20 | ₹82,000 | ₹4,26,40,000 |
| 1,00,000 | ₹8.20 | ₹8,20,000 | ₹42,64,00,000 |

**GigShield cannot go bankrupt from claims — because GigShield never pays claims.**

---

## AI/ML Architecture

GigShield integrates three purpose-built ML models.

---

### Model 1 — Zone Risk Classifier

**Purpose:** Recommend the most appropriate plan tier to each worker at onboarding based on their delivery micro-zone's historical disruption risk.

**Algorithm:** Random Forest Classifier

**Training Data:**
- IMD historical rainfall records (10 years, district-level, freely downloadable)
- CPCB AQI historical data (public)
- NDMA flood zone maps
- Historical cyclone track data (IMD)

**Input Features:**

| Feature | Description |
|---|---|
| Zone latitude / longitude | Geographic position of delivery micro-zone centroid (2–5 km radius) |
| Historical disruption events/month (12-month rolling) | Frequency of past disruption events in that micro-zone |
| Proximity to water bodies | Distance to nearest river, lake, or coastline (flood proxy) |
| Zone elevation | Low elevation = poor drainage = higher flood risk |
| Month of year | Monsoon seasonality weighting |
| Historical AQI exceedance days | Pollution risk profile for the zone |

**Output:** Risk score 0.0–1.0 → plan recommendation

| Risk Score | Plan Recommendation |
|---|---|
| < 0.25 | 🌱 Starter / 🔵 Basic |
| 0.25 – 0.55 | 🟡 Standard |
| 0.55 – 0.75 | 🟠 Premium |
| > 0.75 | 🔴 Elite |

**Why Random Forest:** Handles mixed numerical and categorical features well, produces interpretable feature importance scores, and does not require large datasets — suitable for zone-level historical data volumes.

---

### Model 2 — Fraud Detection Engine

**Purpose:** Score every auto-triggered claim for fraud before payout is released.

**Algorithm:** Isolation Forest (behavioral anomaly detection) + deterministic rule layer (hard rejects)

#### Hard Reject Rules (Deterministic — Applied First)

| Rule | Logic |
|---|---|
| No verified trigger event | If no IMD/CPCB threshold breach recorded in worker's micro-zone on claim day → automatic rejection |
| GPS pincode mismatch | If worker's GPS location at trigger time does not overlap with disruption event micro-zone → automatic rejection |
| Claim cap exceeded | If worker has already reached max hours for the week → automatic rejection |
| Plan not active | If worker's weekly plan has expired → automatic rejection |
| Time confirmation not met | If disruption persisted for fewer than 15 minutes → automatic rejection |

#### Anomaly Scoring (Isolation Forest — Applied After Hard Rules Pass)

| Feature | Fraud Signal |
|---|---|
| GPS velocity during claimed disruption window | Speed > 5 km/h during disruption = actively working, not disrupted |
| Claim frequency (last 4 weeks) | 4 consecutive weekly claims with no variation = anomalous |
| Claim timing relative to trigger | Claim initiated before trigger threshold crossed = suspicious |
| Device fingerprint | Multiple accounts on same device = duplicate registration fraud |
| Historical claim approval rate | Consistent 100% approval rate over months = flag for review |
| Zone crowd signal disagreement | Worker claims disruption, but zone crowd signal shows no inactivity spike = flag |

**Output:** Fraud score 0–100

| Score | Action |
|---|---|
| 0 – 30 | Auto-approve. Payout released immediately. |
| 30 – 70 | Human review queue (admin dashboard). |
| > 70 | Auto-reject. Worker notified with appeal option. |

---

### Worker Eligibility & Trust Score System

**Purpose:** Maintain a persistent, dynamic trust score per worker built from genuine past activity — used to determine payout eligibility before the fraud detection model even runs. This is not a per-claim check. It is a running reputation score that accumulates across weeks.

**Why this exists:** Fraud detection alone scores each claim in isolation. A sophisticated fraudster could pass individual claim checks while still exhibiting suspicious patterns across weeks. The eligibility system catches this by looking at the full history of a worker's behaviour — not just their latest claim.

#### How the Trust Score Is Built

Every worker has a Trust Score from **0 to 100**, updated weekly based on four combined factors:

| Factor | What It Measures | Trust Impact |
|---|---|---|
| **Weeks Actively Subscribed** | Continuous weeks with an active plan (no gaps) | +points per unbroken week |
| **Genuine Past Claims** | Claims that were auto-approved with clean fraud scores | +points per verified clean claim |
| **Consistent GPS Activity** | Regular work-hour GPS movement matching a delivery worker's pattern | +points for consistent activity |
| **Low Fraud Score History** | Rolling average of fraud scores across all past claims | -points if fraud scores are elevated |

All four factors are combined into a single weighted Trust Score. No single factor dominates — a worker must show genuine behaviour across all dimensions.

#### Trust Score Tiers

| Trust Score | Tier | Eligibility Status |
|---|---|---|
| 75 – 100 | 🟢 Trusted | Full auto-approval. Highest payout priority. |
| 50 – 74 | 🔵 Established | Auto-approval. Standard processing. |
| 25 – 49 | 🟡 Building | Claim goes to manual review queue before payout. |
| 0 – 24 | 🔴 Restricted | Claim goes to manual review. Payout capped at 50% of plan maximum. |

#### New Worker Handling (No History)

A worker with no claim history starts with a **Provisional Trust Score of 40 (Building tier)**. They can claim immediately from Week 1, but with a **reduced payout cap of 50%** of their plan maximum until they build 3 weeks of genuine activity.

This approach:
- Does not punish new workers for being new
- Limits insurer exposure on unproven accounts
- Rewards consistent genuine workers with full benefits quickly

| Week | Status | Payout Cap |
|---|---|---|
| Week 1 (new) | Provisional — no history | 50% of plan max |
| Week 2–3 | Building — limited history | 75% of plan max |
| Week 4+ (clean record) | Established or Trusted | 100% of plan max |

#### How Low Eligibility Works

Workers in the **Building (25–49)** or **Restricted (0–24)** tier are not rejected — their claim is automatically routed to the **manual review queue** in the admin dashboard. A human reviewer checks the GPS trace, crowd signal data, and fraud score before approving or rejecting.

This means:
- No genuine worker is ever auto-rejected purely due to low trust score
- Suspicious workers face extra scrutiny without being unfairly blocked
- The insurer's fraud exposure is minimised at the eligibility gate, before individual claim checks run

#### Trust Score Recovery

A worker whose score has dropped due to flagged claims can recover by:
- Maintaining continuous active subscriptions without suspicious claims
- Passing manual review on subsequent claims (each clean manual-review approval restores points)
- Completing 4 consecutive clean weeks (automatic partial score restoration)

#### Combined Flow with Fraud Detection

```
Disruption trigger confirmed
          │
          ▼
┌─────────────────────────────┐
│  Eligibility Gate           │
│  Check worker Trust Score   │
│                             │
│  🟢 75–100 → Proceed        │
│  🔵 50–74  → Proceed        │
│  🟡 25–49  → Manual Review  │
│  🔴 0–24   → Manual Review  │
│             + 50% payout cap│
└──────────────┬──────────────┘
               │
               ▼
     Fraud Detection Model
     (Isolation Forest score)
               │
               ▼
     Payout decision
```

The eligibility gate runs **before** the fraud model — high-risk workers are flagged for human review before any automated payout logic runs.

---

### Model 3 — Predictive Disruption Alert Engine

**Purpose:** Forecast disruption probability 24–48 hours ahead for each delivery micro-zone, enabling proactive worker notifications and insurer risk preparation.

**Algorithm:** XGBoost on time-series weather features (LSTM evaluated as alternative in Phase 3)

**Training Data:** IMD 10-year historical weather records, seasonal cyclone patterns, monsoon onset/withdrawal historical dates

**Input Features:**
- 7-day rolling weather trend for the micro-zone
- Current IMD forecast data (temperature, rainfall probability, wind speed)
- Season flag (monsoon / pre-monsoon / winter)
- Zone historical disruption frequency by month
- Recent AQI trend
- Satellite-derived cloud cover and moisture indices

**Output:** Disruption probability score (0–100%) per micro-zone per day

**Worker-facing notification:**
> *"⚡ Storm likely in your delivery zone tomorrow 6–9pm. Probability: 78%. Your ₹160 coverage is active."*

**Admin-facing view:** City-wide heatmap showing predicted disruption risk for the next 48 hours at micro-zone level, enabling the insurer partner to pre-position liquidity for expected payouts.

---

## Zero-Touch Claim Flow

```
Worker subscribes to ₹79 Standard weekly plan on GigShield mobile app
           │
           ▼
GigShield backend polls OpenWeatherMap + IMD + Satellite API every 15 minutes
Applied at micro-zone level (2–5 km radius, not city/pincode)
           │
           ▼
7:23pm — Rainfall crosses 35mm threshold in worker's micro-zone
           │
           ▼
┌──────────────────────────────────────────────┐
│      Time-Based Confirmation Window          │
│  ⏱️ Monitoring for 15–30 minutes...          │
│  7:53pm — Rain persists. Threshold still met.│
│  Secondary source (radar API) confirms ✅    │
└──────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│           Automated Verification             │
│  ✅ Worker GPS in affected micro-zone?       │
│  ✅ Plan active this week?                   │
│  ✅ Hourly cap not yet reached?              │
│  ✅ Disruption persisted 30+ minutes?        │
│  ✅ Zone crowd signal confirms (7 workers    │
│     showing near-zero movement) ✅           │
│  ✅ Fraud score: 14/100 (clean)              │
│  ✅ No duplicate claim today?                │
└──────────────────────────────────────────────┘
           │
           ▼
   Claim auto-approved
           │
           ▼
   Disruption duration verified: 4 hours
   Payout: 4 hrs × ₹40/hr = ₹160
           │
           ▼
   Insurer partner releases payout
   Processed via Razorpay sandbox (near real-time)
           │
           ▼
   Firebase push notification sent:
   "🌧️ Heavy rain in your zone. ₹160 credited. Stay safe."
           │
           ▼
   Worker is home. Dry. Paid. Without filing a single form.
```

**Total time from disruption confirmation to payout initiation: near real-time. Zero human intervention. Zero forms.**

---

## Platform & Tech Stack

### Platform Strategy

GigShield is built on two platforms sharing a single backend:

| Platform | Target User | Purpose |
|---|---|---|
| **Mobile App (React Native)** | Delivery Workers | Onboarding, plan selection, disruption alerts, payout tracking |
| **Web App (React.js)** | Insurer / Admin | Micro-zone heatmap, policy portfolio, fraud queue, loss ratio analytics, predictive disruption map |

A shared **FastAPI backend** serves both platforms through a unified REST API. This architecture avoids duplication and ensures ML model outputs are consistent across both interfaces.

### Full Tech Stack

| Layer | Technology | Justification |
|---|---|---|
| Mobile Frontend | React Native | Single codebase for iOS + Android, fast iteration |
| Web Frontend | React.js | Component-based admin dashboard with map integration |
| Backend | Python FastAPI | ML-friendly, async support, high performance |
| Database | PostgreSQL | Relational — workers, policies, claims, payout records |
| ML Models | Scikit-learn (Random Forest, Isolation Forest), XGBoost | Production-grade libraries, well-documented |
| Weather API (Primary) | OpenWeatherMap (free tier) + IMD public data | Real-time conditions + historical training data |
| Weather API (Secondary) | Satellite/radar-based private weather API | Backup validation, handles IMD data delays |
| AQI API | CPCB AQI API + OpenAQ (free public APIs) | Government-verified pollution data, cross-validated |
| Disaster Alerts | NDMA public alert feed | Replaces manual curfew verification for Trigger #5 |
| Zone Mapping | Google Maps API + custom micro-zone segmentation (2–5 km) | Precise GPS zone verification beyond pincode level |
| Payments | Razorpay Sandbox (test mode) | Simulated near-real-time payout |
| Push Notifications | Firebase Cloud Messaging | Real-time worker alerts on mobile |
| Hosting | Railway / Render (free tier) | Fast deployment for hackathon demo |

---

## System Architecture

```
┌─────────────────────┐        ┌─────────────────────┐
│   Worker Mobile App  │        │   Admin Web App      │
│   (React Native)     │        │   (React.js)         │
└────────┬────────────┘        └──────────┬──────────┘
         │                                │
         └──────────────┬─────────────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │   FastAPI Backend     │
            │   (Python)            │
            └──────────┬────────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
   ┌──────────┐  ┌──────────┐  ┌──────────────────────┐
   │PostgreSQL│  │ ML Engine│  │Disruption Monitor    │
   │(Workers, │  │(Risk,    │  │(Polls APIs every     │
   │Policies, │  │Fraud,    │  │15 min at micro-zone  │
   │Claims)   │  │Predict)  │  │level — 2–5 km zones) │
   └──────────┘  └──────────┘  └──────┬───────────────┘
                                       │
                    ┌──────────────────┼──────────────────────┐
                    ▼                  ▼                       ▼
           ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐
           │OpenWeatherMap│  │  CPCB AQI    │  │  IMD / NDMA          │
           │+ IMD Weather │  │  API +OpenAQ │  │  Alert Feed          │
           │+ Satellite   │  │              │  │                      │
           │  Radar API   │  │              │  │                      │
           └──────────────┘  └──────────────┘  └──────────────────────┘
                                       │
                                       ▼
                            ┌──────────────────────────┐
                            │  Multi-Layer Validation  │
                            │  • Time confirmation     │
                            │  • Cross-source verify   │
                            │  • GPS micro-zone check  │
                            │  • Crowd signal layer    │
                            │  • Fraud score engine    │
                            └──────────┬───────────────┘
                                       │
                                       ▼
                            ┌─────────────────────┐
                            │  IRDAI Insurer       │
                            │  Partner Payout API  │
                            └──────────┬──────────┘
                                       │
                                       ▼
                            ┌─────────────────────┐
                            │  Razorpay Sandbox    │
                            │  (Payout Processing) │
                            └──────────┬──────────┘
                                       │
                                       ▼
                            ┌─────────────────────┐
                            │  Firebase FCM        │
                            │  (Worker Alert)      │
                            └─────────────────────┘
```

---

## Dashboards

### Worker Mobile Dashboard

- **Plan Status Badge** — Active 🟢 / Expired 🔴 / Disruption in Progress ⚡
- **Current Plan Card** — Plan name, weekly premium, hourly rate, hours remaining this week
- **My Micro-Zone** — Visual map of the worker's assigned 2–5 km delivery zone
- **This Week's Disruptions** — Events detected in your delivery micro-zone
- **Payouts Received** — Timeline of all credited amounts with disruption type and hours covered
- **Predictive Alert Panel** — "Heavy rain likely tomorrow 6–9pm in your zone (78% probability)"
- **Earnings Protected Counter** — "You've saved ₹640 this month with GigShield"
- **Upgrade Plan** — One-tap upgrade to higher tier before next week
- **Renew Plan** — One-tap weekly renewal before plan expires

### Admin / Insurer Web Dashboard

- **City Micro-Zone Risk Heatmap** — Live + 48-hour predictive disruption risk by micro-zone (2–5 km cells)
- **Active Policies by Plan** — Breakdown across all 5 plan tiers with counts and premium volume
- **Premium Collected This Week** — Total across all plans (gross and net of GigShield fee)
- **Claims Today** — Auto-approved / In review / Auto-rejected with hourly breakdown
- **Loss Ratio by Zone** — Real-time portfolio loss ratio, segmented by delivery micro-zone
- **Fraud Review Queue** — Claims in the 30–70 score band with GPS trace, timing evidence, crowd signal comparison
- **ML Model Health** — Confidence scores, feature drift indicators, retraining alerts
- **Predicted Payout Exposure** — Expected payouts for next 48 hours based on disruption forecast
- **Data Source Status** — Live status of all API feeds (IMD, CPCB, NDMA, satellite API) — flags delays

---

## Coverage Scope & Exclusions

### What GigShield Covers

GigShield covers **income lost by food delivery workers during verified external disruptions** that prevent delivery activity. Coverage is parametric — payouts are triggered by objective data thresholds that persist for a minimum confirmation window (15–30 minutes), not manual claim assessment. Payouts are calculated on a per-hour basis up to the plan's weekly maximum.

GigShield provides a **partial income top-up** — not full income replacement. This distinction keeps the product actuarially viable, affordable, and insurer-partnerable.

### What GigShield Explicitly Does NOT Cover

> GigShield strictly excludes coverage for: vehicle repairs, bike maintenance, fuel costs, medical expenses, accident compensation, health insurance, life insurance, platform-side demand fluctuations, traffic congestion, technical issues with the delivery app, and any event not independently verifiable through a government or accredited third-party data source.
>
> All coverage is limited exclusively to verified external environmental and government-declared civic disruptions that directly prevent outdoor delivery work and cause loss of income.

This exclusion boundary is by design — it keeps GigShield compliant, financially sustainable, and operationally simple.

---

## 45-Day Development Roadmap

### Phase 1 — Ideation & Foundation (Weeks 1–2 | March 4–20)
*Theme: Ideate & Know Your Delivery Worker*

- [x] Problem research and gig worker persona analysis
- [x] Insurance model design — 5 plan tiers, hourly payout model, actuarial loss ratio proof
- [x] ML model architecture planning (Zone Risk Classifier, Fraud Detection, Predictive Alert)
- [x] Tech stack selection and platform strategy
- [x] System architecture design
- [x] GitHub repository setup with full README
- [x] Financial & business model — IRDAI partner insurer structure, 10% platform fee model
- [x] Smart Validation Layer design — multi-source reliability, micro-zone precision, time confirmation, crowd signals
- [ ] Minimal prototype: Worker onboarding screen + plan selection UI (React Native)
- [ ] Strategy video (2 minutes)

### Phase 2 — Automation & Protection (Weeks 3–4 | March 21–April 4)
*Theme: Protect Your Worker*

- [ ] Worker registration and KYC flow (simulated Aadhaar verification)
- [ ] Insurance policy management (create, view, renew, upgrade weekly plan)
- [ ] Zone Risk Classifier model — trained and deployed for plan recommendation at onboarding
- [ ] Micro-zone segmentation layer — divide city into 2–5 km zones, map each worker to micro-zone
- [ ] OpenWeatherMap + IMD + satellite radar API integration and disruption detection engine (15-min polling)
- [ ] Time-based confirmation engine (15–30 min persistence check before trigger fires)
- [ ] Hourly payout calculation engine (duration × hourly rate, capped at plan maximum)
- [ ] Claims management system (auto-trigger pipeline: time confirm → cross-source verify → GPS check → fraud check → approve → payout)
- [ ] Razorpay sandbox payout integration
- [ ] Firebase push notification setup
- [ ] 2-minute demo video

### Phase 3 — Scale & Optimise (Weeks 5–6 | April 5–17)
*Theme: Perfect for Your Worker*

- [ ] Advanced fraud detection — Isolation Forest model trained and deployed (GPS spoofing, crowd signal disagreement detection)
- [ ] Anonymized zone-level crowd signal validation layer — aggregate worker behavioral signals per micro-zone
- [ ] Predictive disruption alert engine — XGBoost model, 48-hour micro-zone-level forecast
- [ ] Context-aware delivery time logic — compare disruption duration vs average delivery time before triggering
- [ ] Intelligent admin dashboard (micro-zone heatmap, loss ratio by zone, fraud queue, predictive payout exposure map, API status panel)
- [ ] Worker dashboard — all 5 plan cards, micro-zone map, earnings protected counter, alert panel, upgrade flow
- [ ] NDMA alert feed integration for Trigger #5 (automated curfew/hartal detection)
- [ ] Full system integration testing across all 5 disruption triggers
- [ ] 5-minute demo video (simulated rainstorm → 30-min confirmation → auto-claim → 4-hour payout walkthrough)
- [ ] Final pitch deck (PDF) — persona, AI architecture, fraud model, smart validation layer, business viability

---

## Strategy Video

🎥 *2-minute strategy video — link to be added upon submission (before March 20, EOD).*

---

## Hackathon Prototype Disclaimer

This project is a prototype built for the **Guidewire DEVTrails 2026 Hackathon**.

For demonstration purposes:
- Insurance payouts are simulated using **Razorpay Sandbox**
- Worker identity verification is mocked
- External data sources are integrated using publicly available APIs (OpenWeatherMap, CPCB, IMD, NDMA)
- Satellite/radar secondary API is simulated in demo using cached weather data
- Anonymized crowd signal layer is simulated using synthetic zone-level movement data
- ML models are trained on IMD/CPCB public historical data

In a real deployment, GigShield would integrate with a **licensed IRDAI insurance partner** to underwrite policies and process real claim payouts.

---

## About This Project

Built for the **Guidewire DEVTrails 2026 Pan-India University Hackathon**.

**Team Name:** ZenVyte

**Team Members:**
- Dhayananth N *(Team Lead)*
- Mowlieswaran G
- Arun Kumar S
- Karthick V
- Hardik Muthusamy

**Problem Statement:** AI-Powered Insurance for India's Gig Economy

**Team Persona Focus:** Food Delivery Workers (Zomato / Swiggy)

**Platform:** Web (Admin) + Mobile (Workers)

**Repository:** This repository will be used across all three phases of the hackathon. Commit history will reflect iterative development through each phase.

---

*Build fast. Spend smart. Protect every delivery worker. 🛡️*
*Team ZenVyte — DEVTrails 2026*
