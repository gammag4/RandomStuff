# example trying to implement TBPTT without recomputing entire context window
# check https://discuss.pytorch.org/t/python-functions-to-create-nodes-modify-graph/57275
# check https://jott.live/markdown/Writing%20a%20Toy%20Backend%20Compiler%20for%20PyTorch
# There probably is a better way creating a custom torch.autograd.Function (the backward function of it is the function that goes in grad_fn)

import torch

f = torch.nn.Sequential(torch.nn.Linear(5, 5), torch.nn.ReLU())
optimizer = torch.optim.SGD(f.parameters())

window = 100
iterations = [torch.zeros(5, dtype=torch.float32)]
data = torch.randn(1000, 5)

for i, d in enumerate(data):
    print(i)

    res = f(iterations[-1])
    iterations.append(res)

    (res - d).sum().abs().backward(retain_graph=True)
    optimizer.zero_grad()
    optimizer.step()

    if i > window:
        # Something to break graph here
        del iterations[0]
        _ = iterations[0].detach_().requires_grad_(True)
