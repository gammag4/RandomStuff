## Profiling/debugging

https://discuss.pytorch.org/t/how-to-measure-time-in-pytorch/26964

`torch.cuda.synchronize()` waits for CUDA operations to finish running

Naive way

```
torch.cuda.synchronize()
start = time.time()

# Operation ...

torch.cuda.synchronize()
elapsed = time.time() - start
```

Better way

```
start = torch.cuda.Event(enable_timing=True)
end = torch.cuda.Event(enable_timing=True)

start.record()

# Operation ...

end.record()

torch.cuda.synchronize()
elapsed = start.elapsed_time(end)
```

TODO
https://docs.pytorch.org/docs/stable/profiler.html
https://docs.pytorch.org/docs/stable/autograd.html#debugging-and-anomaly-detection
https://docs.pytorch.org/docs/stable/autograd.html#module-torch.autograd.gradcheck
https://docs.pytorch.org/docs/stable/autograd.html#profiler

TODO
torch.cuda.nvtx.range_push

TODO check both how to profile to find functions that waste most time and also where there are most transfers between cpu and gpu

Best way

It’ll tell you the CPU and CUDA timings of your functions

```
with torch.autograd.profiler.profile(use_cuda=True) as prof:
  # Operation ...
print(prof)
```

## Performance

### Floating-point formats and AMP

TODO
https://itsabout.ai/understanding-data-types-in-ai-and-hpc-int8-fp8-fp16-bf16-bf32-fp32-tf32-fp64-and-hardware-accelerators/?utm_source=chatgpt.com
https://www.flyriver.com/s/tf32?utm_source=chatgpt.com

its not just the exponent bits and mantissa, some of these use specific algorithms for multiplication/division that can be divided into multiple components and some of these are removed for faster computations

https://docs.nvidia.com/deeplearning/performance/mixed-precision-training/index.html

Operation in a tensor core: D = A x B + C
tf32 is a tensor core mode, not a type
In single precision, all tensors are in fp32, A and B are converted to tf32 before multiplication, the multiplication result is stored in fp32 and then summed with C

Don't forget to always let any tensor parameters you can as divisible by large powers of 2 (tensor shapes, layer input/output sizes, ...)
Use at least divisible by 8 to allow tensor core usage
Choose preferably 64 and up to 256
This allows GPU to break operations more evenly
Larger powers don't have that much benefit because most of the size will break down evenly anyway (e.g. breaking down a tensor size 3300 vs 100 tensors size 33)
Pad values sometimes when possible

Note that the operation in a tensor core only requires half precision in A and B, which means you don't need to use mixed precision in biases, only weights

### AMP

When using AMP, only forward passes should be autocasted (including computing loss)
Backward passes should not be autocasted
In an outocast region, tensors might be any type, and you should not convert tensors to other types in these regions
Type mismatch errors in an autocast-enabled region are a bug

Train

```
import torch

device = 'cuda'
enabled = True

# Creates once at the beginning of training
scaler = torch.amp.GradScaler(device=device, enabled=enabled)

for data, label in data_iter:
  optimizer.zero_grad(set_to_none=True)

  # Casts operations to mixed precision
  with torch.amp.autocast(device_type=self.device, dtype=torch.bfloat16, enabled=enabled):
    # output.dtype is float16 because linear layers autocast to bfloat16.
    output = model(data)
    # loss.dtype is float32 because mse_loss layers autocast to float32.
    loss = loss_fn(output, label)

  # Exits autocast before backward()
  # Backward passes under autocast are not recommended
  # Backward ops run in the same dtype autocast chose for corresponding forward ops

  # Scales the loss, and calls backward()
  # to create scaled gradients
  scaler.scale(loss).backward()

  # All gradients are scaled in this region up to scaler.step(optimizer), so they need to be unscaled to be used
  # Unscales the gradients of optimizer's assigned params in-place
  scaler.unscale_(optimizer)

  # Gradient clipping
  # Since the gradients of optimizer's assigned params are unscaled, clips as usual
  torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm)

  # Unscales gradients (if not unscaled before) and calls or skips optimizer.step()
  # It skips gradients if contains infs or NaNs
  # Since we called unscale_ before, it will not unscale gradients again
  scaler.step(optimizer)

  # Updates the scale for next iteration
  scaler.update()
```

