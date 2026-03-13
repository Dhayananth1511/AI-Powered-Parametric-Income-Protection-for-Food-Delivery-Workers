# GigShield 🛡️
### AI-Powered Parametric Income Protection for Food Delivery Workers
**Team ZenVyte | Guidewire DEVTrails 2026**

> *"A delivery worker is stuck during a Chennai thunderstorm. They didn't file a claim. They didn't call anyone. Their phone just buzzed — ₹160 credited. GigShield works so they don't have to."*

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
13. [Development Roadmap](#development-roadmap)

---

## Problem Statement

India's food delivery workers (Zomato, Swiggy) are entirely dependent on daily deliveries for income — no salary, no paid leave, no safety net. External disruptions such as heavy monsoon rain, extreme heat, cyclone alerts, severe air pollution, and government-declared curfews can bring delivery activity to a complete halt.

| Metric | Value |
|---|---|
| Gig workers in India with zero income protection | 5 crore+ |
| Income lost per disruption event per worker | ₹300–₹650 |
| Traditional insurance products covering short-term gig income loss | 0 |
| Time to process a manual insurance claim today | Weeks |

Traditional insurance does not cover short-term income disruption for gig workers. Filing a manual claim is too complex, too slow, and too uncertain for someone who needs money today.

---

## Our Solution

GigShield is an **AI-powered parametric micro-insurance platform** built exclusively for food delivery partners on Zomato and Swiggy. It continuously monitors verified external data sources, automatically detects disruption threshold breaches, verifies GPS location and fraud score in real time, and triggers an instant income top-up — in under 30 seconds, with no human intervention.

**Key differentiators:**
- Every trigger is independently verifiable through government or third-party APIs — no platform data, no subjective metrics
- ML-driven dynamic zone-based pricing makes the model financially sustainable
- Predictive disruption alerts warn workers 24–48 hours before an event
- Zero-touch claim experience — no forms, no uploads, no waiting
- All policies underwritten by a licensed IRDAI insurer partner — GigShield carries zero claims liability
- Actuarially grounded pricing maintaining 50–72% loss ratio across all plans

---

## Delivery Worker Persona

**Illustrative Persona — Swiggy Delivery Partner, Chennai**

| Attribute | Detail |
|---|---|
| City | Chennai (Velachery, Adyar, T. Nagar zones) |
| Daily Hours | 9am – 9pm |
| Daily Deliveries | 20–28 |
| Daily Earnings | ₹900 – ₹1,300 |
| Weekly Earnings | ₹6,500 – ₹9,000 |
| Hourly Earnings | ₹112 – ₹162/hour |
| Peak Vulnerability | Evening hours (7–10pm) — Chennai's heaviest rainfall window |
| Financial Buffer | None. One disrupted week = missed EMI or skipped meals. |

**Disruption Scenario:**
It's a Tuesday evening in August. A delivery partner is midway through their shift in Velachery. Rainfall crosses 40mm in 2 hours. Restaurants begin closing. The Swiggy app goes quiet.

- **Without GigShield:** ₹500 lost with no way to recover it.
- **With GigShield:** *"🌧️ Heavy rain detected in your zone. ₹160 credited to your account. Stay safe."* — no action required.

---

## Parametric Triggers

> Every trigger is an objective, externally verifiable event from a government or accredited third-party source. GigShield does not use platform demand data, traffic metrics, or any subjective signal.

| # | Disruption Event | Data Source | Threshold | Payout Trigger |
|---|---|---|---|---|
| 1 | Heavy Rainfall | OpenWeatherMap + IMD | Rainfall > 35mm within 3 hours in worker's pincode | Per disruption hour (up to plan cap) |
| 2 | Extreme Heat | IMD API | Sustained temperature > 43°C for 2+ hours | Per disruption hour (up to plan cap) |
| 3 | Severe Air Pollution | CPCB AQI API | AQI > 300 (Hazardous category) | Per disruption hour (up to plan cap) |
| 4 | Cyclone / Flood Alert | IMD Disaster Alert + NDMA | Orange or Red alert issued for worker's district | Full weekly plan cap triggered immediately |
| 5 | Government Curfew / Hartal | NDMA alert feed + admin-confirmed flag | Section 144 or state-declared shutdown in worker's zone | Full weekly plan cap triggered immediately |

**Trigger 5 fallback:** If the NDMA feed is delayed, an admin-verified flag in the GigShield dashboard can manually activate Trigger 5 for an affected zone. All new workers are soft-reviewed for their first 2 claims before this trigger is auto-approved.

Each trigger satisfies three compliance requirements: externally verifiable, parametric (threshold-based, binary), and causally linked to income loss.

---

## Weekly Premium Model

### Actuarial Foundation

Base assumptions — Chennai food delivery zones (IMD 10-year historical data):

| Parameter | Value | Basis |
|---|---|---|
| Disruption events/month — monsoon season (Jun–Nov) | 3.0 events | IMD Chennai 10-yr average |
| Disruption events/month — off-season (Dec–May) | 0.5 events | IMD Chennai historical |
| Annual disruption events per worker | 21 events/year | (3.0 × 6) + (0.5 × 6) |
| Average disruption duration | 2.5 hours | IMD urban rainfall event data |
| Annual disruption hours per worker | 52.5 hours/year | 21 × 2.5 |
| Worker's average hourly income | ₹112/hour | ₹900/day ÷ 8 working hours |
| Annual income lost per worker | ₹5,880/year | 52.5 hrs × ₹112 |
| Weekly income lost (annualised average) | ₹113/week | ₹5,880 ÷ 52 weeks |

GigShield is a **partial income top-up**, not full income replacement. Full replacement at these premium levels would produce loss ratios exceeding 300%, making the product uninsurable. The tiered top-up model maintains loss ratios of 50–72% — within standard parametric underwriting thresholds.

### The 5 Plans

| Plan | Weekly Premium | Hourly Payout | Max Hours/Week | Max Weekly Payout | Target User |
|---|---|---|---|---|---|
| 🌱 Starter | ₹35/week | ₹25/hour | 2 hours | ₹50 | New workers, low-risk zones |
| 🔵 Basic | ₹55/week | ₹30/hour | 3 hours | ₹90 | Part-time workers |
| 🟡 Standard | ₹79/week | ₹40/hour | 4 hours | ₹160 | Full-time urban workers |
| 🟠 Premium | ₹109/week | ₹50/hour | 4 hours | ₹200 | High-earning full-time partners |
| 🔴 Elite | ₹149/week | ₹60/hour | 5 hours | ₹300 | Coastal / flood-prone zones |

### Loss Ratio Proof

| Plan | Annual Premium | Expected Annual Claim | Loss Ratio | Heavy Monsoon (+40% events) |
|---|---|---|---|---|
| 🌱 Starter | ₹1,820 | ₹1,312 | 72% ✅ | ~85% ✅ |
| 🔵 Basic | ₹2,860 | ₹1,575 | 55% ✅ | ~77% ✅ |
| 🟡 Standard | ₹4,108 | ₹2,100 | 51% ✅ | ~72% ✅ |
| 🟠 Premium | ₹5,668 | ₹2,625 | 46% ✅ | ~65% ✅ |
| 🔴 Elite | ₹7,748 | ₹4,134 | 53% ✅ | ~75% ✅ |

Elite plan uses a 1.4× disruption frequency multiplier for coastal/flood-prone zones. All plans remain within insurer-acceptable loss ratios even under worst-case monsoon years.

### Affordability Check

| Plan | Weekly Premium | % of Weekly Earnings (₹7,000 avg) | Deliveries to cover |
|---|---|---|---|
| 🌱 Starter | ₹35 | 0.5% | ~1 delivery |
| 🔵 Basic | ₹55 | 0.8% | ~1.5 deliveries |
| 🟡 Standard | ₹79 | 1.1% | ~2 deliveries |
| 🟠 Premium | ₹109 | 1.6% | ~3 deliveries |
| 🔴 Elite | ₹149 | 2.1% | ~4 deliveries |

All plans stay under 2.5% of weekly earnings — the micro-insurance affordability threshold in India.

---

## AI/ML Architecture

### Model 1 — Zone Risk Classifier

**Purpose:** Recommend the correct plan tier to each worker at onboarding based on their delivery zone's historical disruption risk.

**Algorithm:** Random Forest Classifier

**Training Data:** IMD historical rainfall records (10 years, district-level), CPCB AQI historical data, NDMA flood zone maps, IMD cyclone track data.

**Input Features:**

| Feature | Description |
|---|---|
| Zone latitude / longitude | Geographic position of delivery zone centroid |
| Historical disruption events/month | Frequency of past disruption events (12-month rolling) |
| Proximity to water bodies | Distance to nearest river, lake, or coastline |
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

---

### Model 2 — Fraud Detection Engine

**Purpose:** Score every auto-triggered claim before payout is released.

**Algorithm:** Isolation Forest (behavioral anomaly detection) + deterministic hard-reject rule layer

**Cold-start strategy:** For workers with fewer than 2 approved claims, only hard-reject rules apply. Isolation Forest scoring activates after sufficient behavioral history is established. All new accounts are soft-reviewed for their first 2 claims.

#### Hard Reject Rules (Applied First)

| Rule | Logic |
|---|---|
| No verified trigger event | No IMD/CPCB threshold breach in worker's pincode on claim day → auto-reject |
| GPS pincode mismatch | Worker GPS at trigger time does not overlap disruption zone → auto-reject |
| Claim cap exceeded | Worker has already reached max hours for the week → auto-reject |
| Plan not active | Worker's weekly plan has expired → auto-reject |

#### Anomaly Scoring (Applied After Hard Rules Pass)

| Feature | Fraud Signal |
|---|---|
| GPS velocity during disruption window | Speed > 5 km/h = actively working, not disrupted |
| Claim frequency (last 4 weeks) | 4 consecutive weekly claims with no variation = anomalous |
| Claim timing relative to trigger | Claim initiated before threshold crossed = suspicious |
| Device fingerprint | Multiple accounts on same device = duplicate registration |
| Historical claim approval rate | Consistent 100% approval rate over months = flag for review |

**Fraud Score → Action:**

| Score | Action |
|---|---|
| 0 – 30 | Auto-approve. Payout released immediately. |
| 30 – 70 | Human review queue (admin dashboard). |
| > 70 | Auto-reject. Worker notified with appeal option. |

---

### Model 3 — Predictive Disruption Alert Engine

**Purpose:** Forecast disruption probability 24–48 hours ahead per delivery zone for proactive worker notifications and insurer liquidity preparation.

**Algorithm:** XGBoost on time-series weather features

**Input Features:** 7-day rolling weather trend, current IMD forecast, season flag (monsoon/pre-monsoon/winter), zone historical disruption frequency by month, recent AQI trend.

**Output:** Disruption probability score (0–100%) per zone per day.

Worker notification example:
> *"⚡ Storm likely in your delivery zone tomorrow 6–9pm. Probability: 78%. Your ₹160 coverage is active."*

Admin view: city-wide heatmap showing predicted disruption risk for the next 48 hours, enabling the insurer partner to pre-position liquidity for expected payouts.

---

## Zero-Touch Claim Flow

```
Worker subscribes to ₹79 Standard weekly plan
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
```

**Total time from disruption detection to payout: under 30 seconds. Zero forms. Zero human intervention.**

---

## Platform & Tech Stack

GigShield runs on two platforms sharing a single backend:

| Platform | Target User | Purpose |
|---|---|---|
| Mobile App (React Native) | Delivery Workers | Onboarding, plan selection, disruption alerts, payout tracking |
| Web App (React.js) | Insurer / Admin | Zone heatmap, fraud queue, loss ratio analytics, predictive disruption map |

### Full Tech Stack

| Layer | Technology |
|---|---|
| Mobile Frontend | React Native |
| Web Frontend | React.js |
| Backend | Python FastAPI |
| Database | PostgreSQL |
| ML Models | Scikit-learn (Random Forest, Isolation Forest), XGBoost |
| Weather API | OpenWeatherMap (free tier) + IMD public data |
| AQI API | CPCB AQI API / OpenAQ |
| Disaster Alerts | NDMA public alert feed |
| Location | Google Maps API |
| Payments | Razorpay Sandbox |
| Push Notifications | Firebase Cloud Messaging |
| Hosting | Railway / Render (free tier) |

---

## System Architecture

```
┌─────────────────────┐        ┌─────────────────────┐
│   Worker Mobile App  │        │   Admin Web App      │
│   (React Native)     │        │   (React.js)         │
└────────┬────────────┘        └──────────┬──────────┘
         └──────────────┬─────────────────┘
                        ▼
            ┌───────────────────────┐
            │   FastAPI Backend     │
            └──────────┬────────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
   ┌──────────┐  ┌──────────┐  ┌──────────────┐
   │PostgreSQL│  │ ML Engine│  │Disruption    │
   │          │  │(Risk,    │  │Monitor       │
   │          │  │Fraud,    │  │(15-min poll) │
   │          │  │Predict)  │  │              │
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
                                       ▼
                            ┌─────────────────────┐
                            │  Razorpay Sandbox    │
                            └──────────┬──────────┘
                                       ▼
                            ┌─────────────────────┐
                            │  Firebase FCM        │
                            │  (Worker Alert)      │
                            └─────────────────────┘
```

---

## Dashboards

### Worker Mobile Dashboard
- Plan status badge — Active 🟢 / Expired 🔴 / Disruption in Progress ⚡
- Current plan card — plan name, weekly premium, hourly rate, hours remaining
- Disruptions this week — events detected in your delivery zone
- Payouts received — timeline of all credited amounts
- Predictive alert panel — "Heavy rain likely tomorrow 6–9pm (78% probability)"
- Earnings protected counter — "You've saved ₹640 this month with GigShield"
- One-tap plan renewal and upgrade

### Admin / Insurer Web Dashboard
- City zone risk heatmap — live + 48-hour predictive disruption risk by pincode
- Active policies by plan — counts and premium volume across all 5 tiers
- Claims today — auto-approved / in review / auto-rejected with hourly breakdown
- Loss ratio by zone — real-time portfolio loss ratio segmented by delivery zone
- Fraud review queue — claims in the 30–70 score band with GPS trace and timing evidence
- ML model health — confidence scores, feature drift indicators, retraining alerts
- Predicted payout exposure — expected payouts for next 48 hours based on disruption forecast

---

## Coverage Scope & Exclusions

### What GigShield Covers

Income lost by food delivery workers during verified external disruptions that prevent delivery activity. Coverage is parametric — triggered by objective data thresholds, calculated on a per-hour basis up to the plan's weekly maximum. GigShield provides a **partial income top-up**, not full income replacement.

### What GigShield Does NOT Cover

Vehicle repairs, bike maintenance, fuel costs, medical expenses, accident compensation, health insurance, life insurance, platform-side demand fluctuations, traffic congestion, app technical issues, or any event not independently verifiable through a government or accredited third-party data source.

---

## Financial & Business Model

### Platform Structure

GigShield operates as an insurance technology distribution platform, not as the underwriter. All policies are underwritten by a licensed IRDAI insurer partner (e.g., Digit Insurance / Acko).

```
Worker pays weekly premium
         ↓
Licensed IRDAI Insurer Partner
holds all premium capital and pays all claims
         ↓
GigShield earns 10% platform distribution fee per active policy
         ↓
GigShield claims liability: ₹0
```

### Revenue Per Policy Per Week

| Plan | Weekly Premium | GigShield Fee (10%) | Insurer Net Premium | Insurer Loss Ratio on Net |
|---|---|---|---|---|
| 🌱 Starter | ₹35 | ₹3.50 | ₹31.50 | ~72% ✅ |
| 🔵 Basic | ₹55 | ₹5.50 | ₹49.50 | ~55% ✅ |
| 🟡 Standard | ₹79 | ₹7.90 | ₹71.10 | ~51% ✅ |
| 🟠 Premium | ₹109 | ₹10.90 | ₹98.10 | ~46% ✅ |
| 🔴 Elite | ₹149 | ₹14.90 | ₹134.10 | ~53% ✅ |

### Revenue at Scale

| Active Workers | Avg Weekly Fee | Weekly Revenue | Annual Revenue |
|---|---|---|---|
| 1,000 | ₹8.20 | ₹8,200 | ₹42,64,000 |
| 10,000 | ₹8.20 | ₹82,000 | ₹4.26 Cr |
| 1,00,000 | ₹8.20 | ₹8,20,000 | ₹42.64 Cr |

---

## Development Roadmap

### Phase 1 — Ideation & Foundation (March 4–20)
- [x] Problem research and gig worker persona analysis
- [x] Insurance model — 5 plan tiers, hourly payout model, actuarial loss ratio proof
- [x] ML model architecture (Zone Risk Classifier, Fraud Detection, Predictive Alert)
- [x] Tech stack selection and system architecture design
- [x] GitHub repository with full README
- [x] Financial & business model — IRDAI partner insurer structure, 10% fee model
- [ ] Minimal prototype: worker onboarding + plan selection UI (React Native)
- [ ] Strategy video (2 minutes)

### Phase 2 — Automation & Protection (March 21–April 4)
- [ ] Worker registration and KYC flow (simulated Aadhaar verification)
- [ ] Insurance policy management (create, view, renew, upgrade weekly plan)
- [ ] Zone Risk Classifier — trained and deployed for plan recommendation at onboarding
- [ ] OpenWeatherMap + IMD + CPCB AQI API integration and disruption detection (15-min polling)
- [ ] Hourly payout calculation engine
- [ ] Claims pipeline: GPS verify → fraud check → approve → payout
- [ ] Razorpay sandbox payout integration
- [ ] Firebase push notification setup
- [ ] Demo video (2 minutes)

### Phase 3 — Scale & Optimise (April 5–17)
- [ ] Isolation Forest fraud model trained and deployed (GPS spoofing, fake weather detection)
- [ ] Predictive disruption alert engine — XGBoost, 48-hour zone-level forecast
- [ ] Intelligent admin dashboard (zone heatmap, loss ratio, fraud queue, payout exposure map)
- [ ] Worker dashboard — all 5 plan cards, earnings protected counter, alert panel, upgrade flow
- [ ] NDMA alert feed integration for Trigger 5 with admin fallback
- [ ] Full system integration testing across all 5 disruption triggers
- [ ] Demo video (5 minutes) — simulated rainstorm → auto-claim → payout walkthrough
- [ ] Final pitch deck (PDF)

---

## Prototype Disclaimer

This project is a prototype built for the **Guidewire DEVTrails 2026 Hackathon**. Insurance payouts are simulated using Razorpay Sandbox. Worker identity verification is mocked. External data sources use publicly available APIs (OpenWeatherMap, CPCB, IMD, NDMA). In a real deployment, GigShield would integrate with a licensed IRDAI insurance partner to underwrite policies and process real claim payouts.

---

## Team

**Team Name:** ZenVyte

| Name | Role |
|---|---|
| Dhayananth N | Team Lead |
| Mowlieswaran G | Member |
| Arun Kumar S | Member |
| Karthick V | Member |
| Hardik Muthusamy | Member |

**Problem Statement:** AI-Powered Insurance for India's Gig Economy  
**Persona Focus:** Food Delivery Workers (Zomato / Swiggy)  
**Platform:** Web (Admin) + Mobile (Workers)

---

*Build fast. Spend smart. Protect every delivery worker. 🛡️*  
*Team ZenVyte — DEVTrails 2026*
