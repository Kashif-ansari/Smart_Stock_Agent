# Smart Stock Agent — PRD and Development Roadmap Prompt

Copy the prompt below into your preferred AI assistant. It requests a complete PRD, technical architecture, and step-by-step implementation guide; it does not claim the application has already been built.

---

Act as a senior product manager, retail operations specialist, Python full-stack developer, machine learning engineer, LLM/RAG architect, and security engineer.

Create a detailed, implementation-ready **Product Requirements Document (PRD), technical architecture, and step-by-step development roadmap** for **Smart Stock Agent**.

Write in clear English for a six-member development team. Make concrete recommendations, explain important trade-offs, and label assumptions. Proceed with reasonable assumptions when information is missing, then list unresolved decisions. Produce the requested documents now; do not stop at an outline or questions. Do not generate an entire codebase at this stage.

Verify changing model names, package APIs, supported features, licenses, and deployment requirements against official documentation. Include source links and the verification date. If browsing is unavailable, identify recommendations requiring verification and do not claim they are current. Separate user requirements, verified facts, design choices, and proposed targets.

**1. Product purpose, scope, and success**

Smart Stock Agent helps general stores and retailers selling many product categories buy the right products, in the right quantities, at the right time, and sell them profitably. Here, “stock” means merchandise inventory.

Support business owners from store setup and initial assortment planning through daily sales, procurement, inventory, customer retention, staffing support, finance analysis, and expansion. Define achievable workflows and escalation paths instead of promising a solution to every business problem.

Specify personas, user journeys, pain points, business value, assumptions, dependencies, non-goals, and MVP/V1/V2 boundaries. Preserve all requested capabilities in the roadmap while prioritizing a working vertical slice: sign in → upload and validate sales → forecast → recommend replenishment → explain with evidence → export a report.

Define business KPIs such as stockout rate, excess inventory, expiry losses, inventory turnover, forecast error, gross margin, retention, and owner time saved. Explain measurement, baseline collection, and evaluation windows; label improvement targets as proposals, not achieved results.

For each requirement, provide an ID, user role, priority, input, expected behavior, output, permissions, dependency, failure behavior, and testable acceptance criteria. Include Given/When/Then examples for critical journeys.

**2. Technology stack and system architecture**

Use Python, Streamlit, Groq, FAISS, and CrewAI. Recommend a compatible, maintainable stack with minimal unnecessary frameworks:

- Streamlit for the multipage user interface.
- Groq-hosted LLM inference for language understanding, tool selection, and explanations. Select currently supported model IDs, tool/structured-output capabilities, and configurable fallbacks.
- CrewAI for specialized agents and controlled workflows; use deterministic Python services for calculations and routine processing.
- FAISS for dense vector search, a separate BM25 keyword index, and a cross-encoder reranker.
- PostgreSQL as the transactional source of truth, with SQLAlchemy and Alembic. If SQLite is offered for a local demo, explain its limits and migration path.
- Appropriate libraries for data validation, forecasting, customer analytics, parsing, OCR, charting, and report generation. State why each is needed.
- A durable background worker and scheduler for long-running ingestion, forecasting, research, and report tasks. Select a concrete implementation and explain retries, persisted status, cancellation, and duplicate prevention.

Decide whether the MVP needs FastAPI; describe a secure service boundary without adding infrastructure solely for appearance. Explain authenticated identity propagation if a separate API is used.

Provide component and data-flow diagrams covering UI, identity, application services, database, protected file storage, retrieval, forecasting, agent execution, external search, and exports. Explain local development and production deployment, CPU/GPU requirements, persistence, and scaling limits. Keep long jobs and repeated model loading outside Streamlit reruns.

**3. Business data upload and transformation**

Create a dedicated upload and data-quality page. Support CSV, XLSX, XLS, and TSV with suitable parsers; assess JSON, Parquet, and spreadsheet connectors as extensions. Distinguish structured sales imports from documents uploaded to the knowledge base. Do not promise automatic support for every file type.

Specify an end-to-end pipeline: authenticate → validate file → inspect sheets/encoding → preview → suggest column mappings → obtain user confirmation where ambiguous → validate → normalize → show rejected rows → save a versioned dataset → generate features.

Define a canonical schema. Minimum unit-sales forecasting fields are timestamp/date, product/SKU identifier, and quantity sold. Describe conditional fields including transaction ID, customer ID, store ID, price, discount, returns, cost, category, promotion, inventory availability, supplier, lead time, and expiry. Derive tenant identity from the authenticated session, never from an uploaded tenant column.

