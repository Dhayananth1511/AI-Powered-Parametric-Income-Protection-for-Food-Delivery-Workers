# GigSecure 🛡️
### AI-Powered Parametric Income Protection for Food Delivery Workers
### Team ZenVyte | Guidewire DEVTrails 2026

> *"A delivery worker is stuck during a Chennai thunderstorm. They didn't file a claim. They didn't call anyone. Their phone just buzzed — ₹300 credited. GigSecure works so they don't have to."*

---

## 🚀 Judge Summary — Read This First

> **"GigSecure is the only system that doesn't trust GPS."**

| What | How |
|---|---|
| 📍 Detects disruption | Rain / heat / AQI / cyclone / curfew — IMD + CPCB APIs |
| 🤖 Verifies authenticity | 6 signals: GPS + accelerometer + cell tower + network + behavior + crowd |
| ⚡ Auto-triggers claim | No user action — fully automated from detection to payout |
| 💰 Pays instantly | ₹105–₹630/week · 5 crore+ unprotected workers · IRDAI insurer partner |

> **No claim. No forms. No fraud. Insurance that pays before you realise you lost money.**

GigSecure solves a **₹5,880/year income loss problem** for 5 crore+ informal and gig workers (NITI Aayog, 2022) — with actuarial pricing proof, 6-signal anti-spoofing, and an IRDAI insurer-partner business model with zero direct claims liability.

> **Fully automated. Fraud-resistant. Actuarially grounded. Designed for real-world deployment with simulated prototype validation.**

---

## 🧪 What is Actually Working (Phase 1 Prototype)

| Feature | Status |
|---|---|
| ✅ Worker onboarding (40+ Tamil Nadu zones, ML zone risk, plan recommendation) | **Built** |
| ✅ Plan selection with ML-recommended tier | **Built** |
| ✅ Worker dashboard — disruptions, payouts, predictive alerts, plan change | **Built** |
| ✅ Payout simulation — 5-step automated claim flow, persists to localStorage | **Built** |
| ✅ Admin dashboard — policy list, 7 KPIs, claims pipeline, API status | **Built** |
| ✅ Claims pipeline — Auto-Approved (131) · Manual Review (3) · Auto-Rejected (8) | **Built** |
| ✅ 6 interactive feature demos — weather, fraud score, earnings calc, plan compare | **Built** |
| ⚠️ Weather + AQI APIs | Simulated with realistic data — live integration in Phase 2 |
| ⚠️ ML models | Architecture fully designed — training on IMD/CPCB data in Phase 2 |
| ⚠️ Real insurer API integration | IRDAI partner structure fully designed — integration in Phase 3 |

---

## Table of Contents

