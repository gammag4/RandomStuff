# CUDA graphs + streams

import torch

model.eval()
static_input = torch.empty_like(real_input, device=device) # Creates input buffer

# 2. Warmup (Obrigatório para inicializar drivers e memória)
s = torch.cuda.Stream()
s.wait_stream(torch.cuda.current_stream())
with torch.cuda.stream(s):
    for _ in range(3):
        with torch.no_grad(): # When using only inference
            static_output = model(static_input)

    # TODO will it work recording in separate stream?
    # Record once
    g = torch.cuda.CUDAGraph()
    with torch.cuda.graph(g):
        static_output = model(static_input)  # static_output is also a buffer

torch.cuda.current_stream().wait_stream(s)

with torch.no_grad():
    for real_input in stream:
        # Each frame - just replay the graph, no kernel launch overhead
        static_input.copy_(real_input)
        g.replay()
        out = static_output # Do .clone() if you need to access output outside buffer
        # do something with out
