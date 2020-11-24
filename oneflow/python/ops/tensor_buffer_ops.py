"""
Copyright 2020 The OneFlow Authors. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import absolute_import

import functools
import operator

import oneflow as flow
import oneflow.python.framework.dtype as dtype_util
import oneflow.python.framework.id_util as id_util
import oneflow.python.framework.remote_blob as remote_blob_util
from oneflow.python.oneflow_export import oneflow_export
from typing import Optional, Sequence


@oneflow_export("tensor_buffer_to_tensor")
def tensor_buffer_to_tensor(
    x: remote_blob_util.BlobDef,
    dtype: dtype_util.dtype,
    instance_shape: Sequence[int],
    name: Optional[str] = None,
) -> remote_blob_util.BlobDef:
    r"""This operator converts the Blob's type from TensorBuffer to Tensor. 
    Some operator's output data type is `TensorBuffer`, you can use this operator to convert back
    to `Tensor`. 

    Refer to `Concept Explanation <https://docs.oneflow.org/basics_topics/concept_explanation.html#3tensorbuffer-tensorlist>`_ 
    for more about TensorBuffer. 


    Args:
        x (BlobDef): Input `Blob`.
        dtype (dtype_util.dtype): The data dtype.
        instance_shape (Sequence[int]): The shape of each TensorBuffer instance.
        name (Optional[str], optional): The name for the operation. Defaults to None.

    Returns:
        BlobDef: A `Blob`.

    For example: 

    .. code-block:: python 

        import oneflow as flow
        import numpy as np
        import oneflow.typing as tp


        @flow.global_function()
        def tensor_buffer_to_tensor_Job(x: tp.Numpy.Placeholder(shape=(4, 16, 64, 64), dtype=flow.float32),
        ) -> tp.Numpy:
            x = flow.tensor_to_tensor_buffer(x, 
                                            instance_dims=2)
            return flow.tensor_buffer_to_tensor(x, 
                                                instance_shape=(64, 64), 
                                                dtype=flow.float)

        x = np.random.randn(4, 16, 64, 64).astype(np.float32)
        out = tensor_buffer_to_tensor_Job(x)

        # out.shape (4, 16, 64, 64)

    """
    if name is None:
        name = id_util.UniqueStr("TensorBufferToTensor_")
    return (
        flow.user_op_builder(name)
        .Op("tensor_buffer_to_tensor")
        .Input("in", [x])
        .Output("out")
        .Attr("dtype", dtype)
        .Attr("instance_shape", instance_shape)
        .Build()
        .InferAndTryRun()
        .RemoteBlobList()[0]
    )


@oneflow_export("tensor_to_tensor_buffer")
def tensor_to_tensor_buffer(
    x: remote_blob_util.BlobDef, instance_dims: int, name: Optional[str] = None,
) -> remote_blob_util.BlobDef:
    r"""This operator converts the Blob's type from Tensor to TensorBuffer. 

    Refer to `Concept Explanation <https://docs.oneflow.org/basics_topics/concept_explanation.html#3tensorbuffer-tensorlist>`_ 
    for more about TensorBuffer. 


    Args:
        x (BlobDef): Input `Blob`.
        instance_dims (int): The dimensions of dynamic tensor instance. 
        name (Optional[str], optional): The name for the operation. Defaults to None.

    Returns:
        BlobDef: The result Blob. 

    For example: 

    .. code-block:: python 

        import oneflow as flow
        import numpy as np
        import oneflow.typing as tp


        @flow.global_function()
        def tensor_buffer_to_tensor_Job(x: tp.Numpy.Placeholder(shape=(4, 16, 64, 64), dtype=flow.float32),
        ) -> tp.Numpy:
            x = flow.tensor_to_tensor_buffer(x, 
                                            instance_dims=2)
            return flow.tensor_buffer_to_tensor(x, 
                                                instance_shape=(64, 64), 
                                                dtype=flow.float)

        x = np.random.randn(4, 16, 64, 64).astype(np.float32)
        out = tensor_buffer_to_tensor_Job(x)

        # out.shape (4, 16, 64, 64)

    """
    if name is None:
        name = id_util.UniqueStr("TensorToTensorBuffer_")
    return (
        flow.user_op_builder(name)
        .Op("tensor_to_tensor_buffer")
        .Input("in", [x])
        .Output("out")
        .Attr("instance_dims", instance_dims)
        .Build()
        .InferAndTryRun()
        .RemoteBlobList()[0]
    )


@oneflow_export("gen_tensor_buffer")
def gen_tensor_buffer(
    shape: Sequence[int],
    shape_list: Sequence[Sequence[int]],
    value_list: Sequence[float],
    name: Optional[str] = None,
) -> remote_blob_util.BlobDef:
    r"""This operator generates a tensor buffer blob.

    Refer to `Concept Explanation <https://docs.oneflow.org/basics_topics/concept_explanation.html#3tensorbuffer-tensorlist>`_ 
    for more about TensorBuffer. 

    Args:
        shape (Sequence[int]): shape of output blob
        shape_list ( Sequence[Sequence[int]]): shapes for tensor buffer in output blob
        value_list (Sequence[float]): values for tensor buffer in output blob
        name (Optional[str]): The name for the operation. Defaults to None.

    Returns:
        BlobDef: The result Blob. 

    For example: 

    .. code-block:: python 

        import oneflow as flow

        @flow.global_function(function_config=func_config)
        def GenTensorBufferJob():
            with flow.scope.placement("cpu", "0:0"):
                x = flow.gen_tensor_buffer([(2,)], [(2, 1), (1, 2)], [0.0, 1.0])
                y = flow.tensor_buffer_to_list_of_tensors(x, (100, 100), flow.float, True)
                return y
                
        # y_0.shape (2, 1), y_1.shape (1. 2)
    """
    return (
        flow.user_op_builder(
            name if name is not None else id_util.UniqueStr("GenTensorBuffer_")
        )
        .Op("gen_tensor_buffer")
        .Output("out")
        .Attr("shape", shape)
        .Attr("shape_list", shape_list)
        .Attr("value_list", value_list)
        .Build()
        .InferAndTryRun()
        .RemoteBlobList()[0]
    )


@oneflow_export("tensor_buffer_to_list_of_tensors")
def tensor_buffer_to_list_of_tensors(
    x: remote_blob_util.BlobDef,
    out_shape: Sequence[int],
    out_dtype: dtype_util.dtype,
    dynamic_out: Optional[bool] = False,
    name: Optional[str] = None,
) -> remote_blob_util.BlobDef:
    r"""This operator converts the Blob's type from TensorBuffer to list of Tensors. Every element in x will be convert 
    to a Tensor and output will be flatten to a list.

    Refer to `Concept Explanation <https://docs.oneflow.org/basics_topics/concept_explanation.html#3tensorbuffer-tensorlist>`_ 
    for more about TensorBuffer. 


    Args:
        x (BlobDef): Input `Blob`.
        out_shape (Sequence[int]): max shape for a tensor buffer in x
        out_dtype (type_util.dtype,): output data type
        dynamic_out (Optioinal[bool]): if output is dynamic blob. Default to False.
        name (Optional[str]): The name for the operation. Defaults to None.

    Returns:
        BlobDef: The result Blob. 

    For example: 

    .. code-block:: python 
        # the same with `gen_tensor_buffer` op
    """
    return (
        flow.user_op_builder(
            name
            if name is not None
            else id_util.UniqueStr("TensorBufferToListOfTensors_")
        )
        .Op("tensor_buffer_to_list_of_tensors")
        .Input("in", [x])
        .Output("out", functools.reduce(operator.mul, x.shape, 1))
        .Attr("out_dtype", out_dtype)
        .Attr("out_shape", out_shape)
        .Attr("dynamic_out", dynamic_out)
        .Build()
        .InferAndTryRun()
        .RemoteBlobList()
    )
