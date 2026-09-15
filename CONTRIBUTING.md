# Contributing to Vetra

Thank you for contributing to Vetra! Vetra is an open-source control plane for Key-Value cache management in LLM inference engines.

## Architectural Principles

1. **Control Plane, Not Inference Engine**: Never fork or duplicate inference internals. Vetra decides policy; inference engines (vLLM, SGLang, TensorRT-LLM) execute.
2. **Clean Dependency Separation**: `vetra/core/` must never import web frameworks (FastAPI), databases (Redis), or inference libraries (vLLM).
3. **Dry-Run by Default**: Never perform destructive memory operations without explicit capability checks and dry-run flags disabled.
4. **Transparent Status Reporting**: Always distinguish implemented features (`LIVE`), simulated metrics (`SIMULATION`), and architectural stubs (`STUB`).

## Development Workflow

1. Clone the repository and install editable dependencies:
   ```bash
   git clone https://github.com/vetra/vetra.git
   cd vetra
   pip install -e ".[dev,simulation]"
   ```
2. Run tests:
   ```bash
   pytest tests/
   ```
3. Run linter and formatter:
   ```bash
   ruff check vetra/ tests/
   ruff format vetra/ tests/
   ```
4. Verify system dependencies:
   ```bash
   vetra doctor
   ```

## Commit Message Guidelines

Follow conventional commit formats:
- `feat(component): add new feature`
- `fix(component): fix bug`
- `docs(component): update documentation`
- `test(component): add or update tests`