Handle duplicate imports, ambiguous date formats, currencies, units, time zones, missing values, returns, outliers, irregular dates, multiple sheets, and changing SKUs. Preserve raw data and transformation history. Do not silently remove meaningful sales spikes or invent unavailable columns.

Distinguish zero sales, missing records, store closures, and stockouts. Observed sales can understate demand when stock is unavailable. Explain reconciliation, data-quality scores, minimum history rules, and feature availability when required fields are absent.

Provide a sample upload template, column-mapping example, canonical data example, validation report, and feature-to-required-data matrix. PDF/image receipt extraction must include confidence checks and user review before entering sales records.

**4. Forecasting and prediction model selection**

Select a suitable Hugging Face time-series model through benchmarking on representative retail data. Evaluate `amazon/chronos-2` as an initial candidate, plus a lighter alternative where hardware requires it. Verify exact model IDs, licenses, inference interfaces, covariate support, and hosting requirements. Do not assume a Hugging Face listing implies a hosted inference endpoint.

Compare against seasonal naive, ARIMA/SARIMA/SARIMAX where appropriate, Prophet, and exponential smoothing/ETS/Holt-Winters. Include intermittent-demand methods such as Croston/SBA/TSB where justified, and assess a lag-feature tree model when covariates support it.

Explain each model's inputs, suitable demand patterns, minimum history, training or zero-shot usage, runtime, limitations, and fallback. Identify whether the selection is provisional or supported by measured results; do not declare a universal best model.

Support daily/weekly forecasts and configurable 7-, 14-, 30-, and 90-day horizons where data permits. Distinguish units, revenue, and price scenarios. Cover SKU/store/category aggregation, new products, sparse sales, holidays, promotions, known future covariates, and missing future inputs.

Use chronological rolling-origin backtesting, leakage-safe feature preparation, and an untouched final holdout. Specify MAE, WAPE or MASE with zero-denominator handling, forecast bias, prediction-interval coverage, and quantile loss when relevant. Explain uncertainty, nonnegative forecasts, aggregation consistency, per-segment model selection, drift monitoring, and retraining triggers.

The LLM must call verified forecasting and calculation tools. It must not invent numerical predictions or present generated language as model output.

**5. Inventory, procurement, and pricing decisions**

Specify EOQ, reorder point (ROP), safety stock, suggested reorder quantities, days of cover, low-stock alerts, overstock reduction, expiry management, supplier comparisons, and draft purchase orders.

Include correct formulas, units, assumptions, and worked examples. For EOQ, define demand, ordering cost, and holding cost in consistent periods and explain its steady-demand assumptions. Define ROP from lead-time demand plus safety stock. Explain inventory position using on-hand stock, on-order stock, commitments/backorders, and a consistent reservation policy that prevents double counting.

Use forecast error or an appropriate lead-time-demand distribution for safety stock. State assumptions for variable demand and lead times; avoid universal formulas applied without their conditions. Distinguish reorder triggers from order quantities.

Respect cash budgets, supplier minimums, pack sizes, storage capacity, expiry, seasonality, availability, and lead-time uncertainty. Show how a recommendation changes when constraints bind or required cost data is missing.

Specify dynamic pricing as a later, controlled capability using margin floors, price bounds, competitor evidence, inventory age, expiry, and measured demand response. Explain that historical correlations do not establish price elasticity. Start with reviewable rules and simulations; require owner approval for live price changes and purchases, with an audit trail and rollback where possible.

**6. Customer and sales intelligence**

Include RFM segmentation, K-Means, customer churn prediction, and market-basket analysis using Apriori or FP-Growth.

For each, give the business question, required data, preprocessing, outputs, evaluation approach, and recommended action. Define RFM windows, returns treatment, scaling, skew handling, cluster-count selection, stability, and business-readable segment labels.

For churn, define an operational inactivity outcome, observation window, prediction horizon, and leakage-safe labels. Compare a simple baseline with suitable supervised models and report precision/recall, PR-AUC, calibration, and intervention costs. Explain censoring and insufficient history.

Customer-level analysis requires stable customer identifiers and repeat-purchase history. Anonymous sales must not be described as individual churn data. Basket analysis requires transaction-level item groupings; report support, confidence, lift, and minimum evidence before proposing bundles. Disable unsupported features and explain what data is missing.

**7. Knowledge ingestion, embeddings, and hybrid RAG**

