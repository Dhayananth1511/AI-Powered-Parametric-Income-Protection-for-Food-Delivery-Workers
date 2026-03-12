# GigShield 🛡️
### AI-Powered Parametric Income Protection for Food Delivery Workers

> *"A delivery worker is stuck during a Chennai thunderstorm. They didn't file a claim. They didn't call anyone. Their phone just buzzed — ₹400 credited. GigShield works so they don't have to."*

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
12. [45-Day Development Roadmap](#45-day-development-roadmap)
13. [Strategy Video](#strategy-video)

---

## Problem Statement

India's food delivery ecosystem runs on the backs of hundreds of thousands of gig workers delivering for platforms like **Zomato** and **Swiggy**. These workers are entirely dependent on daily deliveries for their income — there is no salary, no paid leave, and no safety net.

External disruptions — heavy monsoon rain, extreme heat, cyclone alerts, air quality emergencies, government-declared curfews — can bring delivery activity to a complete halt. When that happens, a delivery worker loses **₹300–₹500 in a single evening**, with no recourse and no compensation.

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
| Peak Vulnerability | Evening hours (7–10pm) — Chennai's heaviest rainfall window |
| Financial Buffer | None. One disrupted week = missed EMI or skipped meals. |

> Note: This persona is representative of the thousands of food delivery partners GigShield is designed to protect. GigShield serves all Zomato and Swiggy delivery workers regardless of city or background.

### Disruption Scenario

It's a Tuesday evening in August. A delivery partner is midway through their shift in Velachery. Rainfall crosses 40mm in 2 hours. Restaurants begin closing. The Swiggy app goes quiet. They pull over under a shelter.

In the old world: ₹400 lost with no way to recover it.

With GigShield: Phone buzzes. *"🌧️ Heavy rain detected in your zone. ₹400 credited to your account. Stay safe."* They didn't do anything. GigShield did.

---

## Parametric Triggers

> **Design Principle:** Every trigger must be an objective, externally verifiable event from a government or accredited third-party source. GigShield does not use platform demand data, traffic metrics, or any subjective signal.

### Trigger Table

| # | Disruption Event | Data Source | Threshold | Payout |
|---|---|---|---|---|
| 1 | Heavy Rainfall | OpenWeatherMap API + IMD | Rainfall > 35mm within 3 hours in worker's pincode | Full disruption day payout |
| 2 | Extreme Heat | IMD API | Sustained temperature > 43°C for 2+ hours | Full payout (health advisory conditions) |
| 3 | Severe Air Pollution | CPCB AQI API (free public API) | AQI > 300 (Hazardous category) | Full payout |
| 4 | Cyclone / Flood Alert | IMD Disaster Alert Feed | Orange or Red alert issued for worker's district | Full payout + coverage auto-extended 24 hours |
| 5 | Government Curfew / Hartal | Verified news API + admin-confirmed flag | Section 144 order or state-declared shutdown in worker's zone | Full payout |

### Why These Triggers Are Compliant

Each trigger above satisfies all three compliance requirements:

1. **Externally verifiable** — sourced from IMD, CPCB, or a government-issued order. Not derived from platform data.
2. **Parametric** — defined by a measurable threshold that is either crossed or not. No subjective assessment.
3. **Causally linked to income loss** — each event directly prevents outdoor delivery work, causing lost wages.

---

## Weekly Premium Model

### The Actuarial Basis

GigShield's premium model is grounded in 10 years of IMD historical weather data for Chennai urban delivery zones.

**Base assumptions (Chennai):**
- Average disruption days per month during monsoon season (June–November): ~4 days
- Average disruption days per month during off-season: ~1 day
- Annual average disruption days: ~30 days/year (~2.5 per month)
- Average income loss per disruption day: ₹400

**Expected annual payout per worker:** 30 days × ₹400 = **₹12,000/year**

**Weekly expected payout:** ₹12,000 ÷ 52 = **~₹231/week**

### Premium Tiers (ML-Assigned at Onboarding)

| Zone Tier | Weekly Premium | Payout per Disruption Day | Max Claims per Week | Target Loss Ratio |
|---|---|---|---|---|
| 🟢 Green — Low Risk (inland, historically < 1 disruption/month) | ₹18/week | ₹350 | 2 days | 65% |
| 🟡 Yellow — Medium Risk (urban core, 2–3 disruptions/month avg) | ₹25/week | ₹400 | 3 days | 68% |
| 🔴 Red — High Risk (coastal / flood-prone, 4+ disruptions/month) | ₹35/week | ₹500 | 3 days | 70% |

**Target loss ratio: 65–70%**, consistent with sustainable micro-insurance operations globally. Premium tiers are assigned by our Zone Risk Classifier ML model at the point of worker onboarding, based on the worker's declared primary delivery zone.

### Why Weekly Pricing

Gig workers on Zomato/Swiggy operate on a weekly earnings and payout cycle. Daily premiums create friction. Monthly premiums are too large a commitment for workers with variable income. Weekly pricing — small enough to feel negligible (less than one order's earnings), meaningful enough to provide real coverage — matches how delivery workers actually think about money.

---

## AI/ML Architecture

GigShield integrates three purpose-built ML models. Each is described below with its algorithm, features, training data, and output.

---

### Model 1 — Zone Risk Classifier

**Purpose:** Assign each delivery zone a risk tier (Green / Yellow / Red) to determine the worker's weekly premium at onboarding.

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
| Historical disruption days/month (12-month rolling) | Frequency of past disruption events in that zone |
| Proximity to water bodies | Distance to nearest river, lake, or coastline (flood proxy) |
| Zone elevation | Low elevation = poor drainage = higher flood risk |
| Month of year | Monsoon seasonality weighting |
| Historical AQI exceedance days | Pollution risk profile for the zone |

**Output:** Risk score 0.0–1.0 → mapped to Green (< 0.35) / Yellow (0.35–0.65) / Red (> 0.65) → weekly premium assigned

**Why Random Forest:** Handles mixed numerical and categorical features well, produces interpretable feature importance scores, and does not require large datasets to perform reliably.

---

### Model 2 — Fraud Detection Engine

**Purpose:** Score every auto-triggered claim for fraud before payout is released.

**Algorithm:** Isolation Forest (behavioral anomaly detection) + deterministic rule layer (hard rejects)

#### Hard Reject Rules (Deterministic — Applied First)

| Rule | Logic |
|---|---|
| No verified trigger event | If no IMD/CPCB threshold breach recorded in worker's pincode on claim day → automatic rejection |
| GPS pincode mismatch | If worker's GPS location at trigger time does not overlap with disruption event pincode → automatic rejection |
| Claim cap exceeded | If worker has already reached max claims for the week → automatic rejection |

#### Anomaly Scoring (Isolation Forest — Applied After Hard Rules Pass)

| Feature | Fraud Signal |
|---|---|
| GPS velocity during claimed disruption window | High speed during disruption = actively working, not disrupted |
| Claim frequency (last 4 weeks) | 4 consecutive weekly claims with no variation = anomalous |
| Claim timing relative to trigger | Claim filed before trigger threshold crossed = suspicious |
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
> *"⚡ Storm likely in your delivery zone tomorrow 6–9pm. Probability: 78%. Your ₹400 coverage is active."*

**Admin-facing UX:** City-wide heatmap showing predicted disruption risk for the next 48 hours, enabling the insurer to pre-position liquidity for expected payouts.

This model transforms GigShield from **reactive insurance** into **proactive financial protection**.

---

## Zero-Touch Claim Flow

```
Worker purchases weekly plan on GigShield mobile app
           |
           v
GigShield backend polls OpenWeatherMap + IMD every 15 minutes
           |
           v
Rainfall crosses 35mm threshold in worker's pincode
           |
           v
+--------------------------------------+
|         Automated Verification       |
|  [✓] Worker GPS in affected zone?    |
|  [✓] First claim today? (not a dup)  |
|  [✓] Fraud score: clean              |
|  [✓] Weekly claim cap not reached?   |
+--------------------------------------+
           |
           v
   Claim auto-approved in < 30 seconds
           |
           v
   Razorpay sandbox triggers payout
           |
           v
   Firebase push notification sent:
   "🌧️ Heavy rain in your zone. ₹400 credited. Stay safe."
```

**Total time from disruption detection to payout: under 30 seconds. Zero human intervention. Zero forms.**

---

## Platform & Tech Stack

### Platform Strategy

GigShield is built on two platforms sharing a single backend:

| Platform | Target User | Purpose |
|---|---|---|
| **Mobile App (React Native)** | Delivery Workers | Onboarding, plan purchase, disruption alerts, payout tracking |
| **Web App (React.js)** | Insurer / Admin | Zone heatmap, policy portfolio, fraud queue, loss ratio analytics, predictive disruption map |

A shared **FastAPI backend** serves both platforms through a unified REST API.

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
+---------------------+        +---------------------+
|   Worker Mobile App  |        |   Admin Web App      |
|   (React Native)     |        |   (React.js)         |
+--------+------------+        +----------+----------+
         |                                |
         +--------------+-----------------+
                        |
                        v
            +-----------------------+
            |   FastAPI Backend     |
            |   (Python)            |
            +----------+------------+
                       |
          +------------+------------+
          v            v            v
   +----------+  +----------+  +--------------+
   |PostgreSQL|  | ML Engine|  |Disruption    |
   |(Workers, |  |(Risk,    |  |Monitor       |
   |Policies, |  |Fraud,    |  |(Polls APIs   |
   |Claims)   |  |Predict)  |  |every 15 min) |
   +----------+  +----------+  +------+-------+
                                       |
                    +------------------+------------------+
                    v                  v                   v
           +--------------+  +--------------+  +------------------+
           |OpenWeatherMap|  |  CPCB AQI    |  |  IMD Disaster    |
           |+ IMD Weather |  |  API         |  |  Alert Feed      |
           +--------------+  +--------------+  +------------------+
                                       |
                                       v
                            +---------------------+
                            |  Claim Trigger &     |
                            |  Fraud Check Engine  |
                            +----------+----------+
                                       |
                                       v
                            +---------------------+
                            |  Razorpay Sandbox    |
                            |  (Payout Processing) |
                            +----------+----------+
                                       |
                                       v
                            +---------------------+
                            |  Firebase FCM        |
                            |  (Worker Alert)      |
                            +---------------------+
```

---

## Dashboards

### Worker Mobile Dashboard

- **Coverage Status Badge** — Active (🟢) / Expired (🔴) / Disruption in Progress (⚡)
- **This Week's Disruptions** — Events detected in your delivery zone
- **Payouts Received** — Timeline of all credited amounts
- **Predictive Alert Panel** — "Heavy rain likely tomorrow 6–9pm in your zone"
- **Earnings Protected Counter** — "You've saved ₹1,600 this month with GigShield"
- **Renew Plan** — One-tap weekly renewal before plan expires

### Admin / Insurer Web Dashboard

- **City Zone Risk Heatmap** — Live + 48-hour predictive disruption risk by zone
- **Active Policies** — Count, premium collected, zone breakdown
- **Claims Today** — Auto-approved / In review / Auto-rejected
- **Loss Ratio by Zone** — Real-time financial health of the portfolio
- **Fraud Review Queue** — Claims in the 30–70 score band with evidence summary
- **ML Model Health** — Confidence scores, feature drift indicators
- **Predicted Payout Exposure** — Expected payouts for next 48 hours based on disruption forecast

---

## Coverage Scope & Exclusions

### What GigShield Covers

GigShield covers **income lost by food delivery workers during verified external disruptions** that prevent delivery activity. Coverage is parametric — payouts are triggered by objective data thresholds, not manual claim assessment.

### What GigShield Explicitly Does NOT Cover

> GigShield strictly excludes coverage for: vehicle repairs, bike maintenance, fuel costs, medical expenses, accident compensation, health insurance, life insurance, platform-side demand fluctuations, traffic congestion, technical issues with the delivery app, and any event not independently verifiable through a government or accredited third-party data source.
>
> All coverage is limited exclusively to verified external environmental and government-declared civic disruptions that directly prevent outdoor delivery work and cause loss of income.

---

## 45-Day Development Roadmap

### Phase 1 — Ideation & Foundation (Weeks 1–2 | March 4–20)
*Theme: Ideate & Know Your Delivery Worker*

- [x] Problem research and gig worker persona analysis
- [x] Insurance model design (parametric triggers, premium tiers, loss ratio)
- [x] ML model architecture planning (Zone Risk, Fraud, Predictive)
- [x] Tech stack selection and platform strategy
- [x] System architecture design
- [x] GitHub repository setup with full README
- [ ] Minimal prototype: Worker onboarding screen + weekly plan selection UI
- [ ] Strategy video (2 minutes)

### Phase 2 — Automation & Protection (Weeks 3–4 | March 21–April 4)
*Theme: Protect Your Worker*

- [ ] Worker registration and KYC flow (simulated Aadhaar verification)
- [ ] Insurance policy management (create, view, renew weekly plan)
- [ ] Dynamic premium calculation (Zone Risk Classifier model deployed)
- [ ] Weather + AQI API integration and disruption detection engine
- [ ] Claims management system (auto-trigger + fraud check pipeline)
- [ ] Razorpay sandbox payout integration
- [ ] Firebase push notification setup
- [ ] 2-minute demo video

### Phase 3 — Scale & Optimise (Weeks 5–6 | April 5–17)
*Theme: Perfect for Your Worker*

- [ ] Advanced fraud detection (Isolation Forest model trained and deployed)
- [ ] Predictive disruption alert engine (XGBoost model, 48-hour forecast)
- [ ] Intelligent admin dashboard (heatmap, loss ratio, fraud queue, predictive map)
- [ ] Worker dashboard — earnings protected counter + predictive alert panel
- [ ] Full system integration testing
- [ ] 5-minute demo video (simulated rainstorm → auto-claim → payout walkthrough)
- [ ] Final pitch deck (PDF)

---

## Strategy Video

🎥 *2-minute strategy video link will be added here upon submission.*

---

## About This Project

Built for the **Guidewire DEVTrails 2026 Pan-India University Hackathon**.

**Problem Statement:** AI-Powered Insurance for India's Gig Economy

**Team Persona Focus:** Food Delivery Workers (Zomato / Swiggy)

**Platform:** Web (Admin) + Mobile (Workers)

**Repository:** This repository will be used across all three phases of the hackathon. Commit history will reflect iterative development through each phase.

---

*Build fast. Spend smart. Protect every delivery worker. 🛡️*