Inference

```
model = Net().eval()
with torch.autocast(device_type="cpu", dtype=torch.bfloat16):
  for input in data:
    # Runs the forward pass with autocasting.
    output = model(input)
```

Autocast can also be used as decorator in model forward

```
@torch.autocast(device_type="cuda")
def forward(self, input):
  ...
```

Nesting autocast-disabled regions:

```
with torch.autocast(device_type="cuda"):
  e_float16 = torch.mm(a_float32, b_float32)
  with torch.autocast(device_type="cuda", enabled=False):
    # Calls e_float16.float() to ensure float32 execution
    # (necessary because e_float16 was created in an autocasted region)
    f_float32 = torch.mm(c_float32, e_float16.float())

  # No manual casts are required when re-entering the autocast-enabled region.
  # torch.mm again runs in float16 and produces float16 output, regardless of input types.
  g_float16 = torch.mm(d_float32, f_float32)
```

Gradients in the region between `scaler.scale(loss).backward()` and `scaler.step(optimizer)` are scaled
To inspect them, you need to unscale them first
When unscaling them before `scaler.step`, `scaler.step` will not unscale them anymore

```
scaler.unscale_(optimizer)
# Do stuff ...
```

Checkpointing loss scale

```
# Loading
checkpoint = torch.load('checkpoint’)
scaler.load_state_dict(checkpoint['scaler'])
...

# Saving
checkpoint = {
  'scaler': scaler.state_dict(),
  ...
}
torch.save(checkpoint, path)
```

### DistributedDataParallel (DDP)

- DataParallel (DP): An older approach to parallelism which is less performant than DDP and hence DDP should be preferred
  - Model is replicated and destroyed at each forward pass, whereas in DDP model is only replicated once
  - Only supports single-node parallelism, whereas DDP supports multi-node
  - Slower, uses multithreading on a single process and runs into Global Interpreter Lock (GIL) contention, whereas DDP has no GIL contention bc it uses multiprocessing