Build a business chatbot grounded in authorized store data, approved business documents, and verified external sources. Explain that RAG makes documents available at inference time; it does not train an LLM's weights. Describe optional fine-tuning only as a later, separately evaluated activity with suitable data rights, labels, and privacy controls.

Specify extraction from PDF, DOCX, TXT, Markdown, approved HTML/web pages, spreadsheets, and scanned documents/images through OCR. Preserve headings, reading order, tables, page numbers, sheet names, and row/cell references where available. State parser limits, table/OCR confidence, and repair or review behavior.

Define extraction → cleanup → deduplication → structure-aware chunking → metadata enrichment → embeddings → indexing. Propose initial token sizes/overlap as tunable settings; evaluate them rather than claiming one fixed size is optimal. Retain table headers and row context and support parent/child retrieval where useful.

Choose exact embedding and reranking model IDs after checking documentation, licenses, memory, latency, and retrieval quality. Assess English, Urdu, and Roman Urdu support if included in scope. Keep embedding versions, dimensions, normalization, and query/document conventions consistent.

Use this retrieval design: authorize request → choose permitted corpus → normalize query → BM25 keyword retrieval and FAISS semantic retrieval → reciprocal rank fusion or another justified fusion method → cross-encoder reranking → evidence selection → grounded generation → citation checks.

Keyword search must preserve exact SKUs, brands, invoice numbers, and product codes. FAISS is a similarity index; database records and metadata remain separately managed. Exact sales totals and inventory quantities must come from authorized database/calculation tools, not approximate retrieval over text chunks.

Persist indexes in protected folders such as `storage/vectorstores/{tenant_id}/{corpus_id}/{index_version}/`. Specify the FAISS index, stable chunk-ID mapping, document metadata, BM25 assets, embedding configuration, checksums, and build manifest. Define durable volumes, safe server-generated paths, locking, atomic publication, incremental updates, deletion propagation, rebuilding, backups, and recovery.

Enforce tenant and document permissions before material enters reranking, LLM context, caches, or responses. Use separate indexes or an explicitly secure permitted-candidate strategy; do not rely solely on filtering after global top-k retrieval. Load only trusted, integrity-checked index artifacts and avoid unsafe deserialization of uploaded objects.

Include citations, insufficient-evidence responses, conflicting-source handling, source freshness, conversation retention, and chat-history isolation.

**8. Market Research Agent and product opportunities**

Design a separate agent that searches the web through a maintained DuckDuckGo-capable tool. If using `ddgs`, verify the current API and explicitly configure the DuckDuckGo backend instead of silently using other search providers. Include rate limits, caching, timeouts, source-fetching controls, and honest unavailable-search behavior.

Investigate product trends, seasonality, local relevance, competitor prices, and assortment gaps. Match findings against the store catalog to distinguish products not carried from existing products temporarily out of stock. Handle brand, size, variant, and unit mismatches.

Retain source URLs, publication dates when available, retrieval timestamps, relevant evidence, region, and limitations. Search snippets, ads, and online popularity do not prove actual sales. Use a “best-selling” claim only when an identified source provides suitable sales/ranking evidence and explain its scope.

For a suggested new product, report evidence, local relevance, estimated margin assumptions, supplier feasibility, capital needs, shelf-life risk, a small pilot order, and a measurement/review date. Quantities for products with no sales history must be labeled scenario estimates with uncertainty. Avoid repeated recommendations through dismissal, snooze, budget limits, deduplication, and cooldown rules.

**9. Multi-agent roles, state, and review pipeline**

Design an orchestrator and appropriately scoped roles for market research, sales/customer retention, forecasting/analysis, operations/inventory/procurement, finance, HR support, writing/reporting, and independent review. Include a knowledge-retrieval capability; justify whether it needs an agent or a deterministic tool. Do not turn every calculation into a separate LLM agent.

For EVERY agent, provide role, goal, tasks, workflow, tools, input, permitted state/memory, output schema, trigger, dependencies, permissions, failure handling, escalation, and success criteria.

Combine the requested pipelines into one explicit workflow:

User input and authorization → research/retrieval → analyst and calculation tools → verification → organization and writing → reviewer → final report.

Use CrewAI's appropriate workflow features to define routing, persisted typed state, bounded retries, timeouts, evidence handoffs, and review outcomes. Simple lookups should take a short path; complex decisions should use the full pipeline. Do not invoke every agent for every request.

