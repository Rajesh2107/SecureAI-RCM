

\# SecureAI-RCM Threat Model



\## 1. Project Overview



SecureAI-RCM is a local AI-assisted healthcare Revenue Cycle Management (RCM) denial explanation platform.



The system uses synthetic claims, a local LLM, a denial-code knowledge base, security controls, output validation, and audit logging.



The AI provides advisory explanations only. Human review is mandatory.



\## 2. Scope



\### In Scope



\- Synthetic healthcare claim records

\- AI-generated denial explanations

\- Local LLM inference using Ollama

\- Prompt injection detection

\- PHI pattern detection and masking

\- Denial-code reference retrieval

\- Output validation and groundedness checks

\- Security audit logging

\- Security testing dashboard



\### Out of Scope



\- Production patient information

\- Real payer integrations

\- Production EHR integrations

\- Autonomous claim submission

\- Autonomous claim approval

\- Clinical decision-making

\- Production identity federation

\- Production-grade compliance certification



\## 3. Architecture



```text

User

&#x20;|

&#x20;v

Streamlit Dashboard

&#x20;|

&#x20;v

FastAPI Backend

&#x20;|

&#x20;+--> Security Gateway

&#x20;|      |

&#x20;|      +--> Prompt Injection Detection

&#x20;|      +--> PHI Detection

&#x20;|      +--> PHI Masking

&#x20;|

&#x20;+--> Claim Validation

&#x20;|

&#x20;+--> Knowledge Retrieval

&#x20;|

&#x20;+--> Local LLM (Ollama)

&#x20;|

&#x20;+--> Output Validation

&#x20;|      |

&#x20;|      +--> Denial Validation

&#x20;|      +--> Groundedness

&#x20;|      +--> Response Quality

&#x20;|

&#x20;+--> Security Audit Logger

&#x20;|

&#x20;v

AI Explanation + Human Review

```



\## 4. Assets



| Asset | Security Requirement |

|---|---|

| Synthetic Claims | Integrity and confidentiality |

| Knowledge Base | Integrity and accuracy |

| AI Prompt | Confidentiality and integrity |

| AI Output | Integrity and explainability |

| Audit Logs | Integrity and accountability |

| Security Configuration | Integrity |

| Local Model | Integrity and controlled access |



\## 5. Threat Catalog



| ID | Threat | Impact |

|---|---|---|

| T-01 | Prompt Injection | Unauthorized instruction execution |

| T-02 | PHI Exposure | Healthcare data leakage |

| T-03 | Sensitive Data Logging | Confidentiality violation |

| T-04 | AI Hallucination | Incorrect denial explanation |

| T-05 | Knowledge Base Poisoning | Incorrect AI output |

| T-06 | Unauthorized Claim Access | Data exposure |

| T-07 | Model Manipulation | Unsafe or misleading responses |

| T-08 | Excessive AI Agency | Unauthorized business actions |

| T-09 | Incomplete Audit Logging | Reduced accountability |

| T-10 | Denial Validation Failure | Incorrect recommendations |



\## 6. Security Controls



| Threat | Implemented Control |

|---|---|

| T-01 | Regex-based prompt injection detection |

| T-02 | Regex PHI detection and masking |

| T-03 | Security audit logging |

| T-04 | Groundedness and response-quality checks |

| T-05 | Reference knowledge retrieval |

| T-06 | Not yet implemented: claim-level authorization |

| T-07 | Local model execution and controlled prompts |

| T-08 | Advisory-only AI; human review |

| T-09 | JSONL audit event logging |

| T-10 | Denial-code validation |



\## 7. STRIDE Analysis



| STRIDE Category | Example | Mitigation |

|---|---|---|

| Spoofing | Unauthorized claim identity | Future authentication and authorization |

| Tampering | Knowledge base modification | File integrity controls |

| Repudiation | Missing AI activity evidence | Audit logging |

| Information Disclosure | PHI exposure | Detection and masking |

| Denial of Service | Excessive AI requests | Future rate limiting |

| Elevation of Privilege | Prompt injection | Prompt guard and controlled execution |



\## 8. OWASP LLM Security Mapping



| Risk | SecureAI-RCM Relevance |

|---|---|

| LLM01 Prompt Injection | Prompt guard |

| LLM02 Sensitive Information Disclosure | PHI detection and masking |

| LLM03 Supply Chain | Local model and dependency management |

| LLM04 Data and Model Poisoning | Knowledge base integrity |

| LLM05 Improper Output Handling | Output validation |

| LLM06 Excessive Agency | Human review and advisory-only AI |

| LLM07 System Prompt Leakage | Prompt injection testing |

| LLM08 Vector and Embedding Weaknesses | Knowledge retrieval integrity |

| LLM09 Misinformation | Groundedness and response-quality checks |

| LLM10 Unbounded Consumption | Future rate limiting and resource controls |



\## 9. Residual Risks



\- Regex-based PHI detection can miss sensitive information.

\- Prompt injection detection is pattern-based and bypassable.

\- Groundedness checks are heuristic, not proof of correctness.

\- Knowledge base content requires authoritative verification.

\- No production authentication or claim-level authorization.

\- Audit logs do not yet provide tamper-proof integrity.

\- AI output may be incorrect or incomplete.

\- Security testing covers a limited set of scenarios.



\## 10. Risk Treatment



| Risk | Treatment |

|---|---|

| Prompt Injection | Mitigate |

| PHI Exposure | Mitigate |

| AI Hallucination | Mitigate and monitor |

| Unauthorized Access | Future implementation |

| Audit Integrity | Future implementation |

| Autonomous AI Decisions | Avoid |

| Production PHI Usage | Avoid in current project |



\## 11. Governance



\- AI explanations are advisory.

\- Human review is mandatory.

\- Synthetic data only.

\- No autonomous claim approval.

\- Security testing before releases.

\- Audit logging enabled.

\- Known limitations documented.

\- AI output must be independently validated.



\## 12. Project Disclaimer



SecureAI-RCM is an educational AI security prototype.



It is not a production healthcare application, does not establish HIPAA or ISO 27001 compliance, and has not undergone independent security certification.



