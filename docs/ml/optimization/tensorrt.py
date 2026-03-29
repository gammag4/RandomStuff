# TensorRT

import tensorrt as trt

# Create builder with BF16 support
builder = trt.Builder(logger)
config = builder.create_builder_config()
config.set_flag(trt.BuilderFlag.BF16)

# Build engine
network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
# ... parse your model into network ...

engine = builder.build_serialized_network(network, config)



#With PyTorch (torch2trt or torch.compile)

# Option 1: torch.compile with TensorRT backend (simplest)
model = model.to('cuda').half()  # or .bfloat16()
model = torch.compile(model, backend="tensorrt")

# Option 2: torch2trt (older but works)
from torch2trt import torch2trt
model = model.to('cuda').half()
model_trt = torch2trt(model, [input_sample], fp16=True)



#For Your Real-Time Use Case

import torch
import tensorrt as trt

# Convert and compile in one step
model = model.to('cuda').bfloat16()
model = torch.compile(model, backend="tensorrt")

# Warmup
for _ in range(10):
    _ = model(warmup_input)
torch.cuda.synchronize()
