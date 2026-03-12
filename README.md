# GigShield 🛡️
### AI-Powered Parametric Income Protection for Food Delivery Workers
### Team ZenVyte | Guidewire DEVTrails 2026

> *"A delivery worker is stuck during a Chennai thunderstorm. They didn't file a claim. They didn't call anyone. Their phone just buzzed — ₹500 credited. GigShield works so they don't have to."*

---

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Our Solution](#our-solution)
3. [Delivery Worker Persona](#delivery-worker-persona)
4. [Parametric Triggers](#parametric-triggers)
5. [Weekly Premium Model](#weekly-premium-model)
6. [AI/ML Architecture](#aiml-architecture)
7. [Zero-Touch Claim Flow](#zero-touch-claim-flow)
8. [Platform & Tech Stack](#platform--tech-stack)
9. [System Architecture](#system-architecture)
10. [Dashboards](#dashboards)
11. [Coverage Scope & Exclusions](#coverage-scope--exclusions)
12. [Financial & Business Model](#financial--business-model)
13. [45-Day Development Roadmap](#45-day-development-roadmap)
14. [Strategy Video](#strategy-video)

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
- Triggers an instant payout — in under 30 seconds, with no human intervention

The worker's only job is to subscribe to a weekly plan. Everything else is automated.

**Key differentiators:**
- Every trigger is independently verifiable through government or third-party APIs — no platform data, no subjective metrics
- ML-driven dynamic zone-based pricing makes the model financially sustainable
- Predictive disruption alerts warn workers 24–48 hours before an event
- Zero-touch claim experience — no forms, no uploads, no waiting
- GigShield operates as a technology platform — all policies underwritten by a licensed IRDAI insurer partner

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

**With GigShield:** Phone buzzes. *"🌧️ Heavy rain detected in your zone. ₹500 credited to your account. Stay safe."* They didn't do anything. GigShield did.

---

## Parametric Triggers

> **Design Principle:** Every trigger must be an objective, externally verifiable event from a government or accredited third-party source. GigShield does not use platform demand data, traffic metrics, or any subjective signal.

### Trigger Table

| # | Disruption Event | Data Source | Threshold | Payout Trigger |
|---|---|---|---|---|
| 1 | Heavy Rainfall | OpenWeatherMap API + IMD | Rainfall > 35mm within 3 hours in worker's pincode | Per disruption hour |
| 2 | Extreme Heat | IMD API | Sustained temperature > 43°C for 2+ hours | Per disruption hour |
| 3 | Severe Air Pollution | CPCB AQI API (free public API) | AQI > 300 (Hazardous category) | Per disruption hour |
| 4 | Cyclone / Flood Alert | IMD Disaster Alert Feed | Orange or Red alert issued for worker's district | Full plan cap + 24hr extension |
| 5 | Government Curfew / Hartal | Verified news API + admin-confirmed flag | Section 144 order or state-declared shutdown in worker's zone | Full plan cap |

### Why These Triggers Are Compliant

Each trigger above satisfies all three compliance requirements:

1. **Externally verifiable** — sourced from IMD, CPCB, or a government-issued order. Not derived from platform data.
2. **Parametric** — defined by a measurable threshold that is either crossed or not. No subjective assessment.
3. **Causally linked to income loss** — each event directly prevents outdoor delivery work, causing loss of hourly wages.

---

## Weekly Premium Model

### How GigShield Pays — Hourly Micro-Payout Model

GigShield compensates workers based on **disruption hours**, not full days. This is fairer to workers (most disruptions last 2–4 hours, not a full day) and financially sustainable for the platform.

```
Worker earns: ₹900/day ÷ 8 working hours = ₹112/hour average
Typical disruption duration: 2–4 hours (evening peak)
Realistic income lost per event: ₹224 – ₹448
```

### The 5 Plans

| Plan | Weekly Premium | Hourly Payout Rate | Max Hours/Week | Max Weekly Payout | Best For |
|---|---|---|---|---|---|
| 🌱 Starter | ₹25/week | ₹75/hour | 2 hours | ₹150 | New workers, low-risk zones |
| 🔵 Basic | ₹40/week | ₹75/hour | 4 hours | ₹300 | Part-time delivery partners |
| 🟡 Standard | ₹55/week | ₹100/hour | 5 hours | ₹500 | Full-time workers, urban zones |
| 🟠 Premium | ₹75/week | ₹125/hour | 6 hours | ₹750 | High-earning full-time partners |
| 🔴 Elite | ₹99/week | ₹125/hour | 8 hours | ₹1,000 | Coastal/flood-prone high-risk zones |

### The Actuarial Basis

GigShield's premium model is grounded in 10 years of IMD historical weather data for Chennai urban delivery zones.

**Base assumptions (Chennai):**
- Average disruption events per month during monsoon season (June–November): ~4 events
- Average disruption events per month during off-season: ~1 event
- Annual average disruption events: ~30/year
- Average disruption duration per event: ~3 hours
- Average hourly income loss: ₹112/hour

**Expected annual disruption hours per worker:** 30 events × 3 hours = **90 hours/year**

**Expected annual income loss per worker:** 90 hours × ₹112 = **₹10,080/year**

**Standard plan (₹55/week) annual premium collected:** ₹55 × 52 = **₹2,860/year**

> The premium gap between collected premium and expected payout is covered by the underwriting insurer partner. GigShield earns a platform distribution fee of ₹8 per active policy per week, with zero claims liability.

### Why Weekly Pricing

Gig workers on Zomato/Swiggy operate on a weekly earnings and payout cycle. Daily premiums create friction. Monthly premiums are too large a commitment for workers with variable income. Weekly pricing — small enough to feel negligible (less than the earnings from 1–2 deliveries), meaningful enough to provide real coverage — matches how delivery workers actually think about money.

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
GigShield earns a platform distribution fee per active policy
         ↓
GigShield's claims liability: ₹0
```

### GigShield Revenue Per Policy Per Week

| Plan | Weekly Premium | GigShield Platform Fee | Insurer Keeps |
|---|---|---|---|
| 🌱 Starter | ₹25 | ₹4 | ₹21 |
| 🔵 Basic | ₹40 | ₹6 | ₹34 |
| 🟡 Standard | ₹55 | ₹8 | ₹47 |
| 🟠 Premium | ₹75 | ₹10 | ₹65 |
| 🔴 Elite | ₹99 | ₹13 | ₹86 |

### Revenue at Scale

| Active Workers | Avg Plan | Weekly Platform Revenue | Annual Revenue |
|---|---|---|---|
| 1,000 | Standard | ₹8,000/week | ₹41,60,000/year |
| 10,000 | Standard | ₹80,000/week | ₹4,16,00,000/year |
| 1,00,000 | Standard | ₹8,00,000/week | ₹41,60,00,000/year |

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
- Score < 0.25 → Recommend Starter / Basic
- Score 0.25–0.55 → Recommend Standard
- Score 0.55–0.75 → Recommend Premium
- Score > 0.75 → Recommend Elite

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
- Score < 30 → Auto-approve, payout released immediately
- Score 30–70 → Human review queue (admin dashboard)
- Score > 70 → Auto-reject, worker notified with appeal option

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

**Worker-facing UX:**
> *"⚡ Storm likely in your delivery zone tomorrow 6–9pm. Probability: 78%. Your ₹500 coverage is active."*

**Admin-facing UX:** City-wide heatmap showing predicted disruption risk for the next 48 hours, enabling the insurer partner to pre-position liquidity for expected payouts.

This model transforms GigShield from **reactive insurance** into **proactive financial protection** — a meaningful product innovation.

---

## Zero-Touch Claim Flow

```
Worker subscribes to ₹55 Standard weekly plan on GigShield mobile app
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
│  ✅ Fraud score: 12/100 (clean)          │
│  ✅ No duplicate claim today?            │
└──────────────────────────────────────────┘
           │
           ▼
   Claim auto-approved in < 30 seconds
           │
           ▼
   Insurer partner releases ₹100/hour payout
   (Standard plan — disruption duration: 5 hours = ₹500 max)
           │
           ▼
   Razorpay sandbox triggers transfer
           │
           ▼
   Firebase push notification sent:
   "🌧️ Heavy rain in your zone. ₹500 credited. Stay safe."
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
           │OpenWeatherMap│  │  CPCB AQI    │  │  IMD Disaster    │
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

- **Plan Status Badge** — Active (🟢) / Expired (🔴) / Disruption in Progress (⚡)
- **Current Plan Card** — Plan name, weekly premium, hourly rate, hours remaining this week
- **This Week's Disruptions** — Events detected in your delivery zone
- **Payouts Received** — Timeline of all credited amounts with disruption type
- **Predictive Alert Panel** — "Heavy rain likely tomorrow 6–9pm in your zone"
- **Earnings Protected Counter** — "You've saved ₹1,600 this month with GigShield"
- **Upgrade Plan** — One-tap upgrade to higher tier before next week
- **Renew Plan** — One-tap weekly renewal before plan expires

### Admin / Insurer Web Dashboard

- **City Zone Risk Heatmap** — Live + 48-hour predictive disruption risk by zone
- **Active Policies by Plan** — Breakdown across all 5 plan tiers
- **Premium Collected This Week** — Total across all plans
- **Claims Today** — Auto-approved / In review / Auto-rejected with hourly breakdown
- **Loss Ratio by Zone** — Real-time financial health of the portfolio
- **Fraud Review Queue** — Claims in the 30–70 score band with evidence summary
- **ML Model Health** — Confidence scores, feature drift indicators
- **Predicted Payout Exposure** — Expected payouts for next 48 hours based on disruption forecast

---

## Coverage Scope & Exclusions

### What GigShield Covers

GigShield covers **income lost by food delivery workers during verified external disruptions** that prevent delivery activity. Coverage is parametric — payouts are triggered by objective data thresholds, not manual claim assessment. Payouts are calculated on a per-hour basis up to the plan's weekly maximum.

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
- [x] Insurance model design (5 plan tiers, hourly payout model, loss ratio)
- [x] ML model architecture planning (Zone Risk, Fraud, Predictive)
- [x] Tech stack selection and platform strategy
- [x] System architecture design
- [x] GitHub repository setup with full README
- [x] Financial & business model — partner insurer structure defined
- [ ] Minimal prototype: Worker onboarding screen + plan selection UI
- [ ] Strategy video (2 minutes)

### Phase 2 — Automation & Protection (Weeks 3–4 | March 21–April 4)
*Theme: Protect Your Worker*

- [ ] Worker registration and KYC flow (simulated Aadhaar verification)
- [ ] Insurance policy management (create, view, renew, upgrade weekly plan)
- [ ] Zone Risk Classifier model deployed — plan recommendation at onboarding
- [ ] Weather + AQI API integration and disruption detection engine
- [ ] Hourly payout calculation engine
- [ ] Claims management system (auto-trigger + fraud check pipeline)
- [ ] Razorpay sandbox payout integration
- [ ] Firebase push notification setup
- [ ] 2-minute demo video

### Phase 3 — Scale & Optimise (Weeks 5–6 | April 5–17)
*Theme: Perfect for Your Worker*

- [ ] Advanced fraud detection (Isolation Forest model trained and deployed)
- [ ] Predictive disruption alert engine (XGBoost model, 48-hour forecast)
- [ ] Intelligent admin dashboard (heatmap, loss ratio, fraud queue, predictive map)
- [ ] Worker dashboard — all 5 plan cards, earnings protected counter, upgrade flow
- [ ] Full system integration testing
- [ ] 5-minute demo video (simulated rainstorm → auto-claim → hourly payout walkthrough)
- [ ] Final pitch deck (PDF)

---

## Strategy Video

🎥 *2-minute strategy video link will be added here upon submission.*

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
