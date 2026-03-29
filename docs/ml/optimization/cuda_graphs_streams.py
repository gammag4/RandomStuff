# CUDA graphs + streams

import torch

model.eval()
static_input = torch.empty_like(real_input, device=device) # Creates input buffer

# 2. Warmup (Obrigatório para inicializar drivers e memória)
s = torch.cuda.Stream()
s.wait_stream(torch.cuda.current_stream())
with torch.cuda.stream(s):
    for _ in range(3):
        static_output = model(static_input)
torch.cuda.current_stream().wait_stream(s)

# Record once
g = torch.cuda.CUDAGraph()
with torch.cuda.graph(g):
    static_output = model(static_input) # static_output is also a buffer

# Each frame - just replay the graph, no kernel launch overhead
static_input.copy_(real_input)
g.replay()
out = static_output # Do .clone() if you need to access output outside buffer
