# https://docs.pytorch.org/TensorRT/
# Can also deploy to C++

# TensorRT vs PyTorch


# TensorRT - NVIDIA's separate inference optimizer that converts your PyTorch model to a highly optimized TensorRT engine (uses graph optimization, layer fusion, precision calibration).
# To use, export model via ONNX and convert it.

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

#!pip install tensorrt

# Option 1: torch.compile with TensorRT backend (simplest)
import torch
import torch_tensorrt
model = model.to('cuda').half()  # or .bfloat16()
model = torch.compile(model, backend="tensorrt")

# Option 2: torch2trt (older superseded by torch.compile)
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
