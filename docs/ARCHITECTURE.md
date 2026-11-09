

\# SecureAI-RCM — Architecture



\## 1. Architecture Overview



SecureAI-RCM is a local AI-assisted healthcare Revenue Cycle Management (RCM) denial explanation prototype. It uses synthetic claims, FastAPI, Streamlit, Ollama, security validation, and audit logging.



\## 2. Architecture Diagram



```mermaid

flowchart TD

&#x20;   U\[User] --> UI\[Streamlit Dashboard]

&#x20;   UI --> API\[FastAPI Backend]

&#x20;   API --> SG\[Security Gateway]

&#x20;   SG --> PG\[Prompt Injection Detection]

&#x20;   SG --> PHI\[PHI Detection and Masking]

&#x20;   SG --> CV\[Claim Validation]

&#x20;   CV --> KR\[Denial Knowledge Retrieval]

&#x20;   KR --> LLM\[Local Ollama LLM]

&#x20;   LLM --> OV\[Output Validation]

&#x20;   OV --> DV\[Denial Code Validation]

&#x20;   OV --> GV\[Groundedness Checks]

&#x20;   OV --> RQ\[Response Quality Checks]

&#x20;   OV --> HR\[Human Review Required]

&#x20;   OV --> AL\[Audit Logger]

&#x20;   AL --> UI

```



\## 3. Technology Stack



| Component | Technology |

|---|---|

| Frontend | Streamlit |

| Backend | FastAPI |

| AI Runtime | Ollama |

| AI Model | Qwen |

| Language | Python |

| Security | Prompt Guard, PHI Detection, Masking |

| Validation | Denial Validation, Groundedness, Response Quality |

| Audit | JSONL Security Audit |

| Testing | Python Security Test Lab |



\## 4. Security Design Principles



\- Synthetic data only.

\- Local model inference.

\- Prompt injection screening.

\- PHI detection and masking.

\- Knowledge-based denial explanations.

\- Output validation.

\- Human review.

\- Security audit logging.

\- Advisory-only AI outputs.



\## 5. Limitations



\- Prompt injection detection uses pattern-based screening.

\- PHI detection is regex-based and incomplete.

\- Groundedness checks are heuristic.

\- No production authentication or claim-level authorization.

\- Audit logs are not tamper-proof.

\- AI-generated explanations may be incorrect.

\- This prototype is not production-ready or a compliance certification.

```



Save and close.



\## Step 3 — Verify Documentation



Run:



```powershell

Get-ChildItem docs

```



Expected:



```text

THREAT\_MODEL.md

ARCHITECTURE.md

```



\*\*Next milestone:\*\* Professional `README.md` with project overview, features, architecture, setup instructions, demo screenshots, security testing results, and GitHub-ready presentation.

