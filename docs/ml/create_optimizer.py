def create_optimizer(model, weight_decay, learning_rate, betas):
  decay_params, nodecay_params = [], []
  for name, param in model.named_parameters():
    if not param.requires_grad:
      continue
    if param.dim() == 1 or name.endswith('.bias') or getattr(param, '_no_weight_decay', False):
      nodecay_params.append(param)
    else:
      decay_params.append(param)
  optim_groups = [
      {'params': decay_params, 'weight_decay': weight_decay},
      {'params': nodecay_params, 'weight_decay': 0.0}
  ]
  optimizer = torch.optim.AdamW(
      optim_groups,
      lr=learning_rate,
      betas=betas,
      fused=True  # TODO Some places report issues so check if this gives errors or nans
  )
  return optimizer
