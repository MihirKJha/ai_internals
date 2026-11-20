"""
Artificial neuron implementation using PyTorch.

This module implements a single artificial neuron from first principles,
including trainable weights, bias, and configurable activation functions.

Mathematical model:

    z = sum(x_i * w_i) + b
    y = f(z)

where:
    x_i : input features
    w_i : learnable weights
    b   : learnable bias
    f   : activation function
    y   : neuron output
"""

import torch
import torch.nn as nn

# Maps activation function names to their corresponding PyTorch functions.
ACTIVATION_FUNCTIONS = {
    "sigmoid": torch.sigmoid,
    "relu": torch.relu,
    "tanh": torch.tanh,
}


class ArtificialNeuron(nn.Module):
    """A single artificial neuron with learnable weights and bias."""

    def __init__(self, input_size: int, activation_function: str = "sigmoid") -> None:
        """
        Initialize the artificial neuron.

        Args:
            input_size (int):
                Number of input features received by the neuron.

            activation_function (str):
                Activation function applied to the weighted sum.
                Supported functions are sigmoid, relu, and tanh.

        Raises:
            ValueError:
                If the requested activation function is unsupported.
        """

        # Validate the input_size during initialization
        if (
            not isinstance(input_size, int)
            or isinstance(input_size, bool)
            or input_size <= 0
        ):
            raise ValueError("input_size must be a positive integer")

        super().__init__()
        self.input_size = input_size

        # Initialize one learnable weight for each input feature.
        self.weights = nn.Parameter(torch.randn(input_size))

        # Initialize the learnable bias to zero.
        self.bias = nn.Parameter(torch.zeros(()))

        # Validate the activation configuration during initialization
        if activation_function not in ACTIVATION_FUNCTIONS:
            raise ValueError(
                f"Unsupported activation function '{activation_function}'. "
                f"Supported activations: {list(ACTIVATION_FUNCTIONS.keys())}"
            )

        # Resolve the activation name to its callable PyTorch function.
        self.activation_fn = ACTIVATION_FUNCTIONS[activation_function]

    def forward(self, x):
        """
        Perform the forward computation of the artificial neuron.

        The neuron first calculates the weighted sum of its inputs
        and adds the bias. It then applies the selected activation
        function to produce the final output.

        Mathematical operations:

            z = x . w + b
            y = f(z)

        Args:
            x (torch.Tensor):
                Input tensor.

                Supported shapes:
                    (input_size,)              Single input sample
                    (batch_size, input_size)  Batch of input samples

        Returns:
            torch.Tensor:
                Activated neuron output.

                Expected shapes:
                    ()          Single sample
                    (batch_size,) Batch of samples
        """

          if not isinstance(x, torch.Tensor):
            raise TypeError("Input must be a torch.Tensor")

        if not x.is_floating_point():
            raise TypeError("Input tensor must have a floating-point dtype")

        if x.ndim not in (1, 2):
            raise ValueError("Input must be 1D or 2D")

        if x.shape[-1] != self.input_size:
            raise ValueError(
                f"Expected input features of size {self.input_size}, "
                f"but received {x.shape[-1]}"
            )
        
        output = torch.matmul(x, self.weights) + self.bias

        # Apply the configured activation function to the weighted sum.
        return self.activation_fn(output)
