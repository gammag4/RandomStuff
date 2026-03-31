import torch
import threading
from collections import deque


class AsyncInference:
    def __init__(self, model, max_queued=10):
        self.model = model
        self.stream = torch.cuda.Stream()
        self.queue = deque()
        self.results = {}
        self.running = True
        self.thread = threading.Thread(target=self._worker)
        self.thread.start()
        self.counter = 0

    def submit(self, inp):
        idx = self.counter
        self.counter += 1
        self.queue.append((idx, inp))
        return idx

    def get(self, idx):
        while idx not in self.results:
            time.sleep(0.001)
        return self.results.pop(idx)

    def _worker(self):
        while self.running:
            if self.queue:
                idx, inp = self.queue.popleft()
                with torch.cuda.stream(self.stream):
                    out = self.model(inp)
                    self.results[idx] = out.cuda().clone()  # sync back
            else:
                time.sleep(0.001)
