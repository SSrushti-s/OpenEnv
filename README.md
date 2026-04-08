# OpenEnv
# 📧 Email Triage OpenEnv
**Real-World AI Agent Environment for Office Productivity**

This project is a complete, real-world simulation of an email triage task designed for AI agents to learn and be evaluated using the **OpenEnv standard**.

## 🚀 Live Demo
The environment is containerized and running on Hugging Face Spaces:
🔗 **(https://srushtis16-mywork.hf.space/docs)**

---

## 📋 Features
- **OpenEnv Spec Compliant**: Implements the standard `step()`, `reset()`, and `state()` API.
- **3 Challenge Tasks**:
  - **Easy**: Basic spam detection and deletion.
  - **Medium**: Multi-folder organization (Work/Social/Spam).
  - **Hard**: Intelligent priority identification and drafting replies.
- **Programmatic Graders**: High-precision scoring (0.0 to 1.0) based on final state and action history.

## 🛠️ Local Setup
To run this environment locally for development:

1. **Install Dependencies**:
   ```bash
   pip install fastapi uvicorn pydantic requests
