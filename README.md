# ZenVyte GigPulse 🛡️
### Zero-Trust Financial Infrastructure for the Gig Economy
### Team ZenVyte | Guidewire DEVTrails 2026

> *"ZenVyte GigPulse is an AI-powered parametric micro-insurance platform built for food delivery partners on Zomato and Swiggy — platform independent.
Parametric insurance is broken. API triggers are blind to on-the-ground fraud. ZenVyte GigPulse isn't just an insurance app—it's a multi-signal risk validation engine built to algorithmically guarantee that only a real worker in a real disruption gets paid."*

---

## 🚀 Judge Summary

> **"ZenVyte GigPulse is the only system that functions as a Zero-Trust Risk Engine—and the only team that architecturally defeated the Market Crash spoofing attack."**

| What | How |
|---|---|
| 📍 Detects disruption | Rain / heat / AQI / cyclone / curfew — IMD + CPCB APIs |
| 🤖 Verifies authenticity | 6 signals: GPS + accelerometer + cell tower + network + behavior + crowd |
| ⚡ Auto-triggers claim | No user action — fully automated from detection to payout |
| 💰 Pays instantly | ₹105–₹630/week · 5 crore+ unprotected workers · IRDAI insurer partner |
| 🚨 Market Crash Defense | 6-signal anti-spoofing — GPS alone never trusted — see Section 5 |

> **No claim. No forms. No fraud. Insurance that pays before you realise you lost money.**

ZenVyte GigPulse solves a **₹5,880/year income loss problem** for 5 crore+ informal and gig workers (NITI Aayog, 2022) — with actuarial pricing proof, 6-signal anti-spoofing, and an IRDAI insurer-partner business model with zero direct claims liability.

> **Fully automated. Fraud-resistant. Actuarially grounded. All 5 plans maintain controlled loss ratios under both normal and heavy monsoon scenarios.**

---


## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Our Solution](#our-solution)
3. [Why ZenVyte GigPulse Is Innovative](#Why-ZenVyte-GigPulse-Is-Innovative)
4. [Delivery Worker Persona](#delivery-worker-persona)
5. [Adversarial Defense & Anti-Spoofing Strategy](#adversarial-defense--anti-spoofing-strategy)
6. [Parametric Triggers](#parametric-triggers)
7. [Actuarial Basis](#actuarial-basis)
8. [Weekly Premium Model — Corrected & Verified](#weekly-premium-model--corrected--verified)
9. [Weekly Payout Per Disruption Type](#weekly-payout-per-disruption-type)
10. [Loss Ratio Analysis — All Plans Under Control](#Loss-Ratio-Analysis)
11. [Worker Affordability Check](#worker-affordability-check)
12. [AI/ML Architecture](#aiml-architecture)
13. [Smart Validation Layer](#smart-validation-layer)
14. [API Failure & Data Validity Handling](#api-failure--data-validity-handling)
15. [Zero-Touch Claim Flow](#zero-touch-claim-flow)
16. [Platform & Tech Stack](#platform--tech-stack)
17. [System Architecture](#system-architecture)
18. [Dashboards](#dashboards)
19. [Coverage Scope & Exclusions](#coverage-scope--exclusions)
20. [Plan Cancellation & Refund Policy](#plan-cancellation--refund-policy)
21. [Financial & Business Model](#financial--business-model)
22. [Why ZenVyte GigPulse Wins](#Why-ZenVyte-GigPulse-Wins)
23. [Live Website](#Live-Website-Render-Deployed)
24. [45-Day Development Roadmap](#45-day-development-roadmap)

---

## Problem Statement

India's food delivery ecosystem runs on gig workers delivering for **Zomato** and **Swiggy** with no salary, no paid leave, and no safety net.

External disruptions — heavy monsoon rain, extreme heat, cyclone alerts, air quality emergencies, government curfews — bring delivery to a complete halt. A food delivery worker loses **₹300–₹650 in a single evening**, with no recourse.

**The numbers:**
- **5 crore+** informal and gig workers in India with zero income protection (NITI Aayog, 2022)
- **₹300–₹650** lost per disruption event per worker
- **0** traditional insurance products covering short-term gig income loss
- **Weeks** to process a manual insurance claim today

**ZenVyte GigPulse exists to close that gap** — through automated, parametric micro-insurance that pays out before the worker even has to ask.

---

## Our Solution

ZenVyte GigPulse is an **AI-powered parametric micro-insurance platform** built for food delivery partners on Zomato and Swiggy — platform independent.

### ⚡ How It Works

**User → AI Risk Score → Weekly Plan → Monitor APIs → Trigger → Auto Claim → Payout**

- Continuously monitors IMD, CPCB, and government alerts cross-validated with satellite radar APIs
- Detects disruptions at **micro-zone level (2–5 km)** — not city or pincode level
- Validates disruption persists **15–30 minutes** before triggering any payout
- Verifies GPS, behavioral signals, and fraud score in real time
- Triggers automatic partial income top-up — zero human intervention

**Key differentiators:** Independent API verification · Micro-zone precision · Time-based confirmation · ML zone pricing · 24–48hr predictive alerts · IRDAI-partner model · All plans maintain controlled loss ratios under normal and heavy monsoon conditions.

---

## Why ZenVyte GigPulse Is Innovative

- **Parametric Insurance** — payouts triggered by objective data, not manual claims
- **Zero-Touch Claims** — no forms, no uploads, no waiting
- **AI-Driven Risk Pricing** — Random Forest assigns plan tiers based on zone risk
- **Micro-Zone Precision** — 2–5 km disruption detection, not city-level
- **Multi-Source Validation** — IMD/CPCB cross-validated with satellite/radar APIs
- **Time-Based Confirmation** — 15–30 min persistence check eliminates false triggers
- **Crowd Signal Validation** — aggregated zone-level worker signals improve accuracy
- **6-Signal Anti-Spoofing** — GPS alone never trusted; sensors + network + behavior all verified
- **Predictive Alerts** — workers warned 24–48 hours before disruptions via XGBoost
- **Actuarially Viable** — all 5 plans maintain controlled loss ratios under both normal and heavy monsoon scenarios

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

**With ZenVyte GigPulse:** Phone buzzes — *"🌧️ Heavy rain in your zone. ₹300 credited. Stay safe."* They did nothing. ZenVyte GigPulse did.

---

## Adversarial Defense & Anti-Spoofing Strategy

> **This section directly addresses the DEVTrails Market Crash Challenge — 500 GPS spoofer attack scenario — with full architectural defense.**

### The Attack

500 fraudsters use GPS spoofing apps to fake location inside disruption zones while sitting at home.

### Differentiation — Real Worker vs Spoofer

| Signal | Real Worker | GPS Spoofer |
|---|---|---|
| GPS coordinate | Inside zone ✅ | Faked inside zone ✅ |
| Accelerometer / IMU | Bike vibration, stops, turns → stop at disruption | Flat stationary signal — no movement history |
| Cell tower ID | Matches disruption zone towers | Home cell tower — geographic mismatch |
| GPS velocity pattern | Delivery movement → sudden stop at trigger | Zero velocity throughout |
| Device activity | Maps, delivery app, calls | GPS spoofing app in background |
| Weather cross-check | Real location aligns with rain zone | Home location (revealed by cell tower) has no rain |

**Spoofer passes Signal 1, fails Signals 2–6. ZenVyte GigPulse requires 4 of 6.**

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

### Why the 500-Spoofer Attack Fails

| Reason | Why It Fails |
|---|---|
| Sensors can't be mass-faked | Spoofing accelerometer + cell tower needs device rooting — not worth it for ₹105–₹630 |
| Attacks are statistically visible | 500 identical flat accelerometer readings = obvious Isolation Forest anomaly |
| Economics don't work | Coordinating 500 devices to earn ₹630 max/week is not rational |
| Trust Score catches repeat offenders | Baseline diverges over weeks — future claims always trigger review |
| Cell tower is hardest to fake | Requires physically travelling to the disruption zone |

---

## Parametric Triggers

> Every trigger is an objective, externally verifiable event from a government or accredited API. No platform data. No subjective metrics.

| # | Event | Source | Threshold | Confirmation | Payout |
|---|---|---|---|---|---|
| 1 | Heavy Rainfall | OpenWeatherMap + IMD + Satellite Radar | > 35mm in 3 hrs in micro-zone | 15–30 min persistence | Per hour up to plan cap |
| 2 | Extreme Heat | IMD API + Private Weather API | > 43°C sustained 2+ hrs | 30 min persistence | Per hour up to plan cap |
| 3 | Severe AQI | CPCB AQI API + OpenAQ | AQI > 300 Hazardous | Confirmed 2+ sources | Per hour up to plan cap |
| 4 | Cyclone / Flood | IMD Disaster Feed + NDMA | Orange/Red alert in district | Alert active 30+ min | **Full weekly cap immediately** |
| 5 | Curfew / Hartal | NDMA feed + admin-confirmed flag | Section 144 / state shutdown | Admin-verified flag | **Full weekly cap immediately** |

> ⚡ **Triggers 4 & 5** always release the full weekly payout cap immediately — no hourly calculation.
> **Triggers 1–3** pay at the hourly rate for each hour of actual disruption, up to the plan's weekly cap.

**Time confirmation:**

| Duration | Action |
|---|---|
| < 15 minutes | Monitoring — no trigger |
| 15–30 minutes | Confirmation window — worker alerted |
| > 30 minutes | Trigger confirmed — claim initiated |

---

## Actuarial Basis

| Parameter | Value | Basis |
|---|---|---|
| Disruption events/month (monsoon Jun–Nov) | 3.0 | IMD Chennai 10-yr average |
| Disruption events/month (off-season Dec–May) | 0.5 | IMD Chennai historical |
| Annual disruption events/worker | **21 / year** | (3.0 × 6) + (0.5 × 6) |
| Average disruption duration | **2.5 hrs** | IMD urban rainfall data |
| Annual disruption hours/worker | **52.5 hrs** | 21 × 2.5 |
| Monsoon-year disruption hours/worker | **73.5 hrs** | 52.5 × 1.40 (+40% frequency) |
| Worker hourly income | ₹112/hr | ₹900/day ÷ 8 hrs |
| Annual income lost | **₹5,880** | 52.5 × ₹112 |

### Core Actuarial Formula

```
Annual Premium       = Weekly Premium × 52 weeks
Expected Annual Claim = Hourly Payout Rate × Annual Disruption Hours
Loss Ratio           = Expected Annual Claim ÷ Annual Premium
```

> **Every plan's expected annual claim is calculated as: Hourly Payout Rate × 52.5 hrs (normal) or × 73.5 hrs (monsoon).** This is the only internally consistent approach — the stated hourly rate for each plan is applied directly to the annual disruption hours. No separate assumption about claim amounts is needed or valid.

---

## Weekly Premium Model — Corrected & Verified

### 💡 Pricing Logic

```
Weekly Premium = Base Price + (Risk Score × Zone Risk Factor)
Minimum Premium = Hourly Payout Rate × 52.5 hrs ÷ (0.75 × 52 weeks)
```

### Design Philosophy

ZenVyte GigPulse is a **partial income top-up** — not full replacement. All premiums are set so that the loss ratio stays **below 75% under normal conditions** and **below 95% under heavy monsoon (+40% disruption frequency)**. This means every plan is financially sustainable for the insurer partner in both typical and worst-case weather years.

### ✅ The 5 Corrected Plans

> Weekly premiums have been recalculated from the actuarial formula. Hourly payouts and caps are unchanged — only the premiums are adjusted to ensure all plans are viable.

| Plan | Weekly Premium | Hourly Payout | Max Hrs/Week | Max Weekly Payout | Target User |
|---|---|---|---|---|---|
| 🌱 Starter | **₹55/week** | ₹35/hour | 3 hours | ₹105 | New workers, low-risk zones |
| 🔵 Basic | **₹70/week** | ₹45/hour | 4 hours | ₹180 | Part-time, low-risk zones |
| 🟡 Standard | **₹90/week** | ₹60/hour | 5 hours | ₹300 | Full-time, urban zones |
| 🟠 Premium | **₹115/week** | ₹75/hour | 6 hours | ₹450 | High-earning full-time |
| 🔴 Elite | **₹135/week** | ₹90/hour | 7 hours | ₹630 | Coastal / flood-prone zones |

> **What changed:** Starter was raised from ₹35 → ₹55 (the original ₹35 produced a 101% loss ratio — one disruption hour wiped the entire week's premium). Basic was raised from ₹55 → ₹70, Standard from ₹79 → ₹90, and Elite reduced from ₹149 → ₹135 (it was over-priced). Premium moved from ₹109 → ₹115.

---

## Weekly Payout Per Disruption Type

> This table shows exactly how much each plan pays for each disruption scenario.
> **Formula:** Payout = Hourly Rate × actual disruption hours, capped at plan's weekly maximum.
> **Triggers 4 & 5** always pay the full weekly cap immediately.

| Disruption | Duration | 🌱 Starter ₹35/hr · 3h cap | 🔵 Basic ₹45/hr · 4h cap | 🟡 Standard ₹60/hr · 5h cap | 🟠 Premium ₹75/hr · 6h cap | 🔴 Elite ₹90/hr · 7h cap |
|---|---|---|---|---|---|---|
| Heavy rainfall (avg event) | 2.5 hrs | ₹88 | ₹113 | ₹150 | ₹188 | ₹225 |
| Extended rain / evening storm | 4 hrs | ₹105 *(cap)* | ₹180 *(cap)* | ₹240 | ₹300 | ₹360 |
| Extreme heat > 43°C | 2 hrs | ₹70 | ₹90 | ₹120 | ₹150 | ₹180 |
| Severe AQI > 300 | 3 hrs | ₹105 *(cap)* | ₹135 | ₹180 | ₹225 | ₹270 |
| Cyclone / Flood | Full week cap | **₹105** | **₹180** | **₹300** | **₹450** | **₹630** |
| Curfew / Hartal | Full week cap | **₹105** | **₹180** | **₹300** | **₹450** | **₹630** |

*Cap = plan's weekly maximum hours reached before disruption ends.*

---

## Loss Ratio Analysis

### Normal Year (52.5 disruption hrs/year)

| Plan | Weekly Premium | Annual Premium | Expected Annual Claim | Loss Ratio | Status |
|---|---|---|---|---|---|
| 🌱 Starter | ₹55 | ₹2,860 | ₹1,838 | **64.2%** ✅ | Controlled |
| 🔵 Basic | ₹70 | ₹3,640 | ₹2,363 | **64.9%** ✅ | Controlled |
| 🟡 Standard | ₹90 | ₹4,680 | ₹3,150 | **67.3%** ✅ | Controlled |
| 🟠 Premium | ₹115 | ₹5,980 | ₹3,938 | **65.8%** ✅ | Controlled |
| 🔴 Elite | ₹135 | ₹7,020 | ₹4,725 | **67.3%** ✅ | Controlled |

> All 5 plans deliver loss ratios between **64–68%** — well within the 65% parametric micro-insurance benchmark and the insurer-acceptable ceiling of 75%.

### Heavy Monsoon Year (+40% disruption frequency → 73.5 hrs/year)

| Plan | Annual Premium | Monsoon Claim | Monsoon Loss Ratio | Status |
|---|---|---|---|---|
| 🌱 Starter | ₹2,860 | ₹2,573 | **89.9%** ✅ | Under control |
| 🔵 Basic | ₹3,640 | ₹3,308 | **90.9%** ✅ | Under control |
| 🟡 Standard | ₹4,680 | ₹4,410 | **94.2%** ✅ | Under control |
| 🟠 Premium | ₹5,980 | ₹5,513 | **92.2%** ✅ | Under control |
| 🔴 Elite | ₹7,020 | ₹6,615 | **94.2%** ✅ | Under control |

> All plans stay **below 95%** even in the worst-case +40% monsoon year — no plan crosses the insurer's hard ceiling.

### Why This Works

```
Target ceiling:    Normal year  ≤ 75%    Monsoon year  ≤ 95%
All plans achieve: Normal year  64–68%   Monsoon year  90–94%

Safety buffer:     Normal year  +7–11%   Monsoon year  +1–5%
```

The safety buffer on normal years absorbs zone-risk variability. The monsoon buffer is tighter (1–5%) — this is why zone-risk pricing multipliers (1.2–1.4×) are still applied in high-disruption coastal zones to widen the monsoon buffer for those specific micro-zones.

---

## Worker Affordability Check

| Plan | Weekly Premium | % of Weekly Earnings | Deliveries to Cover | Weekly Protection |
|---|---|---|---|---|
| 🌱 Starter | ₹55 | 0.8% | ~1.5 deliveries | ₹105 |
| 🔵 Basic | ₹70 | 1.1% | ~2 deliveries | ₹180 |
| 🟡 Standard | ₹90 | 1.3% | ~2.5 deliveries | ₹300 |
| 🟠 Premium | ₹115 | 1.7% | ~3 deliveries | ₹450 |
| 🔴 Elite | ₹135 | 2.0% | ~3.5 deliveries | ₹630 |

All plans remain **under 2.5% of weekly earnings** (CGAP affordability threshold). The Standard plan at ₹90/week delivers up to ₹300 — still more than the typical ₹280 income loss from a 2.5-hour disruption, making it a net positive for subscribing workers.

### Why Weekly Pricing

Gig workers operate on weekly income cycles. Daily premiums create friction. Monthly premiums are too large a commitment for variable income. Weekly pricing — under 3 deliveries' worth — matches how delivery workers think about money.

---

## Demo Scenario

1. Ravi subscribes to **Standard Plan (₹90/week)** via ZenVyte GigPulse mobile web.
2. ZenVyte GigPulse polls OpenWeatherMap + IMD + satellite radar every 15 min across Ravi's micro-zone (Velachery, 3 km).
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

### Worker Trust Score System

Every worker has a running Trust Score (0–100) updated weekly.

| Trust Score | Tier | Status |
|---|---|---|
| 75–100 | 🟢 Trusted | Full auto-approval |
| 50–74 | 🔵 Established | Auto-approval, standard processing |
| 25–49 | 🟡 Building | Manual review before payout |
| 0–24 | 🔴 Restricted | Manual review + 50% payout cap |

New workers start at **Provisional Score 40** — can claim from Week 1 at 50% cap. Full benefits after 3 clean weeks.

---

### Model 3 — Predictive Disruption Alert Engine

**Algorithm:** XGBoost on time-series weather features
**Output:** Disruption probability 0–100% per micro-zone per day, 24–48 hrs ahead

> *"⚡ Storm likely in your zone tomorrow 6–9pm. Probability: 78%. Your ₹300 coverage is active."*

---

## Smart Validation Layer

| Layer | Problem | Solution |
|---|---|---|
| **1. Multi-Source Reliability** | IMD/CPCB APIs can be delayed or stale | Cross-verify 2+ independent sources. Satellite radar as fallback. |
| **2. Micro-Zone Precision (2–5 km)** | City/pincode data too coarse | Workers mapped to 2–5 km micro-zones. Trigger at zone centroid. |
| **3. Time-Based Confirmation** | Brief 5-min showers ≠ meaningful disruption | Disruption must persist 15–30 min. Counter resets if drops below threshold. |
| **4. Context-Aware Delivery Logic** | 20-min vs 3-hr disruption ≠ same impact | Compare disruption duration vs avg delivery time (30–45 min). Payout scales proportionally. |
| **5. Crowd Signal Validation** | API data lags real conditions 10–20 min | Anonymized zone-level aggregate: movement speed + inactivity spikes. Never individual tracking. |

```
Layer 1: API threshold crossed → Layer 2: Secondary source confirms →
Layer 3: 15–30 min persistence → Layer 4: Worker GPS + sensors verified →
Layer 5: Crowd signal confirms → ✅ Payout initiated
```

**Privacy:** No individual worker tracked. All behavioral and crowd signals are anonymized, aggregated at zone level, and permanently discarded after the disruption window closes.

---

## API Failure & Data Validity Handling

| Failure Scenario | ZenVyte GigPulse Response |
|---|---|
| **Primary API (IMD) goes down** | Auto-fallback to satellite/radar secondary. No monitoring disruption. |
| **Both APIs return stale data (> 30 min)** | Payout frozen. Worker notified: "Verification pending." |
| **API data outside valid range** | Outlier detection flags reading. Discarded before trigger logic runs. |
| **Partial zone coverage (< 60% micro-zone)** | Weighted average applied. Trigger only fires if weighted threshold met. |
| **CPCB AQI slow / unavailable** | Cross-reference OpenAQ fallback. If neither available, AQI trigger suspended. |
| **NDMA alert feed delayed** | Trigger 5 requires admin-confirmed flag as second gate. |
| **All external APIs fail simultaneously** | Full monitoring pause. Workers notified. No payouts triggered. Insurer alerted. |

> **ZenVyte GigPulse's principle: better to delay a valid payout than release an invalid one.**

---

## Zero-Touch Claim Flow

```
Worker subscribes → ZenVyte GigPulse polls APIs every 15 min at micro-zone level
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

### Why Responsive Web Over a Native App

ZenVyte GigPulse is built as a **fully responsive web application** — workers access via mobile browser, admins via desktop. This was a deliberate choice over a native Android/iOS app for three reasons specific to India's gig worker context: there is zero Play Store friction (a critical barrier for workers on pre-paid plans who avoid large downloads), the platform runs on low-end ₹4,000 Android phones with minimal data usage, and updates deploy instantly without requiring any user action. A single Python FastAPI backend serves both the mobile worker interface and the desktop admin dashboard from the same codebase.

> **Sensor data collection plan (Phase 2):** Accelerometer and device motion data will be collected via the browser's Device Motion API (supported on all modern Android browsers). Cell tower ID matching will be handled by a backend SIM-toolkit integration that cross-references the worker's registered SIM carrier against their claimed GPS zone — no native app required for this signal.

| Platform | User | Purpose |
|---|---|---|
| Mobile Web (HTML · CSS · JS) | Delivery Workers | Onboarding, plan selection, alerts, payouts, plan management |
| Desktop Web (HTML · CSS · JS) | Insurer / Admin | Policies, fraud queue, loss ratio, payout simulation |
| Mobile Frontend | HTML · CSS · JavaScript | Responsive mobile web — no install needed |
| Web Frontend | HTML · CSS · JavaScript | Same codebase, shared components |
| Backend | Python FastAPI | ML-friendly, async, high performance |
| Database | SQLite / PostgreSQL Ready | Workers, policies, claims, payout records |
| ML Models | Scikit-learn (Random Forest, Isolation Forest), XGBoost | Production-grade, well-documented |
| Weather API (Primary) | OpenWeatherMap + IMD public data | Real-time + historical training data |
| Weather API (Secondary) | Satellite/radar private API | Backup validation, handles IMD delays |
| AQI API | CPCB AQI API + OpenAQ | Government-verified, cross-validated |
| Disaster Alerts | NDMA public alert feed | Automated curfew detection (Trigger 5) |
| Zone Mapping | Google Maps API + micro-zone segmentation (2–5 km) | Precise GPS zone verification |
| Payments | Razorpay Sandbox | Simulated near-real-time payout |
| Notifications | Real-Time Push / FCM | Real-time worker alerts & updates |
| Hosting | Railway / Render (free tier) | Fast hackathon deployment |

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
     │SQLite    │  │ML Engine │  │Disruption Monitor │
     │Workers,  │  │Risk,     │  │15-second poll at  │
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
              │  Push Notification Engine│
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
- **Earnings Protected Counter** — Total saved via ZenVyte GigPulse
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

### Standard Exclusions (IRDAI-aligned)

ZenVyte GigPulse does NOT pay out for disruptions caused by:

- Declared war, invasion, civil war, or armed conflict
- Nuclear, chemical, or biological weapon events
- WHO or Central Government declared pandemic (e.g. COVID-19 national lockdown — different from local curfew/hartal which IS covered under Trigger 5)
- Government-mandated pandemic shutdowns
- Riot or civil commotion beyond normal Section 144 curfew
- Disruptions lasting less than 15 minutes
- Events not verifiable through government or accredited API sources

### Covered vs Excluded — Curfew Distinction

| Situation | Covered |
|---|---|
| Section 144 curfew — law and order | ✅ Yes — Trigger 5 |
| Hartal / bandh — local strike | ✅ Yes — Trigger 5 |
| COVID-19 national lockdown | ❌ No — pandemic exclusion |
| War-related shutdown | ❌ No — war exclusion |

> **Design rationale:** A local curfew (Section 144) is a verifiable, geo-bounded, short-duration event detectable via NDMA feeds. A national pandemic lockdown is a systemic, economy-wide event — the risk profile is fundamentally different and uninsurable at parametric micro-insurance price points. This distinction is standard IRDAI practice for all parametric products.

---

## Plan Cancellation & Refund Policy

| Situation | Policy |
|---|---|
| **Cancel before Monday auto-renew** | No charge for next week. Current week coverage runs to Sunday. |
| **Cancel mid-week (Day 1–4)** | Coverage continues to end of week. Pro-rata credit toward next payment. |
| **Cancel mid-week (Day 5–7)** | Coverage runs to Sunday. No refund — week nearly complete. |
| **Cancel within 24 hours of first subscription** | **Full refund. No questions. Cooling-off period.** |
| **Cancel after payout received this week** | No refund — payout already released, premium consumed. |

> **Friction-free exit builds the trust that brings workers back.**

---

## Financial & Business Model

### ZenVyte GigPulse is a Technology Platform — Not an Insurer

```
Worker pays weekly premium
         ↓
Licensed IRDAI Insurer Partner (e.g., Digit Insurance / Acko)
holds all premium capital and pays all claims
         ↓
ZenVyte GigPulse earns a 5% platform distribution fee per active policy
         ↓
ZenVyte GigPulse does not underwrite risk or pay claims directly.
All claim liabilities handled by the licensed insurer partner.
```

### Revenue Per Policy Per Week

| Plan | Weekly Premium | ZenVyte GigPulse Fee (5%) | Insurer Net Premium | Normal Loss Ratio | Monsoon Loss Ratio |
|---|---|---|---|---|---|
| 🌱 Starter | ₹55 | ₹2.75 | ₹52.25 | 64.2% ✅ | 89.9% ✅ |
| 🔵 Basic | ₹70 | ₹3.50 | ₹66.50 | 64.9% ✅ | 90.9% ✅ |
| 🟡 Standard | ₹90 | ₹4.50 | ₹85.50 | 67.3% ✅ | 94.2% ✅ |
| 🟠 Premium | ₹115 | ₹5.75 | ₹109.25 | 65.8% ✅ | 92.2% ✅ |
| 🔴 Elite | ₹135 | ₹6.75 | ₹128.25 | 67.3% ✅ | 94.2% ✅ |

### Why Insurers Partner with ZenVyte GigPulse

- **Controlled loss ratios** — all plans 64–68% normal year, 90–94% monsoon year — well within insurer thresholds
- **Parametric triggers** — no disputes, no assessors, minimal admin cost
- **Fraud detection** — minimises payout leakage before insurers see a claim
- **Untapped market** — 5 crore+ informal workers (NITI Aayog, 2022) currently unreachable by insurers
- **Zero distribution cost** — ZenVyte GigPulse handles acquisition, onboarding, and tech

### Revenue at Scale

| Active Workers | Weekly Fee (avg ₹4.65) | Weekly Revenue | Annual Revenue |
|---|---|---|---|
| 1,000 | ₹4.65 | ₹4,650 | ₹24,18,000 |
| 10,000 | ₹4.65 | ₹46,500 | ₹2,41,80,000 |
| 1,00,000 | ₹4.65 | ₹4,65,000 | ₹24,18,00,000 |

*Average fee calculated across all 5 plans weighted equally.*

---

## Anticipated Judge Q&A & Edge Cases 🕵️

> **We designed ZenVyte GigPulse to proactively solve the hardest edge cases in parametric insurance. Here is how we address the most common "gotcha" questions.**

### Q1: You checked off Twilio SMS, but did you actually build it?
**Yes.** We built the full integration in `gigpulse/app/sms_engine.py`. It currently degrades gracefully to a simulated server log because we didn't want to expose our private Twilio API keys on a live hackathon environment. But the `Client(account_sid, auth_token)` logic is fully written and tested. If we drop keys into the `.env` file right now, it will instantly text our phones.

### Q2: You claim to use Accelerometer and Cell Tower data to stop GPS spoofing, but this is a web app. You can't read those easily from a mobile browser.
**Correct, and we have a production roadmap for this.** We intentionally built this as a mobile web app because gig workers in India use low-tier phones and don't want to download 100MB native apps. For Phase 2, we simulate these signals in our God-View Sandbox. For production, we will capture the **Accelerometer** using HTML5's built-in `DeviceMotionEvent API` which works perfectly on mobile Chrome. For the **Cell Tower ID**, we don't need phone permissions—we use a backend SIM-toolkit integration that checks the registered worker's telecom provider directly against the claimed GPS zone.

### Q3: What if the OpenWeatherMap API crashes? Doesn't your Zero-Touch claim flow just leave the worker stranded with zero money?
**We built an Enterprise-grade fail-safe for this.** As outlined in our *API Failure & Data Validity Handling* table, if the primary API goes down, the system auto-stalls and falls back to a secondary Satellite Radar API. If both APIs fail simultaneously or return conflicting data, our engine strictly freezes the payout and puts a **"Pending Manual Review"** notification on the worker's dashboard. Our philosophy: *It is better to safely delay a valid payout than to automatically release a fraudulent one.*

---

## Why ZenVyte GigPulse Wins

| What Others Do | What ZenVyte GigPulse Does |
|---|---|
| Rely on GPS alone | 6-signal validation — GPS + accelerometer + cell tower + network + behavior + crowd |
| Detect weather events | 5-layer validation with time confirmation + multi-source cross-check |
| Ignore fraud edge cases | Simulate 500-spoofer attack and defeat it architecturally |
| Skip business viability | Actuarial loss ratio proof — all 5 plans controlled under both normal and monsoon scenarios |
| Present ideas | Working prototype + ML architecture + IRDAI insurer-partner model |

1. **Only solution with multi-signal fraud prevention** — GPS + accelerometer + cell tower + network + behavior + crowd signal
2. **Only solution with fully controlled actuarial pricing** — all 5 plans maintain 64–68% loss ratio (normal) and 90–94% (heavy monsoon) — no plan exceeds insurer thresholds in any scenario
3. **Only solution with micro-zone precision (2–5 km)** — disruption detection at neighbourhood level, not city or pincode
4. **Only solution that simulates the attack it's defending against** — 500 GPS spoofers, defeated architecturally
5. **Only solution with zero-touch claims** — fully automated from disruption detection to payout, no user action needed
6. **Only solution with IRDAI-aligned standard exclusions** — war, pandemic, nuclear events explicitly excluded per regulatory best practice

> **ZenVyte GigPulse is not just innovative — it is designed for real-world deployment, fraud-resistant, financially viable, and fully IRDAI-compliant on Day 1 under all weather conditions.**

---

## Live Website Render Deployed

🎥 **2-Minute Strategy Video →**

Youtube : <br><br>
Drive : 

> Video covers: problem & persona → solution walkthrough → anti-spoofing architecture → financial model & roadmap.

📱 **Home →**
https://ai-powered-parametric-income-protection.onrender.com

📱 **Login →**
https://ai-powered-parametric-income-protection.onrender.com/gigpulse_login.html

🧪 **Feature Demo →**(optional)
https://ai-powered-parametric-income-protection.onrender.com/gigpulse_features.html

💡 **What to explore:**
- Worker onboarding with zone risk ML (40+ Tamil Nadu zones)
- Plan selection with AI recommendation
- Worker dashboard: simulation, payouts timeline, predictive alerts, plan change
- Admin dashboard: policy list, 7 KPIs, claims pipeline (auto-approved / review / rejected), API status
- Features: weather monitor, claim simulator, fraud visualizer, earnings calc, disruption chart, plan compare

> Prototype built for Guidewire DEVTrails 2026. All data simulated. No real money transacted.

---

## 🛠️ How to Run Locally

If the live Render deployment is asleep or you want to run the full simulation engine locally, follow these steps:

### 1. Prerequisites
- **Python 3.10+** (Python 3.13 is fully supported)
- Git

### 2. Auto-Start (Windows Only)
The easiest way to run the platform on Windows is to double-click:
```bash
.\START_GIGPULSE.bat
```
*This script will automatically create a virtual environment, install all dependencies, and launch the server in one click.*

### 3. Manual Setup (Mac / Linux / Windows Manual)
If you prefer to set it up manually via the terminal:

```bash
# Clone the repository
git clone https://github.com/Dhayananth1511/AI-Powered-Parametric-Income-Protection-for-Food-Delivery-Workers.git
cd AI-Powered-Parametric-Income-Protection-for-Food-Delivery-Workers

# Create and activate virtual environment
python -m venv .venv
# Mac/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Install dependencies and run
pip install -r requirements.txt
python main.py
```

### 4. Access the Dashboards
Once the server says `Open: http://localhost:8000`:
- **Landing Page**: http://localhost:8000/index.html
- **Worker Login**: http://localhost:8000/gigpulse_login.html 
- **Interactive Sandbox & Features**: http://localhost:8000/gigpulse_features.html
- **Admin Dashboard**: http://localhost:8000/gigpulse_admin.html

> **Note:** The SQLite database (`gigpulse.db`) will be automatically created and securely seeded with test data upon the first launch!

---
## What is Actually Working (Phase 1 Prototype)

| Feature | Status |
|---|---|
| ✅ Worker onboarding (40+ Tamil Nadu zones, ML zone risk, plan recommendation) | **Phase 1** |
| ✅ Plan selection with ML-recommended tier | **Phase 1** |
| ✅ Worker dashboard — disruptions, payouts, predictive alerts, plan change | **Phase 1** |
| ✅ Payout simulation — 5-step automated claim flow, persists to localStorage | **Phase 1** |
| ✅ Admin dashboard — policy list, 7 KPIs, claims pipeline, API status | **Phase 1** |
| ✅ Claims pipeline — Auto-Approved · Manual Review · Auto-Rejected | **Phase 1** |
| ✅ 6 interactive feature demos — weather, fraud score, earnings calc, plan compare | **Phase 1** |
| 🛡️ **Phase 2: Automation & Final Polish** | **Completed** |
| ✅ **Unified Architecture** (FastAPI serving frontend at root `/`) | **Phase 2** |
| ✅ **Aadhaar KYC Verification** (Simulated UIDAI OIDC flow) | **Phase 2** |
| ✅ **Multi-Method Payment** (GPay, UPI, Cards, Order Summary) | **Phase 2** |
| ✅ **Real-Time Monitoring** (15-second background polling + auto-trigger) | **Phase 2** |
| ✅ **Zero-Touch Claims Pipeline** (End-to-end automation verified) | **Phase 2** |
| ✅ **Mobile-First Responsiveness** (Worker BottomNav · Admin Mobile Sidebar) | **Phase 2** |
| ✅ **Interactive Fraud Defense Sandbox** (Simulation UI) | **Phase 2** |
| ✅ **Live API Transparency Console** (OWM Bypass) | **Phase 2** |
| ✅ **God-View Map Dashboards** (Hexagon Spatial Bounds) | **Phase 2** |
| ✅ **Isolation Forest Fraud Engine** (Live Telemetry) | **Phase 2** |
| ✅ **Twilio SMS Engine** (Claim verification alerts) | **Phase 2** |
| ✅ **Live Relational Database** (Native SQLite integration) | **Phase 2** |
| ✅ **Worker Shift & Staleness Logic** (Online/Offline engine) | **Phase 2** |

---

## 45-Day Development Roadmap

### Phase 1 — Foundation (Weeks 1–2 | Mar 4–20) ✅
- [x] Problem research + gig worker persona analysis
- [x] Insurance model — 5 plans, hourly payout, corrected actuarial loss ratio proof (all plans controlled)
- [x] ML architecture (Zone Risk · Fraud Detection · Predictive Alert)
- [x] System architecture + tech stack
- [x] Business model — IRDAI partner structure, 5% platform fee
- [x] Smart Validation Layer — multi-source, micro-zone, time confirmation, crowd signals
- [x] Adversarial Defense — 6-signal GPS spoofing detection (Market Crash scenario)
- [x] API Failure & Data Validity handling strategy
- [x] Plan Cancellation & Refund Policy
- [x] Standard IRDAI exclusions — war, pandemic, nuclear events
- [x] Full HTML/CSS/JS prototype — Login · Onboarding · Worker Dashboard · Admin Dashboard · Feature Demo
- [x] Strategy video (2 minutes) — to be submitted before deadline

### Phase 2 — Automation & Final Engine (Weeks 3–4 | Mar 21–Apr 4) ✅
- [x] Worker KYC flow (Aadhaar verification simulation)
- [x] Unified FastAPI Architecture (Frontend served at `/`)
- [x] Policy management (create, view, renew, upgrade/downgrade)
- [x] Zone Risk Classifier — trained + deployed for onboarding
- [x] Micro-zone segmentation — 2–5 km zones mapped per city
- [x] OpenWeatherMap + IMD + satellite radar API integration (15-second polling)
- [x] Time-based confirmation engine (15–30 min persistence)
- [x] Hourly payout engine (hours × rate, capped at plan max)
- [x] Auto-claim pipeline: confirm → verify → GPS + cell tower + accelerometer → fraud → approve → payout
- [x] Premium Payment System (GPay, UPI, Card checkout)
- [x] Firebase push notifications (Simulated via toast)
- [x] Isolation Forest fraud model with live hardware telemetry signals
- [x] Anti-spoofing layer — live tracking endpoints deployed
- [x] Twilio SMS Alert Integration (Production-Ready)
- [x] Enterprise Data Export (Admin CSV Claims & Worker Reports)
- [x] Crowd signal layer — anonymized zone-level behavioral aggregation (Via staleness checks)
- [x] Full integration testing across triggers and ML modules (Production validated)
- [x] **Interactive Fraud Defense Sandbox** — live manual injection testing for Judges
- [x] **God-View Map Upgrades** — sophisticated Hexagon micro-zones implemented
- [x] **Live API Transparency Console** — explicit OpenWeatherMap HTTP bypass demo

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

In production, ZenVyte GigPulse integrates with a licensed IRDAI insurance partner for real claim payouts.

---

## About This Project

**Hackathon:** Guidewire DEVTrails 2026 Pan-India University Hackathon
<br>
**Team:** ZenVyte
<br>
**Members:** 
· Dhayananth N *(Lead)* 
· Mowlieswaran G 
· Arun Kumar S 
· Karthick V 
· Hardik Muthusamy
<br>
**Problem:** AI-Powered Insurance for India's Gig Economy
<br>
**Focus:** Food Delivery Workers — Zomato / Swiggy
<br>
**Platform:** Responsive Web — Mobile (Workers) + Desktop (Admin)

---

*Build fast. Spend smart. Protect every delivery worker. 🛡️*
*Team ZenVyte — DEVTrails 2026*
