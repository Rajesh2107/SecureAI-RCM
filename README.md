

\# SecureAI-RCM

\### AI Security \& Governance for Healthcare Revenue Cycle Management



!\[Python](https://img.shields.io/badge/Python-3.12-blue)

!\[FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)

!\[Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)

!\[Ollama](https://img.shields.io/badge/AI-Ollama-black)

!\[Security](https://img.shields.io/badge/AI\_Security-Enabled-purple)



\## Overview



SecureAI-RCM is an educational AI security project designed to demonstrate secure AI-assisted healthcare Revenue Cycle Management (RCM).



The platform analyzes synthetic healthcare claim denials and generates AI-assisted explanations using a locally hosted Large Language Model (LLM).



The project demonstrates practical implementation of AI security controls, validation, governance, and auditability.



\## Objectives



\- Build a local AI-assisted healthcare RCM application.

\- Implement prompt injection detection.

\- Detect and mask sensitive information.

\- Validate AI-generated denial explanations.

\- Implement groundedness and response-quality checks.

\- Maintain security audit logs.

\- Demonstrate AI security testing and governance.



\## Architecture



```mermaid

flowchart TD

&#x20;   A\[User] --> B\[Streamlit Dashboard]

&#x20;   B --> C\[FastAPI Backend]

&#x20;   C --> D\[Security Gateway]

&#x20;   D --> E\[Prompt Injection Detection]

&#x20;   D --> F\[PHI Detection and Masking]

&#x20;   D --> G\[Claim Validation]

&#x20;   G --> H\[Knowledge Retrieval]

&#x20;   H --> I\[Local Ollama LLM]

&#x20;   I --> J\[Output Validation]

&#x20;   J --> K\[Groundedness]

&#x20;   J --> L\[Response Quality]

&#x20;   J --> M\[Denial Validation]

&#x20;   J --> N\[Human Review]

&#x20;   J --> O\[Audit Logger]

```



\## Key Features



\### AI Security

\- Prompt injection detection.

\- PHI pattern detection.

\- Sensitive information masking.

\- Local AI inference.



\### AI Governance

\- Advisory-only AI responses.

\- Mandatory human review.

\- Output validation.

\- Groundedness checks.

\- Response-quality checks.

\- Security audit logging.



\### Security Testing

\- Automated security test suite.

\- Prompt injection test cases.

\- PHI detection tests.

\- PHI masking validation.

\- Security score calculation.

\- Interactive security testing dashboard.



\## Technology Stack



| Component | Technology |

|---|---|

| Programming | Python |

| Backend | FastAPI |

| Frontend | Streamlit |

| AI Runtime | Ollama |

| AI Models | Qwen |

| Data | JSON / JSONL |

| Testing | Pytest / Custom Security Tests |

| API Documentation | Swagger / OpenAPI |



\## Project Structure



```text

SecureAI-RCM/

├── app/

│   ├── ai/

│   ├── audit/

│   ├── frontend/

│   ├── knowledge/

│   ├── security/

│   └── validation/

├── datasets/

├── docs/

│   ├── THREAT\_MODEL.md

│   └── ARCHITECTURE.md

├── logs/

├── app/

├── run\_security\_lab.py

└── README.md

```



\## Getting Started



\### Prerequisites



\- Windows 11

\- Python 3.12+

\- Ollama

\- Git (optional)



\### 1. Clone Repository



```powershell

git clone https://github.com/YOUR\_USERNAME/SecureAI-RCM.git

cd SecureAI-RCM

```



\### 2. Create Virtual Environment



```powershell

python -m venv .venv

```



\### 3. Install Dependencies



```powershell

.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt

```



\### 4. Start Ollama



Install Ollama and download a compatible model:



```powershell

ollama pull qwen3:1.7b

ollama serve

```



If Ollama is already running, continue without starting another instance.



\### 5. Start FastAPI Backend



```powershell

.\\.venv\\Scripts\\python.exe -m uvicorn app.main:app --reload

```



API documentation:



http://127.0.0.1:8000/docs



\### 6. Start Streamlit Dashboard



Open another PowerShell terminal:



```powershell

.\\.venv\\Scripts\\python.exe -m streamlit run app/frontend/dashboard.py --server.port 8502

```



Dashboard:



http://localhost:8502



\## Security Testing



Run the security test suite:



```powershell

.\\.venv\\Scripts\\python.exe run\_security\_lab.py

```



\### Current Test Results



| Test | Status |

|---|---|

| Prompt Injection Detection | PASS |

| Email PHI Detection | PASS |

| Phone PHI Detection | PASS |

| Safe Prompt Validation | PASS |

| PHI Masking | PASS |

| SSN Detection | PASS |



\*\*Initial Security Test Result: 6/6 PASS (100%)\*\*



Note: This score represents the six implemented test cases, not overall security effectiveness.



\## Documentation



\- \[Threat Model](docs/THREAT\_MODEL.md)

\- \[Architecture](docs/ARCHITECTURE.md)



\## Security Limitations



\- Prompt injection detection is pattern-based.

\- PHI detection uses regex and is incomplete.

\- Groundedness checks are heuristic.

\- Claim-level authorization is not implemented.

\- Audit logs are not tamper-proof.

\- AI-generated explanations may be incorrect.

\- Security tests cover a limited number of scenarios.



\## Disclaimer



SecureAI-RCM is an educational AI security prototype.



\- Synthetic data only.

\- No production patient information.

\- No autonomous claim approval.

\- Human review required.

\- Not a production healthcare application.

\- Does not establish HIPAA or ISO 27001 compliance.



\## Future Roadmap



\- Advanced adversarial AI testing.

\- AI risk assessment and threat modeling.

\- Improved PHI detection.

\- Audit integrity enhancements.

\- Role-based access control.

\- Docker deployment.

\- CI/CD security testing.

\- AI governance reporting.



\## Author



\*\*Rajesh Chavan\*\*



Cybersecurity | AI Security | Security Operations | Cloud Security





