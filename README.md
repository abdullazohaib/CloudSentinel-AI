# CloudSentinel AI

## AI-Powered Cloud Incident Response & Observability Platform

CloudSentinel AI is an AI-assisted cloud incident response platform that helps engineers investigate incidents, analyze logs, identify probable root causes, and generate recovery recommendations.

## Features

- Dashboard and platform health monitoring
- Incident management with SQLite
- AI incident analysis
- LangGraph orchestration
- Ollama-powered RCA enhancement
- Severity classification
- Root Cause Analysis
- Recovery recommendations
- Kubernetes health monitoring
- Prometheus metrics
- Settings page
- Docker deployment
- Automated backend tests

## Architecture

```text
React Frontend
      ↓
FastAPI
      ↓
LangGraph
      ↓
Severity
      ↓
RCA
      ↓
Ollama
      ↓
Recommendations