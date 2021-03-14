import torch
import numpy as np
import coremltools as ct
from coremltools.converters.mil import Builder as mb
from coremltools.converters.mil import register_torch_op
from coremltools.converters.mil.frontend.torch.ops import _get_inputs

model = torch.load('lstm_pretrained.pt')
model.eval()
model = model.double()

# Trace with random data
example_input = torch.rand(2000, 100, 1, dtype=torch.float64)
traced_model = torch.jit.trace(model, example_input)


@register_torch_op
def type_as(context, node):
    inputs = _get_inputs(context, node)
    context.add(mb.cast(x=inputs[0], dtype='fp32'), node.name)


# Convert to Core ML using the Unified Conversion API
model = ct.convert(
    traced_model,
    inputs=[ct.TensorType(name="input_1", shape=example_input.shape,
                          dtype=np.float32)]
)

# Save model
model.save("lstm_pretrained.mlmodel")
