# Navi Mumbai House Price Predictor
### Product Requirements Document (PRD) — v1.0 | Status: Draft | Owner: Product Team | Market: Navi Mumbai

---

## 1. Product Overview

The Navi Mumbai House Price Predictor is a web and mobile application that leverages machine learning to provide accurate, real-time property valuations across Navi Mumbai's diverse micro-markets — including Kharghar, Vashi, Panvel, Nerul, Belapur, Airoli, and Ulwe. The platform empowers homebuyers, sellers, investors, and real estate agents with data-driven pricing intelligence.

---

## 2. Problem Statement

Navi Mumbai's real estate market is fragmented and opaque. Buyers overpay due to lack of pricing benchmarks, sellers underprice or hold unrealistic expectations, and agents rely on anecdotal data. Key pain points include:

- No reliable, locality-specific price benchmark for buyers and sellers
- High variability in per sq. ft. pricing across nodes (e.g., Kharghar vs. Ulwe vs. Vashi)
- Manual price discovery is slow, error-prone, and dependent on broker networks
- Investors lack tools to identify undervalued micro-markets or forecast appreciation trends

---

## 3. Goals & Success Metrics

| Goal | Success Metric |
|------|---------------|
| Prediction Accuracy | Mean Absolute Error (MAE) < 8% of actual market price |
| User Adoption | 5,000 MAU within 6 months of launch |
| Locality Coverage | All 14 major Navi Mumbai nodes covered at launch |
| Engagement | Average session duration > 3 minutes |
| Data Freshness | Property price data updated within 30 days |

---

## 4. Target Users

### 4.1 Primary Users
- **Homebuyers** — first-time or upgraders evaluating properties in Navi Mumbai
- **Property Sellers** — individuals wanting a fair price benchmark before listing
- **Real Estate Investors** — tracking micro-market trends and ROI potential

### 4.2 Secondary Users
- **Real Estate Agents & Brokers** — using predictions to justify pricing with clients
- **Housing Finance Companies** — loan underwriting and collateral valuation

---

## 5. Feature Requirements

| ID | Feature | Description | Priority | Effort |
|----|---------|-------------|----------|--------|
| F-01 | Price Prediction Engine | ML model (XGBoost/Random Forest) trained on historical transaction data to predict price per sq. ft. and total valuation | High | XL |
| F-02 | Property Input Form | User inputs: locality, BHK type, area (sq. ft.), floor, age, amenities, parking | High | M |
| F-03 | Locality Heatmap | Interactive map showing average price bands across Navi Mumbai nodes | High | L |
| F-04 | Comparable Listings | Show 5–10 recent sales/listings near the predicted property for context | High | L |
| F-05 | Price Trend Charts | 6-month and 12-month price trend per locality | Medium | M |
| F-06 | Appreciation Forecast | 3-year price appreciation forecast based on infrastructure pipeline (e.g., metro, NAINA) | Medium | XL |
| F-07 | Save & Compare | Save multiple property estimates and compare side-by-side | Medium | S |
| F-08 | Agent Connect | Lead generation — connect user with a verified agent for that locality | Low | M |
| F-09 | Valuation Report PDF | Downloadable one-page valuation report with prediction, comps, and trend | Medium | M |
| F-10 | EMI Calculator | Integrated EMI calculator linked to the predicted price | Low | S |

---

## 6. Machine Learning Model Specification

### 6.1 Input Features

| Feature Category | Variables |
|-----------------|-----------|
| Location | Node/locality, sector, proximity to station (km), proximity to highway |
| Property Attributes | BHK configuration, carpet area (sq. ft.), floor number, total floors, age of building |
| Amenities | Lift, parking, gym, swimming pool, gated society, CCTV |
| Market Signals | Recent avg. price/sq. ft. in locality (30-day), transaction volume |
| Infrastructure | Metro station distance, upcoming NAINA projects, IT park proximity |

### 6.2 Model Architecture

- **Primary Model:** Gradient Boosted Trees (XGBoost) trained on RERA-registered transaction data
- **Fallback Model:** Linear regression with locality-level price adjustments for sparse data areas
- **Retraining Cadence:** Monthly, triggered when new RERA data is available
- **Validation:** 80/20 train-test split with cross-validation across locality segments

---

## 7. Data Sources

- **MahaRERA Transaction Registry** — registered sale deeds and price disclosures
- **CIDCO & NMC Property Records** — approved layout and usage data
- **99acres / MagicBricks Listings API** — active listing prices for comps
- **OpenStreetMap** — distance calculations for transit and amenity proximity
- **MMRDA & MSRDC** — metro corridor and infrastructure pipeline data

---

## 8. Technical Architecture

| Layer | Technology / Component |
|-------|----------------------|
| Frontend | React.js (Web), React Native (Mobile), Mapbox GL for heatmaps |
| Backend API | FastAPI (Python), REST endpoints, JWT authentication |
| ML Pipeline | Scikit-learn, XGBoost, MLflow for experiment tracking |
| Data Storage | PostgreSQL (structured data), Redis (caching), S3 (model artifacts) |
| Data Ingestion | Apache Airflow for ETL pipelines from RERA and listing sources |
| Hosting | AWS (EC2 + RDS + S3), auto-scaled behind an ALB |
| Monitoring | Grafana dashboards for model drift, API latency, and error rates |

---

## 9. Non-Functional Requirements

### 9.1 Performance
- Prediction API response time: < 2 seconds (p95)
- Heatmap tile load time: < 1.5 seconds
- System uptime: 99.5% SLA

### 9.2 Security & Compliance
- All user data encrypted at rest (AES-256) and in transit (TLS 1.3)
- No PII stored beyond email and phone (optional, for agent connect)
- RERA data usage compliant with Maharashtra government data policies

### 9.3 Accessibility
- WCAG 2.1 Level AA compliance for web interface
- Multilingual support: English and Marathi at launch

---

## 10. Roadmap & Milestones

| Phase | Timeline | Deliverables |
|-------|----------|-------------|
| Phase 1 | Months 1–2 (Foundation) | Data pipeline, RERA ingestion, baseline ML model (F-01), property input form (F-02) |
| Phase 2 | Months 3–4 (Core Product) | Locality heatmap (F-03), comparable listings (F-04), price trend charts (F-05), web app launch |
| Phase 3 | Months 5–6 (Enrichment) | Appreciation forecast (F-06), save & compare (F-07), valuation PDF (F-09), mobile app launch |
| Phase 4 | Month 7+ (Monetisation) | Agent connect lead gen (F-08), EMI calculator (F-10), API licensing to banks/HFCs |

---

## 11. Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Limited RERA data for newer nodes (Ulwe, Dronagiri) | Medium | Supplement with listing data; use fallback linear model; show confidence intervals |
| Market dislocation (policy changes, interest rate spikes) | High | Monthly model retraining; prominent disclaimer on predictions; human-in-loop review for extreme outliers |
| 3rd-party listing API rate limits or pricing changes | Medium | Build internal web scraper as fallback; cache listing data for 72 hours |

---

## 12. Open Questions

- Should the platform support pan-MMR (Mumbai, Thane) expansion in Phase 4, or remain Navi Mumbai-focused?
- Will the valuation report be free or part of a paid tier? What is the monetisation model?
- Do we pursue a B2B API licensing model with banks/HFCs from day one, or post-traction?
- How do we handle user-submitted corrections to predictions — feedback loop into retraining?

---

*Navi Mumbai House Price Predictor — PRD v1.0 · Confidential · For Internal Use Only*