Define shared fields including run ID, tenant/user identity, request, evidence IDs, dataset/model versions, tool results, assumptions, limitations, draft, review findings, approval status, and final artifact references. Require structured handoffs rather than free-form undocumented messages.

The reviewer checks evidence, arithmetic, citations, completeness, contradictory claims, permissions, and requested format. Failed checks return to the responsible stage within a fixed retry limit; unresolved issues produce a qualified result or human escalation. LLM review complements deterministic checks and does not establish factual correctness by itself.

Finance supports cash-flow, margins, expenses, and budgeting using stated accounting assumptions. HR supports schedules, onboarding, and approved policy questions with restricted access to employee data. Keep consequential employment decisions under human control.

**10. Business process automation**

Specify workflows for scheduled forecasts, reorder alerts, draft purchase requests, slow-stock/expiry reviews, approved price proposals, repeat-customer campaigns, weekly finance summaries, staffing support, and periodic market research.

For each automation, define event/schedule, timezone, input requirements, conditions, responsible agent/service, output, approval requirements, audit events, retry policy, duplicate prevention, notification preferences, and cancellation. Distinguish advice, drafts awaiting approval, and actions authorized for execution. Approval must be tied to the exact proposed action and rechecked if inputs change.

**11. Website pages and visual design**

Provide a sitemap and page specification for Home, About Us with six member profiles, sign-in/onboarding, Dashboard, Upload & Data Quality, Demand Forecasting, Inventory & Reordering, Business Chatbot, Customer Insights, Market Opportunities, Sales & Pricing, Finance, HR & Operations, Reports & Downloads, Automation & Approvals, and Settings & Administration. Group pages sensibly and assign each to MVP, V1, or V2.

For every page, describe purpose, allowed roles, components, user actions, data/API dependencies, navigation, validation, loading/empty/error states, and acceptance criteria. Use placeholders for the six members' names, photos, and biographies; do not invent credentials.

Use a consistent three-color brand palette: navy `#0F172A`, teal `#0F766E`, and amber `#F59E0B`, with neutral white/light backgrounds. Explain usage, typography, spacing, accessible contrast, keyboard navigation, chart labels, and responsive behavior. Use dark text on amber where needed for contrast. Make the product understandable to store owners and keep infrastructure details out of normal user flows.

**12. Database and modular project structure**

Provide an ERD, data dictionary, relationships, key indexes, migrations, and tenant-scoping rules for organizations/stores, users, memberships/roles, products, suppliers, sales/line items, customers, inventory movements, stock snapshots, purchase orders, dataset versions, forecasts/model runs, recommendations, documents/chunks, research evidence, agent runs, approvals, reports, scheduled jobs, and audit logs. Add employee data only to the scoped HR module.

Define stock-ledger reconciliation, transactional consistency, idempotent imports, dataset lineage, and how corrections affect future forecasts and reports. Design constraints to prevent cross-tenant relationships.

Show a complete folder/file tree with separate modules for every page and feature. Include the app entry point, UI components, settings, database models/repositories/migrations, identity/authorization, ingestion/parsers/validation, forecasting/model adapters/backtesting, inventory math, customer analytics, RAG, agent roles/tasks/tools/flows, integrations, exports, workers/jobs, tests, and deployment configuration.

Explain each important file's responsibility and main interface. Keep business logic out of page files. Include dependency configuration, an environment-variable template with no secrets, README, synthetic sample data, Docker configuration, and CI. Exclude customer files, model caches, and runtime indexes from version control.

**13. Reports and requested output formats**

The chatbot and analytics pages must support text, Markdown tables, charts, Word/DOCX, PDF, Excel/XLSX, and CSV where suitable. Select an output format from the user's request and explain export scope and limitations.

Use a shared structured report object so all formats contain consistent figures, evidence, assumptions, and recommendations. Specify suitable libraries and chart/table rendering. Preserve numeric/date types in Excel and prevent spreadsheet formula injection from untrusted values.

Include report ID, generation timestamp, data period, source references, model/dataset versions, units/currency, limitations, and approval status. Define protected download access and retention. Provide sample final-report layouts and export acceptance criteria.

**14. Security, privacy, and governance**

Define authentication and authorization separately. Prefer a supported identity provider/OIDC integration, with server-side role and resource checks. Streamlit login alone is not the permission system. Cover owners/admins, managers, sales/inventory staff, finance, HR, and read-only analysts with an explicit permission matrix.

