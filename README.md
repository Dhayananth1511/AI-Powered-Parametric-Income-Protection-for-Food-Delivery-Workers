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
8. [Zero-Touch Claim Flow](#zero-touch-claim-flow)
9. [Platform & Tech Stack](#platform--tech-stack)
10. [System Architecture](#system-architecture)
11. [Dashboards](#dashboards)
12. [Coverage Scope & Exclusions](#coverage-scope--exclusions)
13. [Financial & Business Model](#financial--business-model)
14. [45-Day Development Roadmap](#45-day-development-roadmap)
15. [Strategy Video](#strategy-video)

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

Instead of requiring manual claim submission, GigShield:

- Continuously monitors verified external data sources (IMD, CPCB, government alerts)
- Automatically detects when a disruption threshold is crossed in a worker's delivery zone
- Verifies the worker's GPS location and fraud score in real time
- Triggers an instant partial income top-up — in under 30 seconds, with no human intervention

The worker's only job is to subscribe to a weekly plan. Everything else is automated.

**Key differentiators:**
- Every trigger is independently verifiable through government or third-party APIs — no platform data, no subjective metrics
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
- **Predictive Disruption Alerts** — workers receive warnings 24–48 hours before disruptions
- **Fraud Detection Engine** — anomaly detection protects insurers from fraudulent claims
- **Instant Micro-Payouts** — automated top-up payouts delivered in under 30 seconds
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

| # | Disruption Event | Data Source | Threshold | Payout Trigger |
|---|---|---|---|---|
| 1 | Heavy Rainfall | OpenWeatherMap API + IMD | Rainfall > 35mm within 3 hours in worker's pincode | Per disruption hour (up to plan cap) |
| 2 | Extreme Heat | IMD API | Sustained temperature > 43°C for 2+ hours | Per disruption hour (up to plan cap) |
| 3 | Severe Air Pollution | CPCB AQI API (free public API) | AQI > 300 (Hazardous category) | Per disruption hour (up to plan cap) |
| 4 | Cyclone / Flood Alert | IMD Disaster Alert Feed + NDMA | Orange or Red alert issued for worker's district | Full weekly plan cap triggered immediately |
| 5 | Government Curfew / Hartal | NDMA public alert feed + admin-confirmed flag | Section 144 order or state-declared shutdown in worker's zone | Full weekly plan cap triggered immediately |

### Why These Triggers Are Compliant

Each trigger satisfies all three compliance requirements:

1. **Externally verifiable** — sourced from IMD, CPCB, NDMA, or a government-issued order. Not derived from platform data.
2. **Parametric** — defined by a measurable threshold that is either crossed or not. No subjective assessment.
3. **Causally linked to income loss** — each event directly prevents outdoor delivery work, causing loss of hourly wages.

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
2. GigShield continuously monitors weather data using **OpenWeatherMap and IMD APIs** (polled every 15 minutes).
3. Rainfall in Ravi's delivery zone (Velachery pincode) crosses the **35mm disruption threshold**.
4. The platform verifies Ravi's **GPS location** is within the affected zone.
5. Fraud detection model evaluates the claim — fraud score: **14/100 (clean)**.
6. The claim is automatically approved. Disruption duration verified: **4 hours**.
7. Standard plan payout: **4 hours × ₹40/hour = ₹160**.
8. Insurer partner releases the payout through **Razorpay Sandbox**.

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

**Purpose:** Recommend the most appropriate plan tier to each worker at onboarding based on their delivery zone's historical disruption risk.

**Algorithm:** Random Forest Classifier

**Training Data:**
- IMD historical rainfall records (10 years, district-level, freely downloadable)
- CPCB AQI historical data (public)
- NDMA flood zone maps
- Historical cyclone track data (IMD)

**Input Features:**

| Feature | Description |
|---|---|
| Zone latitude / longitude | Geographic position of delivery zone centroid |
| Historical disruption events/month (12-month rolling) | Frequency of past disruption events in that zone |
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
| No verified trigger event | If no IMD/CPCB threshold breach recorded in worker's pincode on claim day → automatic rejection |
| GPS pincode mismatch | If worker's GPS location at trigger time does not overlap with disruption event pincode → automatic rejection |
| Claim cap exceeded | If worker has already reached max hours for the week → automatic rejection |
| Plan not active | If worker's weekly plan has expired → automatic rejection |

#### Anomaly Scoring (Isolation Forest — Applied After Hard Rules Pass)

| Feature | Fraud Signal |
|---|---|
| GPS velocity during claimed disruption window | Speed > 5 km/h during disruption = actively working, not disrupted |
| Claim frequency (last 4 weeks) | 4 consecutive weekly claims with no variation = anomalous |
| Claim timing relative to trigger | Claim initiated before trigger threshold crossed = suspicious |
| Device fingerprint | Multiple accounts on same device = duplicate registration fraud |
| Historical claim approval rate | Consistent 100% approval rate over months = flag for review |

**Output:** Fraud score 0–100

| Score | Action |
|---|---|
| 0 – 30 | Auto-approve. Payout released immediately. |
| 30 – 70 | Human review queue (admin dashboard). |
| > 70 | Auto-reject. Worker notified with appeal option. |

---

### Model 3 — Predictive Disruption Alert Engine

**Purpose:** Forecast disruption probability 24–48 hours ahead for each delivery zone, enabling proactive worker notifications and insurer risk preparation.

**Algorithm:** XGBoost on time-series weather features (LSTM evaluated as alternative in Phase 3)

**Training Data:** IMD 10-year historical weather records, seasonal cyclone patterns, monsoon onset/withdrawal historical dates

**Input Features:**
- 7-day rolling weather trend for the zone
- Current IMD forecast data (temperature, rainfall probability, wind speed)
- Season flag (monsoon / pre-monsoon / winter)
- Zone historical disruption frequency by month
- Recent AQI trend

**Output:** Disruption probability score (0–100%) per zone per day

**Worker-facing notification:**
> *"⚡ Storm likely in your delivery zone tomorrow 6–9pm. Probability: 78%. Your ₹160 coverage is active."*

**Admin-facing view:** City-wide heatmap showing predicted disruption risk for the next 48 hours, enabling the insurer partner to pre-position liquidity for expected payouts.

---

## Zero-Touch Claim Flow

```
Worker subscribes to ₹79 Standard weekly plan on GigShield mobile app
           │
           ▼
GigShield backend polls OpenWeatherMap + IMD every 15 minutes
           │
           ▼
7:23pm — Rainfall crosses 35mm threshold in worker's pincode
           │
           ▼
┌──────────────────────────────────────────┐
│           Automated Verification         │
│  ✅ Worker GPS in affected zone?         │
│  ✅ Plan active this week?               │
│  ✅ Hourly cap not yet reached?          │
│  ✅ Fraud score: 14/100 (clean)          │
│  ✅ No duplicate claim today?            │
└──────────────────────────────────────────┘
           │
           ▼
   Claim auto-approved in < 30 seconds
           │
           ▼
   Disruption duration verified: 4 hours
   Payout: 4 hrs × ₹40/hr = ₹160
           │
           ▼
   Razorpay sandbox triggers transfer
           │
           ▼
   Firebase push notification sent:
   "🌧️ Heavy rain in your zone. ₹160 credited. Stay safe."
           │
           ▼
   Worker is home. Dry. Paid. Without filing a single form.
```

**Total time from disruption detection to payout: under 30 seconds. Zero human intervention. Zero forms.**

---

## Platform & Tech Stack

### Platform Strategy

GigShield is built on two platforms sharing a single backend:

| Platform | Target User | Purpose |
|---|---|---|
| **Mobile App (React Native)** | Delivery Workers | Onboarding, plan selection, disruption alerts, payout tracking |
| **Web App (React.js)** | Insurer / Admin | Zone heatmap, policy portfolio, fraud queue, loss ratio analytics, predictive disruption map |

A shared **FastAPI backend** serves both platforms through a unified REST API. This architecture avoids duplication and ensures ML model outputs are consistent across both interfaces.

### Full Tech Stack

| Layer | Technology | Justification |
|---|---|---|
| Mobile Frontend | React Native | Single codebase for iOS + Android, fast iteration |
| Web Frontend | React.js | Component-based admin dashboard with map integration |
| Backend | Python FastAPI | ML-friendly, async support, high performance |
| Database | PostgreSQL | Relational — workers, policies, claims, payout records |
| ML Models | Scikit-learn (Random Forest, Isolation Forest), XGBoost | Production-grade libraries, well-documented |
| Weather API | OpenWeatherMap (free tier) + IMD public data | Real-time conditions + historical training data |
| AQI API | CPCB AQI API / OpenAQ (free public APIs) | Government-verified pollution data |
| Disaster Alerts | NDMA public alert feed | Replaces manual curfew verification for Trigger #5 |
| Location | Google Maps API | GPS zone verification, delivery area mapping |
| Payments | Razorpay Sandbox (test mode) | Simulated instant payout |
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
   ┌──────────┐  ┌──────────┐  ┌──────────────┐
   │PostgreSQL│  │ ML Engine│  │Disruption    │
   │(Workers, │  │(Risk,    │  │Monitor       │
   │Policies, │  │Fraud,    │  │(Polls APIs   │
   │Claims)   │  │Predict)  │  │every 15 min) │
   └──────────┘  └──────────┘  └──────┬───────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    ▼                  ▼                   ▼
           ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
           │OpenWeatherMap│  │  CPCB AQI    │  │  IMD / NDMA      │
           │+ IMD Weather │  │  API         │  │  Alert Feed      │
           └──────────────┘  └──────────────┘  └──────────────────┘
                                       │
                                       ▼
                            ┌─────────────────────┐
                            │  Claim Trigger &     │
                            │  Fraud Check Engine  │
                            └──────────┬──────────┘
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
- **This Week's Disruptions** — Events detected in your delivery zone
- **Payouts Received** — Timeline of all credited amounts with disruption type and hours covered
- **Predictive Alert Panel** — "Heavy rain likely tomorrow 6–9pm in your zone (78% probability)"
- **Earnings Protected Counter** — "You've saved ₹640 this month with GigShield"
- **Upgrade Plan** — One-tap upgrade to higher tier before next week
- **Renew Plan** — One-tap weekly renewal before plan expires

### Admin / Insurer Web Dashboard

- **City Zone Risk Heatmap** — Live + 48-hour predictive disruption risk by pincode
- **Active Policies by Plan** — Breakdown across all 5 plan tiers with counts and premium volume
- **Premium Collected This Week** — Total across all plans (gross and net of GigShield fee)
- **Claims Today** — Auto-approved / In review / Auto-rejected with hourly breakdown
- **Loss Ratio by Zone** — Real-time portfolio loss ratio, segmented by delivery zone
- **Fraud Review Queue** — Claims in the 30–70 score band with GPS trace, timing evidence
- **ML Model Health** — Confidence scores, feature drift indicators, retraining alerts
- **Predicted Payout Exposure** — Expected payouts for next 48 hours based on disruption forecast

---

## Coverage Scope & Exclusions

### What GigShield Covers

GigShield covers **income lost by food delivery workers during verified external disruptions** that prevent delivery activity. Coverage is parametric — payouts are triggered by objective data thresholds, not manual claim assessment. Payouts are calculated on a per-hour basis up to the plan's weekly maximum.

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
- [ ] Minimal prototype: Worker onboarding screen + plan selection UI (React Native)
- [ ] Strategy video (2 minutes)

### Phase 2 — Automation & Protection (Weeks 3–4 | March 21–April 4)
*Theme: Protect Your Worker*

- [ ] Worker registration and KYC flow (simulated Aadhaar verification)
- [ ] Insurance policy management (create, view, renew, upgrade weekly plan)
- [ ] Zone Risk Classifier model — trained and deployed for plan recommendation at onboarding
- [ ] OpenWeatherMap + IMD + CPCB AQI API integration and disruption detection engine (15-min polling)
- [ ] Hourly payout calculation engine (duration × hourly rate, capped at plan maximum)
- [ ] Claims management system (auto-trigger pipeline: verify GPS → fraud check → approve → payout)
- [ ] Razorpay sandbox payout integration
- [ ] Firebase push notification setup
- [ ] 2-minute demo video

### Phase 3 — Scale & Optimise (Weeks 5–6 | April 5–17)
*Theme: Perfect for Your Worker*

- [ ] Advanced fraud detection — Isolation Forest model trained and deployed (GPS spoofing, fake weather claim detection)
- [ ] Predictive disruption alert engine — XGBoost model, 48-hour zone-level forecast
- [ ] Intelligent admin dashboard (zone heatmap, loss ratio by zone, fraud queue, predictive payout exposure map)
- [ ] Worker dashboard — all 5 plan cards, earnings protected counter, alert panel, upgrade flow
- [ ] NDMA alert feed integration for Trigger #5 (automated curfew/hartal detection)
- [ ] Full system integration testing across all 5 disruption triggers
- [ ] 5-minute demo video (simulated rainstorm → auto-claim → 4-hour payout walkthrough)
- [ ] Final pitch deck (PDF) — persona, AI architecture, fraud model, business viability of weekly pricing

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
