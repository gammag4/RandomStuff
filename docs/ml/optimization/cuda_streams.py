# CUDA streams

import torch

# Create a custom stream
s1 = torch.cuda.Stream()

# Context manager to queue work into that stream
with torch.cuda.stream(s1):
    # These ops are now asynchronous relative to the default stream
    A = torch.randn(100, 100, device='cuda')
    B = torch.mm(A, A)

# Synchronize if you need the results immediately on the CPU
torch.cuda.synchronize()  # Blocks CPU until all tasks in all streams are finished


# Synchronize between two streams:
event.record(stream)  # Marks a point in a stream's timeline.
# Makes a stream wait until the recorded event is finished.
stream.wait_event(event)