Include tenant isolation, least privilege, session expiry/revocation, MFA where supported, secret management, HTTPS, encryption at rest, rate limits, safe file types and size limits, parser isolation, malicious uploads, SQL injection, XSS, CSRF, path traversal, unsafe deserialization, and SSRF protections for fetched URLs.

Treat retrieved documents, web pages, and uploaded text as untrusted content. Specify prompt-injection defenses, tool allowlists, structured argument validation, and narrow database tools. Do not execute arbitrary generated Python, SQL, shell commands, or document macros. Enforce permissions again inside tools and workers.

Prevent data leakage through shared caches, logs, tracing, retrieval, chat history, report downloads, and third-party calls. Define what data may be sent to Groq/search services, redaction/minimization, user controls, and provider-policy verification. Public search queries must exclude confidential customer and business details.

Specify data ownership, retention/deletion/export, deletion propagation to indexes and backups, consent where applicable, access review, audit records, incident handling, model/prompt versioning, approval governance, and restoration tests. Identify jurisdiction-dependent requirements without asserting legal compliance. Do not allow cross-customer training or knowledge sharing without explicit authorization.

**15. Evidence, accuracy, completeness, quality, and efficiency**

Create a measurable quality matrix:

- Evidence: source provenance, citation validity, freshness, and claim support.
- Accuracy: forecast metrics, checked calculations, factual grounding, and calibrated uncertainty where available.
- Completeness: coverage of the question, required inputs, constraints, and requested output format.
- Quality: understandable explanations, useful next actions, consistent terminology, and usable exports.
- Efficiency: latency, token/API cost, tool calls, worker runtime, caching, and time saved.

For every metric, give the definition, test set, measurement method, proposed target, release gate, and monitoring owner. Set concrete targets based on stated workload and hardware assumptions; do not manufacture measured performance or unsupported confidence percentages.

Cover retrieval Recall@k/MRR/nDCG where appropriate, grounded-answer and citation evaluation, unknown-question handling, exact SKU matching, numerical reconciliation, and human review. Include security tests for unauthorized tenants/documents, prompt injection, stale permissions, and report access.

Test missing identifiers, sparse history, zero demand, stockouts, changing prices, malformed files, conflicting sources, unavailable APIs, duplicate jobs, concurrent index updates, deletion, and export consistency. Include smoke, integration, end-to-end, model-backtesting, and selected load tests. Explain representative synthetic data, held-out evaluation, monitoring, rollback, and realistic failure limits.

**16. Step-by-step development and team delivery plan**

End with an ordered implementation guide covering repository setup; Python environment and compatible dependencies; local database and migrations; identity/permissions; Streamlit navigation; import validation; baseline forecasting; inventory calculations; Hugging Face benchmarking; customer analytics; document ingestion; hybrid retrieval and citations; Groq chatbot; CrewAI workflows; web research; reporting; approvals/automation; hardening; deployment; monitoring; and maintenance.

For EACH step, provide objective, prerequisites, exact files to create/edit, commands where appropriate, inputs/outputs or interfaces, implementation actions, a small verification procedure, expected result, and completion criteria. Give minimal schemas or pseudocode where they resolve ambiguity. Include both local demo and production deployment paths and clearly label unverified commands or versions.

Provide a phased schedule with effort assumptions and dependencies, six-member ownership using Member 1–6 placeholders, shared interface contracts, Git branch/PR practices, integration milestones, risk register, and final acceptance checklist. Identify the first week of work and the first usable demo.

Include an operating-cost model for LLM calls, search, CPU/GPU inference, storage, database, and workers. Use explicit workload assumptions; verify dated prices if provided. Explain how batching, caching, smaller models, and selective agent routing control cost.

Finish with a traceability matrix mapping every capability in this prompt to its PRD requirement, development phase, owner, and acceptance test. Keep critical security and data isolation in the MVP. Clearly identify what remains advisory, unvalidated, deferred, or dependent on unavailable data.

**Source starting points to verify**

- Chronos-2 model card: https://huggingface.co/amazon/chronos-2
- Groq supported models: https://console.groq.com/docs/models
- CrewAI Flows: https://docs.crewai.com/en/concepts/flows
- Streamlit authentication: https://docs.streamlit.io/develop/concepts/connections/authentication
- FAISS documentation: https://github.com/facebookresearch/faiss/wiki
- DDGS package documentation: https://pypi.org/project/ddgs/

Use official sources for technical claims. Treat these links as starting points requiring verification at the time the PRD is written. The final result must be a coherent product specification and executable development plan, not a collection of disconnected technology descriptions.
