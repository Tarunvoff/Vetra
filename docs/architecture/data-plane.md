# Data Plane & Engine Adapters

Vetra interacts with data-plane inference engines via the `IInferenceEngineAdapter` contract.

## Adapters
- **vLLM Adapter**: Primary implementation parsing live Prometheus exposition metrics from `/metrics`.
- **SGLang Adapter**: Planned RadixAttention adapter stub.
- **TensorRT-LLM Adapter**: Planned NVIDIA runtime adapter stub.
- **Simulated Adapter**: Complete offline simulation engine generating realistic GPU and KV cache state.
