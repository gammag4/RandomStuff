import torch
import torch.nn as nn


def wrap_output_none(x):
    return x


def wrap_output_tuple(x):
    return (x,)


def wrap_output_dict(item_id):
    return lambda x: {item_id: x}


class FromFunction(nn.Module):
    def __init__(self, function, wrap_output=wrap_output_none, *extra_args, **extra_kwargs):
        super().__init__()

        self.function = function
        self.wrap_output = wrap_output
        self.extra_args = extra_args
        self.extra_kwargs = extra_kwargs

    def forward(self, *args, **kwargs):
        args = (*args, *self.extra_args)
        kwargs = {**kwargs, **self.extra_kwargs}

        res = self.function(*args, **kwargs)
        return self.wrap_output(res)


class Parallel(nn.Module):
    def __init__(self, layers, num_args: tuple[int], num_kwargs: tuple[int]):
        super().__init__()

        self.layers = layers
        self.total_num_args = sum(num_args)
        self.total_num_kwargs = sum(num_kwargs)

    def forward(self, *args, **kwargs):
        ...


def f(*args, **kwargs):
    print(args, kwargs)


a = FromFunction(f, 1, 2, 3, a=4, b=5)
a.forward(4, 5, b=7, c=3, d=5)
