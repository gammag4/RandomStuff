# CUDA graphs + torch.compile + AMP

import torch
import torch.backends.cudnn as cudnn

cudnn.benchmark = True  # Enable cuDNN autotuning

# For more aggressive caching - Force torch to cache compiled kernels
# torch._dynamo.config.cache_size_limit = 64
# torch._inductor.config.triton.cudagraphs = True

model = model.cuda().eval()
try:
    model = torch.compile(model, mode="default")  # or "reduce-overhead", "max-autotune"
    # Or try with inductor backend
    # model = torch.compile(model, backend="inductor", mode="default")
except Exception as e:
    # If compile fails, fallback
    print(f"Compile failed: {e}, using original model")

# Warmup runs - triggers JIT kernel compilation
dummy_input = torch.randn(1, *input_shape).cuda()
for _ in range(10):
    with torch.no_grad(), torch.cuda.amp.autocast(dtype=torch.bfloat16):
        _ = model(dummy_input)

torch.cuda.synchronize()  # Ensure all kernels are compiled


# Use
with torch.cuda.amp.autocast(dtype=torch.bfloat16):
    out = model(dummy_input)


Modes:
- "default" - balanced compilation(better for larger models)
- "reduce-overhead" - lower latency, good for real-time
- "max-autotune" - slowest compile, fastest inference(batch)

This pre-warms:
- cuDNN kernels(finds fastest conv/linear algos)
- CUDA JIT compilation of torch operations
- CUDA graph capture if applicable