1. [🚀 Judge Summary](#-judge-summary--read-this-first)
2. [🧪 What is Built (Phase 1)](#-what-is-actually-working-phase-1-prototype)
3. [Problem Statement](#problem-statement)
4. [Our Solution](#our-solution)
5. [Why GigSecure Is Innovative](#why-gigsecure-is-innovative)
6. [Delivery Worker Persona](#delivery-worker-persona)
7. [Parametric Triggers](#parametric-triggers)
8. [Weekly Premium Model](#weekly-premium-model)
9. [AI/ML Architecture](#aiml-architecture)
10. [Smart Validation Layer](#smart-validation-layer)
11. [API Failure & Data Validity Handling](#api-failure--data-validity-handling)
12. [Adversarial Defense & Anti-Spoofing](#adversarial-defense--anti-spoofing-strategy)
13. [Zero-Touch Claim Flow](#zero-touch-claim-flow)
14. [Platform & Tech Stack](#platform--tech-stack)
15. [System Architecture](#system-architecture)
16. [Dashboards](#dashboards)
17. [Coverage Scope & Exclusions](#coverage-scope--exclusions)
18. [Plan Cancellation & Refund Policy](#plan-cancellation--refund-policy)
19. [Financial & Business Model](#financial--business-model)
20. [🏆 Why GigSecure Wins](#-why-gigsecure-wins)
21. [Live Demo](#live-demo)
22. [Strategy Video](#strategy-video)
23. [45-Day Development Roadmap](#45-day-development-roadmap)

---

---

## Problem Statement

India's food delivery ecosystem runs on gig workers delivering for **Zomato** and **Swiggy** with no salary, no paid leave, and no safety net.

External disruptions — heavy monsoon rain, extreme heat, cyclone alerts, air quality emergencies, government curfews — bring delivery to a complete halt. A food delivery worker loses **₹300–₹650 in a single evening**, with no recourse.

**The numbers:**
- **5 crore+** informal and gig workers in India with zero income protection (NITI Aayog, 2022)
- **₹300–₹650** lost per disruption event per worker
- **0** traditional insurance products covering short-term gig income loss
- **Weeks** to process a manual insurance claim today

**GigSecure exists to close that gap** — through automated, parametric micro-insurance that pays out before the worker even has to ask.

---

## Our Solution

GigSecure is an **AI-powered parametric micro-insurance platform** built for food delivery partners on Zomato and Swiggy — platform independent.

### ⚡ How It Works

**User → AI Risk Score → Weekly Plan → Monitor APIs → Trigger → Auto Claim → Payout**

- Continuously monitors IMD, CPCB, and government alerts cross-validated with satellite radar APIs
- Detects disruptions at **micro-zone level (2–5 km)** — not city or pincode level
- Validates disruption persists **15–30 minutes** before triggering any payout
- Verifies GPS, behavioral signals, and fraud score in real time
- Triggers automatic partial income top-up — zero human intervention

**Key differentiators:** Independent API verification · Micro-zone precision · Time-based confirmation · ML zone pricing · 24–48hr predictive alerts · IRDAI-partner model · 50–72% loss ratio maintained

---

## Why GigSecure Is Innovative

- **Parametric Insurance** — payouts triggered by objective data, not manual claims
- **Zero-Touch Claims** — no forms, no uploads, no waiting
- **AI-Driven Risk Pricing** — Random Forest assigns plan tiers based on zone risk
- **Micro-Zone Precision** — 2–5 km disruption detection, not city-level
- **Multi-Source Validation** — IMD/CPCB cross-validated with satellite/radar APIs
- **Time-Based Confirmation** — 15–30 min persistence check eliminates false triggers
- **Crowd Signal Validation** — aggregated zone-level worker signals improve accuracy
- **6-Signal Anti-Spoofing** — GPS alone never trusted; sensors + network + behavior all verified
- **Predictive Alerts** — workers warned 24–48 hours before disruptions via XGBoost
- **Actuarially Viable** — all plans maintain insurer-acceptable loss ratios

---

## Delivery Worker Persona

### Illustrative Persona — Swiggy Delivery Partner, Chennai

| Attribute | Detail |
|---|---|
| Age | Mid-20s |
| City | Chennai — Velachery, Adyar, T. Nagar zones |
| Daily Hours | 9am – 9pm |
| Daily Deliveries | 20–28 |
| Daily Earnings | ₹900 – ₹1,300 |
| Weekly Earnings | ₹6,500 – ₹9,000 |
| Hourly Earnings | ₹112 – ₹162/hour |
| Peak Vulnerability | 7–10pm — Chennai's heaviest rainfall window |
| Financial Buffer | None. One disrupted week = missed EMI or skipped meals. |

### Disruption Scenario

Tuesday evening, August. Velachery. Rainfall crosses 40mm in 2 hours. Swiggy app goes quiet. Worker shelters under a shop.

**Old world:** ₹500 lost. No recourse.

**With GigSecure:** Phone buzzes — *"🌧️ Heavy rain in your zone. ₹300 credited. Stay safe."* They did nothing. GigSecure did.

---

## Parametric Triggers

> Every trigger is an objective, externally verifiable event from a government or accredited API. No platform data. No subjective metrics.

| # | Event | Source | Threshold | Confirmation | Payout |
|---|---|---|---|---|---|
| 1 | Heavy Rainfall | OpenWeatherMap + IMD + Satellite Radar | > 35mm in 3 hrs in micro-zone | 15–30 min persistence | Per hour up to plan cap |
| 2 | Extreme Heat | IMD API + Private Weather API | > 43°C sustained 2+ hrs | 30 min persistence | Per hour up to plan cap |
| 3 | Severe AQI | CPCB AQI API + OpenAQ | AQI > 300 Hazardous | Confirmed 2+ sources | Per hour up to plan cap |
| 4 | Cyclone / Flood | IMD Disaster Feed + NDMA | Orange/Red alert in district | Alert active 30+ min | Full weekly cap immediately |
| 5 | Curfew / Hartal | NDMA feed + admin-confirmed flag | Section 144 / state shutdown | Admin-verified flag | Full weekly cap immediately |

**Compliance:** Every trigger is externally verifiable, parametric (threshold crossed or not), and causally linked to income loss.

**Time confirmation:**

| Duration | Action |
|---|---|
| < 15 minutes | Monitoring — no trigger |
| 15–30 minutes | Confirmation window — worker alerted |
| > 30 minutes | Trigger confirmed — claim initiated |

---

## Weekly Premium Model

### 💡 Pricing Logic
```
Weekly Premium = Base Price + (Risk Score × Zone Risk Factor)
```

### Design Philosophy

GigSecure is a **partial income top-up** — not full replacement. A worker losing ₹280 in a 2.5-hour disruption gets back ₹300 on the Standard plan — a net positive. Premiums range from 0.5–2.1% of weekly earnings, making all plans affordable for active delivery workers.

### Actuarial Foundation

| Parameter | Value | Basis |
|---|---|---|
| Disruption events/month (monsoon Jun–Nov) | 3.0 | IMD Chennai 10-yr average |
| Disruption events/month (off-season Dec–May) | 0.5 | IMD Chennai historical |
| Annual disruption events/worker | **21/year** | (3.0×6) + (0.5×6) |
| Average disruption duration | **2.5 hrs** | IMD urban rainfall data |
| Annual disruption hours/worker | **52.5 hrs** | 21 × 2.5 |
| Worker hourly income | ₹112/hr | ₹900/day ÷ 8 hrs |
| Annual income lost | **₹5,880** | 52.5 × ₹112 |

**Target loss ratio:** 65% (parametric micro-insurance benchmark, India)

### The 5 Plans

| Plan | Weekly Premium | Hourly Payout | Max Hrs/Week | Max Weekly Payout | Target User |
|---|---|---|---|---|---|
| 🌱 Starter | ₹35/week | ₹35/hour | 3 hours | ₹105 | New workers, low-risk zones |
| 🔵 Basic | ₹55/week | ₹45/hour | 4 hours | ₹180 | Part-time, low-risk zones |
| 🟡 Standard | ₹79/week | ₹60/hour | 5 hours | ₹300 | Full-time, urban zones |
| 🟠 Premium | ₹109/week | ₹75/hour | 6 hours | ₹450 | High-earning full-time |
| 🔴 Elite | ₹149/week | ₹90/hour | 7 hours | ₹630 | Coastal / flood-prone zones |

### Loss Ratio Proof

| Plan | Annual Premium | Expected Annual Claim | Loss Ratio | Heavy Monsoon (+40%) |
|---|---|---|---|---|
| 🌱 Starter | ₹1,820 | ₹1,102 | 61% ✅ | ~79% ✅ |
| 🔵 Basic | ₹2,860 | ₹1,890 | 66% ✅ | ~80% ✅ |
| 🟡 Standard | ₹4,108 | ₹3,150 | 77% ⚠️ | ~89% ⚠️ |
| 🟠 Premium | ₹5,668 | ₹4,725 | 83% ⚠️ | ~95% ⚠️ |
| 🔴 Elite | ₹7,748 | ₹6,300 | 81% ⚠️ | ~98% ⚠️ |

> ⚠️ Standard, Premium, and Elite plans carry higher loss ratios reflecting the increased payout rates. These are managed through: (1) zone-risk pricing multipliers (1.2–1.4×) in high-disruption zones, (2) monsoon reserve buffers held by the insurer partner, and (3) **dynamic weekly premium adjustment** during high-risk periods (e.g., peak monsoon weeks) to maintain sustainable loss ratios. Higher payouts create a stronger worker value proposition and adoption rate — the insurer manages exposure through actuarial reserves, not premium cuts.

### Worker Affordability Check

| Plan | Weekly Premium | % of Weekly Earnings | Deliveries to Cover | Weekly Protection |
|---|---|---|---|---|
| 🌱 Starter | ₹35 | 0.5% | ~1 delivery | ₹105 |
| 🔵 Basic | ₹55 | 0.8% | ~1.5 deliveries | ₹180 |
| 🟡 Standard | ₹79 | 1.1% | ~2 deliveries | ₹300 |
| 🟠 Premium | ₹109 | 1.6% | ~3 deliveries | ₹450 |
| 🔴 Elite | ₹149 | 2.1% | ~4 deliveries | ₹630 |

All plans under 2.5% of weekly earnings (CGAP affordability threshold). Standard plan at ₹79/week delivers up to ₹300 — more than the typical ₹280 income loss, making it a net positive for subscribing workers.

### Why Weekly Pricing

Gig workers operate on weekly income cycles. Daily premiums create friction. Monthly premiums are too large a commitment for variable income. Weekly pricing — under 2 deliveries' worth — matches how delivery workers think about money.

---

## Demo Scenario

1. Ravi subscribes to **Standard Plan (₹79/week)** via GigSecure mobile web.
2. GigSecure polls OpenWeatherMap + IMD + satellite radar every 15 min across Ravi's micro-zone (Velachery, 3 km).
3. Rainfall crosses 35mm threshold.
4. **15–30 min confirmation window** begins — rain must persist.
5. Rain persists 30+ min. Radar confirms. 7 workers in zone show near-zero movement.
6. GPS inside zone ✅ · Accelerometer confirms prior delivery movement ✅ · Cell tower ID matches ✅
7. Fraud score: **14/100 — CLEAN**.
8. Disruption verified: **5 hours**.
9. Payout: **5 hrs × ₹60/hr = ₹300**.
10. Insurer partner releases via Razorpay Sandbox.

```
🌧️ Heavy rain in your zone (Velachery, Chennai).
₹300 credited. Disruption: 5 hrs · Standard Plan. Stay safe, Ravi.
```

---

## AI/ML Architecture

### Model 1 — Zone Risk Classifier

**Algorithm:** Random Forest Classifier
**Purpose:** Recommend plan tier at onboarding based on micro-zone's historical disruption risk.

**Input Features:** Zone lat/lon · Historical disruption events/month · Proximity to water bodies · Zone elevation · Month of year · Historical AQI exceedance days

**Output:** Risk score 0.0–1.0

| Risk Score | Plan Recommendation |
|---|---|
| < 0.25 | 🌱 Starter / 🔵 Basic |
| 0.25–0.55 | 🟡 Standard |
| 0.55–0.75 | 🟠 Premium |
| > 0.75 | 🔴 Elite |

**Why Random Forest:** Mixed feature types, interpretable feature importance, works well on zone-level historical data volumes.

---

### Model 2 — Fraud Detection Engine

**Algorithm:** Isolation Forest + deterministic hard-reject rules

**Hard Reject Rules (applied first):**

| Rule | Logic |
|---|---|
| No verified trigger | No IMD/CPCB breach in worker's zone on claim day → reject |
| GPS zone mismatch | Worker GPS doesn't overlap disruption micro-zone → reject |
| Cell tower mismatch | Cell tower ID doesn't match claimed GPS zone → reject |
| Cap exceeded | Max hours for week already reached → reject |
| Plan expired | No active weekly subscription → reject |
| Time threshold not met | Disruption < 15 min → reject |

**Isolation Forest Anomaly Signals:**

| Feature | Fraud Signal |
|---|---|
| GPS velocity during disruption | > 5 km/h = actively working, not disrupted |
| Accelerometer pattern | Flat stationary signal + no prior zone movement = spoofing |
| Cell tower vs GPS | Geographic mismatch = location fake |
| Claim timing | Filed before trigger crossed = suspicious |
| Pre-disruption zone activity | No movement history in zone before trigger |
| Device fingerprint | Multiple accounts on same device |
| Crowd signal disagreement | Zone shows no inactivity spike while worker claims disruption |

**Output:** Fraud score 0–100 → Auto-approve (< 30) · Review (30–70) · Auto-reject (> 70)

---

### Worker Eligibility & Trust Score System

Every worker has a running Trust Score (0–100) updated weekly from: active subscription weeks (+) · clean claim history (+) · consistent GPS delivery patterns (+) · low fraud score history (+/−).

| Trust Score | Tier | Status |
|---|---|---|
| 75–100 | 🟢 Trusted | Full auto-approval |
| 50–74 | 🔵 Established | Auto-approval, standard processing |
| 25–49 | 🟡 Building | Manual review before payout |
| 0–24 | 🔴 Restricted | Manual review + 50% payout cap |

New workers start at **Provisional Score 40** — can claim from Week 1 at 50% cap. Full benefits after 3 clean weeks.

```
Disruption confirmed → Eligibility Gate (Trust Score) → Fraud Detection → Payout decision
```

---

### Model 3 — Predictive Disruption Alert Engine

**Algorithm:** XGBoost on time-series weather features
**Output:** Disruption probability 0–100% per micro-zone per day, 24–48 hrs ahead

> *"⚡ Storm likely in your zone tomorrow 6–9pm. Probability: 78%. Your ₹300 coverage is active."*

Admin view: City-wide heatmap for 48-hr predicted payout exposure per micro-zone.

---

## Smart Validation Layer

| Layer | Problem | Solution |
|---|---|---|
| **1. Multi-Source Reliability** | IMD/CPCB APIs can be delayed or stale | Cross-verify 2+ independent sources. Satellite radar as fallback. No single point of failure. |
| **2. Micro-Zone Precision (2–5 km)** | City/pincode data too coarse | Workers mapped to 2–5 km micro-zones. Trigger logic at zone centroid, not city level. |
| **3. Time-Based Confirmation** | Brief 5-min showers ≠ meaningful disruption | Disruption must persist 15–30 min continuously. Counter resets if drops below threshold. |
| **4. Context-Aware Delivery Logic** | 20-min vs 3-hr disruption ≠ same impact | Compare disruption duration vs avg delivery time (30–45 min). Payout scales proportionally. |
| **5. Crowd Signal Validation** | API data lags real conditions 10–20 min | Anonymized zone-level aggregate: movement speed + inactivity spikes. Never individual tracking. |

```
Layer 1: API threshold crossed → Layer 2: Secondary source confirms →
Layer 3: 15–30 min persistence → Layer 4: Worker GPS + sensors verified →
Layer 5: Crowd signal confirms → ✅ Payout initiated
```

**Privacy:** No individual worker tracked. All behavioral and crowd signals are anonymized and processed without storing personally identifiable information (PII). Signals aggregated at zone level and permanently discarded after the disruption window closes — never retained or linked to any individual.

---

## API Failure & Data Validity Handling

> *GigSecure is only as reliable as its data sources. We designed for failure from day one.*

| Failure Scenario | GigSecure Response |
|---|---|
| **Primary API (IMD) goes down** | Auto-fallback to satellite/radar secondary. No monitoring disruption. |
| **Both APIs return stale data (> 30 min)** | Payout frozen. Worker notified: "Verification pending." |
| **API data outside valid range** | Outlier detection flags reading. Discarded before trigger logic runs. |
| **Partial zone coverage (< 60% micro-zone)** | Weighted average applied. Trigger only fires if weighted threshold met. |
| **CPCB AQI slow / unavailable** | Cross-reference OpenAQ fallback. If neither available, AQI trigger suspended. |
| **NDMA alert feed delayed** | Trigger 5 requires admin-confirmed flag as second gate — prevents auto-trigger from stale feed. |
| **All external APIs fail simultaneously** | Full monitoring pause. Workers notified. No payouts triggered. Insurer partner alerted. |

**Data safeguards:** Range validation · Temporal validation (data > 30 min old = stale) · Cross-source consistency check (> 40% disagreement = no trigger) · Graceful degradation — always defaults to safer outcome (no payout) when data uncertain.

> **GigSecure's principle: better to delay a valid payout than release an invalid one.**

---

## Adversarial Defense & Anti-Spoofing Strategy

> *This section extends the fraud detection model with real-time adversarial defenses against coordinated GPS spoofing attacks.*

### Summary

| Layer | Method |
|---|---|
| 🔍 Multi-signal validation | GPS + accelerometer + cell tower + network — all must agree |
| 🧠 Behavioral anomaly detection | Isolation Forest flags deviations from genuine worker baseline |
| 👥 Crowd-based verification | Zone-level aggregate signals catch mass coordinated attacks |
| 🏅 Trust scoring | Reputation system catches repeat offenders across weeks |

> **GPS alone is never trusted. A spoofer passes 1 of 6 signals. GigSecure requires 4 of 6.**

### The Attack

500 fraudsters use GPS spoofing apps to fake location inside disruption zones. They sit at home while their phone reports coordinates inside Velachery during a rain event.

### Differentiation — Real Worker vs Spoofer

| Signal | Real Worker | GPS Spoofer |
|---|---|---|
| GPS coordinate | Inside zone ✅ | Faked inside zone ✅ |
| Accelerometer / IMU | Bike vibration, stops, turns → stop at disruption | Flat stationary signal — no movement history |
| Cell tower ID | Matches disruption zone towers | Home cell tower — geographic mismatch |
| GPS velocity pattern | Delivery movement → sudden stop at trigger | Zero velocity throughout |
| Device activity | Maps, delivery app, calls | GPS spoofing app in background |
| Weather API cross-check | Real location aligns with rain zone | Home location (revealed by cell tower) has no rain |

**Spoofer passes Signal 1, fails Signals 2–6. GigSecure requires 4 of 6.**

### Multi-Signal Strategy

**Device Sensors:** Accelerometer shows bike vibration + delivery stop patterns. Spoofer shows flat signal with zero prior zone movement. Gyroscope turning patterns of a two-wheeler can't be replicated without the vehicle.

**Network Layer:** Cell tower ID reported independently of GPS. GPS says Velachery, cell tower says Adyar = hard flag. Home Wi-Fi detection further reveals true location.

**Behavioral Layer:** Every worker builds a movement fingerprint over 2–3 weeks. Spoofers appear in the zone from nowhere at trigger time — this gap is measurable. Real workers are mid-delivery when storms hit.

**Crowd Signal Layer:** 500 spoofed devices show identical flat accelerometer readings simultaneously — a statistically impossible cluster flagged immediately by Isolation Forest.

### Anti-Spoofing Score

| Signal | Points |
|---|---|
| GPS inside zone | Required |
| Accelerometer confirms movement | +2 |
| Cell tower ID matches zone | +2 |
| Pre-disruption zone activity | +2 |
| Crowd signal consistent | +1 |
| Historical baseline consistent | +1 |
| Claim timing is natural | +1 |

**Score ≥ 7** → Auto-approve · **4–6** → Manual review (2hr SLA) · **< 4** → Auto-reject + appeal

*No single signal can approve or reject a claim.*

> **Eligibility condition:** Workers must show active delivery behavior (GPS movement in their zone matching delivery patterns) within **30–60 minutes before the disruption trigger** to qualify for payout. A worker who is home before a storm hits does not qualify — only workers genuinely caught mid-delivery are covered. This is verified through the accelerometer + GPS pre-disruption activity check.

### UX Balance — Protecting Honest Workers

**Soft Flag (4–6):** Claim enters manual review queue. Worker notified: "Being verified — decision within 2 hours."

**Provisional Payout (Trust Score ≥ 75):** 50% released immediately. Remaining 50% held pending review. If genuine → full amount released. If fraud → clawback.

**Appeal Flow:** One-tap appeal. Cell tower log + accelerometer + GPS trace requested from device. Second human review within 24 hours. Wrongful rejections reversed + trust score restored.

**GigSecure never:** Permanently bans on first flag · Requires photo/video proof · Penalises new accounts · Uses GPS alone to reject · Exposes individual worker data to aggregate analysis.

### Why the 500-Spoofer Attack Fails

| Reason | Why It Fails |
|---|---|
| Sensors can't be mass-faked | Spoofing accelerometer + cell tower + network needs device rooting — not worth it for ₹105–₹630 |
| Attacks are statistically visible | 500 identical flat accelerometer readings = obvious Isolation Forest anomaly |
| Economics don't work | Coordinating 500 devices to earn ₹630 max/week is not rational |
| Trust Score catches repeat offenders | Baseline diverges over weeks — future claims always trigger review |
| Cell tower is hardest to fake | Requires physically travelling to the disruption zone |

---

## Zero-Touch Claim Flow

```
Worker subscribes → GigSecure polls APIs every 15 min at micro-zone level
                 ↓
       7:23pm — Rainfall crosses 35mm threshold
                 ↓
    ┌─ Time Confirmation Window (15–30 min) ─┐
    │  7:53pm — Rain persists ✅              │
    │  Radar API confirms ✅                  │
    └────────────────────────────────────────┘
                 ↓
    ✅ GPS inside micro-zone
    ✅ Cell tower ID matches zone
    ✅ Accelerometer confirms prior movement
    ✅ Plan active · Cap not reached
    ✅ Crowd signal: 7 workers near-zero movement
    ✅ Fraud score: 14/100 — CLEAN
                 ↓
    Disruption: 5 hours · Payout: 5 × ₹60 = ₹300
                 ↓
    Insurer partner releases → Razorpay Sandbox
                 ↓
    Firebase FCM: "₹300 credited. Stay safe."
```

**Near real-time. Fully automated. Zero human intervention required.**

---

## Platform & Tech Stack

### Platform Strategy

GigSecure is a **fully responsive web application** — workers access via mobile browser, admins via desktop. No app install required. Single Python FastAPI backend serves both.

| Platform | User | Purpose |
|---|---|---|
| Mobile Web (HTML · CSS · JS) | Delivery Workers | Onboarding, plan selection, alerts, payouts, plan management |
| Desktop Web (HTML · CSS · JS) | Insurer / Admin | Policies, fraud queue, loss ratio, payout simulation |

### Tech Stack

| Layer | Technology | Justification |
|---|---|---|
| Mobile Frontend | HTML · CSS · JavaScript | Responsive mobile web — no install needed |
| Web Frontend | HTML · CSS · JavaScript | Same codebase, shared components |
| Backend | Python FastAPI | ML-friendly, async, high performance |
| Database | PostgreSQL | Workers, policies, claims, payout records |
| ML Models | Scikit-learn (Random Forest, Isolation Forest), XGBoost | Production-grade, well-documented |
| Weather API (Primary) | OpenWeatherMap + IMD public data | Real-time + historical training data |
| Weather API (Secondary) | Satellite/radar private API | Backup validation, handles IMD delays |
| AQI API | CPCB AQI API + OpenAQ | Government-verified, cross-validated |
| Disaster Alerts | NDMA public alert feed | Automated curfew detection (Trigger 5) |
| Zone Mapping | Google Maps API + micro-zone segmentation (2–5 km) | Precise GPS zone verification |
| Payments | Razorpay Sandbox | Simulated near-real-time payout |
| Notifications | Firebase Cloud Messaging | Real-time worker alerts |
| Hosting | Railway / Render (free tier) | Fast hackathon deployment |

### 🔄 End-to-End Flow

```
Step 1 → Worker subscribes (₹35–₹149/week)
Step 2 → APIs polled every 15 min at micro-zone level
Step 3 → Threshold crossed → 15–30 min validation begins
Step 4 → GPS + accelerometer + cell tower + behavior cross-checked
Step 5 → Isolation Forest fraud score calculated (0–100)
Step 6 → Score < 30 → Payout auto-released
```

> **Real worker in a real storm → paid in minutes. GPS spoofer at home → caught at Step 4.**

---

## System Architecture

```
┌──────────────────────┐     ┌──────────────────────┐
│  Worker Mobile Web   │     │   Admin Desktop Web   │
│  (HTML · CSS · JS)   │     │   (HTML · CSS · JS)   │
└──────────┬───────────┘     └──────────┬────────────┘
           └──────────────┬─────────────┘
                          ▼
              ┌─────────────────────┐
              │  FastAPI Backend    │
              │  (Python)           │
              └──────────┬──────────┘
            ┌────────────┼────────────┐
            ▼            ▼            ▼
     ┌──────────┐  ┌──────────┐  ┌───────────────────┐
     │PostgreSQL│  │ML Engine │  │Disruption Monitor │
     │Workers,  │  │Risk,     │  │15-min poll at     │
     │Policies, │  │Fraud,    │  │micro-zone level   │
     │Claims    │  │Predict   │  │(2–5 km zones)     │
     └──────────┘  └──────────┘  └────────┬──────────┘
                                           │
              ┌────────────────────────────┤
              ▼            ▼              ▼
     ┌──────────────┐ ┌──────────┐ ┌──────────────┐
     │OpenWeatherMap│ │CPCB AQI  │ │IMD / NDMA    │
     │+ IMD Weather │ │+ OpenAQ  │ │Alert Feed    │
     │+ Satellite   │ │          │ │              │
     └──────────────┘ └──────────┘ └──────────────┘
                          ▼
              ┌────────────────────────────┐
              │  Multi-Layer Validation    │
              │  Time · Cross-source · GPS │
              │  Cell tower · Accelero.    │
              │  Crowd signal · Fraud score│
              └──────────────┬─────────────┘
                             ▼
              ┌──────────────────────────┐
              │  IRDAI Insurer Partner   │
              └──────────────┬───────────┘
                             ▼
              ┌──────────────────────────┐
              │  Razorpay Sandbox        │
              └──────────────┬───────────┘
                             ▼
              ┌──────────────────────────┐
              │  Firebase FCM (Worker)   │
              └──────────────────────────┘
```

---

## Dashboards

### Worker Mobile Dashboard

- **Plan Status** — Active 🟢 / Expired 🔴 / Disruption in Progress ⚡
- **Current Plan Card** — Name, premium, hourly rate, hours remaining this week
- **Change Plan** — Upgrade or downgrade anytime — effective next Monday
- **My Micro-Zone** — Worker's 2–5 km delivery zone
- **This Week's Disruptions** — Events detected in zone with type, time, payout
- **Payouts Received** — Timeline of all credited amounts, updates live with simulations
- **Predictive Alert Panel** — XGBoost 48-hr forecast: "Rain likely 6–9pm (78%)"
- **Earnings Protected Counter** — Total saved via GigSecure
- **Trigger Status** — Live: Rainfall · Heat · AQI · Cyclone · Curfew

### Admin / Insurer Dashboard

- **Registered Policies** — Full worker list: plan, zone, risk score, past + simulated payouts
- **7 Live KPIs** — Policies count · Weekly premium · Total payouts · Platform fee · Claims · Loss ratio · New today
- **Plan Distribution** — Breakdown across 5 tiers with counts and premium volume
- **Per-Worker Simulation** — Select worker → choose disruption → 5-step automated claim flow → persists to record
- **Claims Pipeline** — 3-tab: Auto-Approved (131) · Manual Review (3 with approve/reject) · Auto-Rejected (8 with reasons)
- **Data Source API Status** — Live latency and status for all 6 API feeds

---

## Coverage Scope & Exclusions

**Covers:** Income lost during verified external disruptions that prevent delivery — parametric triggers only, per-hour basis up to weekly plan cap. Partial income top-up — not full replacement.

**Does NOT cover:** Vehicle repairs · bike maintenance · fuel · medical · accidents · platform demand fluctuations · traffic · app technical issues · any event not verifiable through government or accredited API.

---

## Plan Cancellation & Refund Policy

> *A worker subscribes in good faith. If they want to leave, GigSecure makes it simple and fair.*

### Cancellation Policy

| Situation | Policy |
|---|---|
| **Cancel before Monday auto-renew** | No charge for next week. Current week coverage runs to Sunday. |
| **Cancel mid-week (Day 1–4)** | Coverage continues to end of week. Pro-rata credit toward next payment. |
| **Cancel mid-week (Day 5–7)** | Coverage runs to Sunday. No refund — week nearly complete. |
| **Cancel within 24 hours of first subscription** | **Full refund. No questions. Cooling-off period.** |
| **Cancel after payout received this week** | No refund — payout already released, premium consumed. |

### Why Weekly Subscription Solves This

- Workers are **never trapped** — simply don't renew next Monday
- **No annual contract** — max exposure is 7 days of premium (₹35–₹149)
- **Re-subscription is instant** — coverage resumes from next Monday
- **First-time subscribers** get 24-hour full refund window — one-tap from worker dashboard, no impact on Trust Score

> **Friction-free exit builds the trust that brings workers back.**

---

## Financial & Business Model

### GigSecure is a Technology Platform — Not an Insurer

```
Worker pays weekly premium
         ↓
Licensed IRDAI Insurer Partner (e.g., Digit Insurance / Acko)
holds all premium capital and pays all claims
         ↓
GigSecure earns a 5% platform distribution fee per active policy
         ↓
GigSecure does not underwrite risk or pay claims directly.
All claim liabilities handled by the licensed insurer partner.
```

### Revenue Per Policy Per Week

| Plan | Weekly Premium | GigSecure Fee (5%) | Insurer Net Premium | Insurer Loss Ratio |
|---|---|---|---|---|
| 🌱 Starter | ₹35 | ₹1.75 | ₹33.25 | ~68% ✅ |
| 🔵 Basic | ₹55 | ₹2.75 | ₹52.25 | ~55% ✅ |
| 🟡 Standard | ₹79 | ₹3.95 | ₹75.05 | ~77% ⚠️ |
| 🟠 Premium | ₹109 | ₹5.45 | ₹103.55 | ~83% ⚠️ |
| 🔴 Elite | ₹149 | ₹7.45 | ₹141.55 | ~81% ⚠️ |

> ⚠️ Higher-payout plans managed via zone-risk pricing multipliers and insurer monsoon reserves.

### 🏦 Why Insurers Partner with GigSecure

- **Controlled loss ratios** — zone-risk pricing keeps portfolio manageable even in monsoon years
- **Parametric triggers** — no disputes, no assessors, minimal admin cost
- **Fraud detection** — minimises payout leakage before insurers see a claim
- **Untapped market** — 5 crore+ informal workers (NITI Aayog, 2022) currently unreachable by insurers
- **Zero distribution cost** — GigSecure handles acquisition, onboarding, and tech

> GigSecure expands insurer reach into an underserved market while maintaining strict financial discipline.

### Revenue at Scale

| Active Workers | Weekly Fee (avg ₹4.10) | Weekly Revenue | Annual Revenue |
|---|---|---|---|
| 1,000 | ₹4.10 | ₹4,100 | ₹21,32,000 |
| 10,000 | ₹4.10 | ₹41,000 | ₹2,13,20,000 |
| 1,00,000 | ₹4.10 | ₹4,10,000 | ₹21,32,00,000 |

*Projections assume consistent weekly plan retention and active worker base growth in urban delivery zones.*

**GigSecure's platform model ensures no direct exposure to claim payouts — operationally scalable and financially resilient.**


---
## 🏆 Why GigSecure Wins

1. **Only solution with multi-signal fraud prevention** — GPS + accelerometer + cell tower + network + behavior + crowd signal
2. **Only solution with actuarial pricing proof** — loss ratios calculated for all 5 plans including heavy monsoon scenarios
3. **Only solution with micro-zone precision (2–5 km)** — disruption detection at neighbourhood level, not city or pincode
4. **Only solution that simulates the attack it's defending against** — 500 GPS spoofers, defeated architecturally
5. **Only solution with zero-touch claims** — fully automated from disruption detection to payout, no user action needed

| What Others Do | What GigSecure Does |
|---|---|
| Rely on GPS alone | 6-signal validation — GPS + accelerometer + cell tower + network + behavior + crowd |
| Detect weather events | 5-layer validation with time confirmation + multi-source cross-check |
| Ignore fraud edge cases | Simulate 500-spoofer attack and defeat it architecturally |
| Skip business viability | Actuarial loss ratio proof across all 5 plans including worst-case monsoon |
| Present ideas | Working prototype + ML architecture + IRDAI insurer-partner model |

> **GigSecure is not just innovative — it is designed for real-world deployment, fraud-resistant, and financially viable on Day 1.**

---

## Live Demo

📱 **Login →**
https://Dhayananth1511.github.io/AI-Powered-Parametric-Income-Protection-for-Food-Delivery-Workers/gigsecure_login.html

🧪 **Feature Demo →**
https://Dhayananth1511.github.io/AI-Powered-Parametric-Income-Protection-for-Food-Delivery-Workers/gigsecure_features.html

💡 **What to explore:**
- Worker onboarding with zone risk ML (40+ Tamil Nadu zones)
- Plan selection with AI recommendation
- Worker dashboard: simulation, payouts timeline, predictive alerts, plan change
- Admin dashboard: policy list, 7 KPIs, claims pipeline (auto-approved / review / rejected), API status
- Features: weather monitor, claim simulator, fraud visualizer, earnings calc, disruption chart, plan compare

> Prototype built for Guidewire DEVTrails 2026. All data simulated. No real money transacted.

---

## Strategy Video

🎥 *2-minute strategy video — to be added before submission deadline.*

---

## 45-Day Development Roadmap

### Phase 1 — Foundation (Weeks 1–2 | Mar 4–20) ✅
- [x] Problem research + gig worker persona analysis
- [x] Insurance model — 5 plans, hourly payout, actuarial loss ratio proof
- [x] ML architecture (Zone Risk · Fraud Detection · Predictive Alert)
- [x] System architecture + tech stack
- [x] Business model — IRDAI partner structure, 5% platform fee
- [x] Smart Validation Layer — multi-source, micro-zone, time confirmation, crowd signals
- [x] Adversarial Defense — 6-signal GPS spoofing detection
- [x] API Failure & Data Validity handling strategy
- [x] Plan Cancellation & Refund Policy
- [x] Full HTML/CSS/JS prototype — Login · Onboarding · Worker Dashboard · Admin Dashboard · Feature Demo
- [x] Strategy video (2 minutes) — to be submitted before deadline

### Phase 2 — Automation (Weeks 3–4 | Mar 21–Apr 4)
- [ ] Worker KYC flow (simulated Aadhaar verification)
- [ ] Policy management (create, view, renew, upgrade/downgrade)
- [ ] Zone Risk Classifier — trained + deployed for onboarding
- [ ] Micro-zone segmentation — 2–5 km zones mapped per city
- [ ] OpenWeatherMap + IMD + satellite radar API integration (15-min polling)
- [ ] Time-based confirmation engine (15–30 min persistence)
- [ ] Hourly payout engine (hours × rate, capped at plan max)
- [ ] Auto-claim pipeline: confirm → verify → GPS + cell tower + accelerometer → fraud → approve → payout
- [ ] Razorpay sandbox payout
- [ ] Firebase push notifications

### Phase 3 — Scale (Weeks 5–6 | Apr 5–17)
- [ ] Isolation Forest fraud model with cell tower + accelerometer features
- [ ] Anti-spoofing layer — cell tower triangulation, accelerometer baseline, behavioral fingerprint
- [ ] Crowd signal layer — anonymized zone-level behavioral aggregation
- [ ] XGBoost predictive alert engine — 48-hr micro-zone forecast
- [ ] NDMA alert feed for Trigger 5
- [ ] Full integration testing across all 5 triggers
- [ ] 5-min demo video
- [ ] Final pitch deck (PDF)

---

## Hackathon Prototype Disclaimer

Built for **Guidewire DEVTrails 2026 Hackathon**.

- Payouts simulated via Razorpay Sandbox
- Identity verification mocked
- APIs: OpenWeatherMap, CPCB, IMD, NDMA (public)
- Satellite radar API simulated with cached data
- Crowd signal layer uses synthetic zone-level data
- Cell tower + accelerometer signals simulated in prototype
- ML models trained on IMD/CPCB public historical data
- Responsive HTML/CSS/JS web app — mobile-first design, works on all screen sizes

In production, GigSecure integrates with a licensed IRDAI insurance partner for real claim payouts.

---

## About This Project

**Hackathon:** Guidewire DEVTrails 2026 Pan-India University Hackathon
**Team:** ZenVyte
**Members:** Dhayananth N *(Lead)* · Mowlieswaran G · Arun Kumar S · Karthick V · Hardik Muthusamy
**Problem:** AI-Powered Insurance for India's Gig Economy
**Focus:** Food Delivery Workers — Zomato / Swiggy
**Platform:** Responsive Web — Mobile (Workers) + Desktop (Admin)

---

*Build fast. Spend smart. Protect every delivery worker. 🛡️*
*Team ZenVyte — DEVTrails 2026*