- DistributedDataParallel (DDP): Pattern where the model trains in parallel in multiple gpus
  - Data gets copied into all gpus
  - Then the dataset is broken into samples that go each to one gpu
  - Then the forward and backward pass happen in the gpus
  - Then the gradients from the backward pass are synchronized between the gpus
    - Synchronizes using the [ring all-reduce algorithm](https://tech.preferred.jp/en/blog/technologies-behind-distributed-deep-learning-allreduce/)
  - More details on the inner workings [here](https://docs.pytorch.org/docs/stable/notes/ddp.html)
- `torchrun`:
  - It is fault-tolerant: When one process goes wrong, all the processes get automatically restarted

Some layers need to be converted for DDP to work (e.g. `BatchNorm` to `SyncBatchNorm`)

Processes, jobs and groups:

- A node is generally a logical machine, a VM in the cloud with multiple GPUs
- A job is the overall work you will do
- The job is composed of multiple nodes, each with multiple GPUs
- It runs one global process group (called world), which has all processes across all nodes
  - The process group allows these processes to discover each other and communicate
  - When in single node, `torchrun` handles this by itself
  - When in multiple nodes they synchronize and communicate using a rendezvous job
- Normally, each GPU runs one process
  - It could run more than one in a GPU or there could be a GPU with no processes, but both would be suboptimal
  - The processes are differentiated by specifying env vars like `LOCAL_RANK` and `RANK`
  - Other variables like `WORLD_SIZE`, `MASTER_ADDR`, `MASTER_PORT` are the same to all processes
- Master: The machine that coordinates communications between processes in the group

Vars:

- `MASTER_ADDR` and `MASTER_PORT` specify the IP and port of the master
- `WORLD_SIZE`: Total number of processes in a group
- `RANK` (or global rank): Unique id given to each process (between 0 to world_size - 1) in the group
- `LOCAL_RANK`: Id given to each process in a node
- `NODE_RANK`: Unique id given to each node
- These are all set by `torchrun`



- When using multi-node, be sure that the nodes can communicate with each other over TCP (not just opening ICMP)
- one can explicity specify network interface by using `NCCL_SOCKET_IFNAME=eth0`
  - generally the rendezvous job finds it automatically, so no need for that
- Debugging
  - `NCCL_DEBUG=INFO` can also help you identify bugs by making it verbose
  - `NCCL_DEBUG_SUBSYS` can also be used for details about specific aspects of NCCL
  - More on debugging [here](https://docs.pytorch.org/docs/stable/distributed.html#debugging-torch-distributed-applications)
- All NCCL env vars [here](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html)





newer, taken from https://docs.pytorch.org/docs/stable/elastic/run.html#definitions

Definitions

- `Node`: A physical instance or a container; maps to the unit that the job manager works with.
- `Worker`: A worker in the context of distributed training.
- `WorkerGroup`: The set of workers that execute the same function (e.g. trainers).
- `LocalWorkerGroup`: A subset of the workers in the worker group running on the same node.
- `RANK`: The rank of the worker within a worker group.
- `WORLD_SIZE`: The total number of workers in a worker group.
- `LOCAL_RANK`: The rank of the worker within a local worker group.
- `LOCAL_WORLD_SIZE`: The size of the local worker group.
- `rdzv_id`: A user-defined id that uniquely identifies the worker group for a job. This id is used by each node to join as a member of a particular worker group.
- `rdzv_backend`: The backend of the rendezvous (e.g. c10d). This is typically a strongly consistent key-value store.
- `rdzv_endpoint`: The rendezvous backend endpoint; usually in form `<host>:<port>`.

A Node runs `LOCAL_WORLD_SIZE` workers which comprise a `LocalWorkerGroup`. The union of all `LocalWorkerGroups` in the nodes in the job comprise the `WorkerGroup`.

Environment Variables

- `LOCAL_RANK`: The local rank.
- `RANK`: The global rank.
- `GROUP_RANK`: The rank of the worker group. A number between 0 and max_nnodes. When running a single worker group per node, this is the rank of the node.
- `ROLE_RANK`: The rank of the worker across all the workers that have the same role. The role of the worker is specified in the `WorkerSpec`.
- `LOCAL_WORLD_SIZE`: The local world size (e.g. number of workers running locally); equals to `--nproc-per-node` specified on `torchrun`.
- `WORLD_SIZE`: The world size (total number of workers in the job).
- `ROLE_WORLD_SIZE`: The total number of workers that was launched with the same role specified in `WorkerSpec`.
- `MASTER_ADDR`: The FQDN of the host that is running worker with rank 0; used to initialize the Torch Distributed backend.
- `MASTER_PORT`: The port on the `MASTER_ADDR` that can be used to host the C10d TCP store.
- `TORCHELASTIC_RESTART_COUNT`: The number of worker group restarts so far.
- `TORCHELASTIC_MAX_RESTARTS`: The configured maximum number of restarts.
- `TORCHELASTIC_RUN_ID`: Equal to the rendezvous `run_id` (e.g. unique job id).
- `PYTHON_EXEC`: System executable override. If provided, the python user script will use the value of `PYTHON_EXEC` as executable. The sys.executable is used by default.



[DDP YT Series](https://www.youtube.com/playlist?list=PL_lsbAsL_o2CSuhUhJIiW0IkdT5C2wGWj)
stopped at https://www.youtube.com/watch?v=KaAJtI1T2x4&list=PL_lsbAsL_o2CSuhUhJIiW0IkdT5C2wGWj&index=6&t=360

also check:
https://docs.pytorch.org/tutorials/recipes/distributed_device_mesh.html?highlight=devicemesh
https://docs.pytorch.org/docs/stable/distributed.elastic.html
https://docs.pytorch.org/docs/stable/notes/fsdp.html
https://docs.pytorch.org/docs/stable/distributed.fsdp.fully_shard.html


[All distributed tutorials (DDP, FSDP, TP, PP)](https://docs.pytorch.org/tutorials/distributed.html)


## Other

checking which parameter is being unused:

First way:

```py
DistributedDataParallel(model, find_unused_parameters=True, static_graph=True)
```

Second way (single-GPU only):

```py
loss.backward()
for name, p in model.named_parameters():
  if p.grad is None: # Only works if using zero_grad with set grads to none
    print("unused:", name)
```

Then you can add the param with zero weight to the loss function just to consider it when doing backward pass:

```
loss = loss + 0 * param
```
