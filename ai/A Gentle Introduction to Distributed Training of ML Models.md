A Gentle Introduction to Distributed Training of ML Models
Discussion of various approaches for Distributed Training
Rachit Tayal

Apr 21, 2023

Distributed training is the process of training ML models across multiple machines or devices, with the goal of speeding up the training process and enabling the training of larger models on larger datasets.

In this article, we are going to cover high-level approaches for distributed training and will deep dive into one of the extensively applied approaches.

There are several approaches to distributed training, which can be broadly classified into two categories: data parallelism and model parallelism

Model parallelism involves splitting the model itself across multiple machines, and training different parts of the model on different machines. This approach is useful when the model is too large to fit in the memory of a single machine, or when certain parts of the model require more computation than others. Model parallelism is a bit more complex to implement and is less common than data parallelism, but is still used in some specialized applications.

Model Parallelism in Distributed Training
Data parallelism involves splitting the training data across multiple machines and training a copy of the model on each machine using its own portion of the data. The models are then synchronized periodically to ensure that they all have the same weights. This approach works well when the models are large and the training data is plentiful, as it allows for efficient use of computing resources. In this article, we are going to focus on data parallelism in depth and see an example code of how we can perform that using Pytorch.

Data Parallelism in Distributed Training
In data parallelism, the training data is split across multiple machines, and each machine trains a copy of the model using its own portion of the data. After each training step, the model weights are synchronized across all the machines, typically using a technique called gradient averaging. Here’s how the weight update process works:

Each machine computes the gradients of the model weights with respect to its own portion of the training data.
The gradients from all the machines are averaged to produce a single set of gradient values.
The model weights are updated using the averaged gradient values, as in standard stochastic gradient descent.
The updated weights are then broadcast to all the machines so that they can continue training on the next batch of data.
This process is repeated for a specified number of training steps or until convergence is reached.

It’s worth noting that there are different ways to implement data parallelism in distributed training, and the specific details of how weights are updated may vary depending on the framework and algorithm used. However, the basic idea of gradient averaging to synchronize model weights across machines remains a common approach.

Let’s look at an example source code in Pytorch to implement the data parallelism approach:

```
import torch
import torch.nn as nn
import torch.optim as optim
import torch.distributed as dist
import torch.multiprocessing as mp
from torch.nn.parallel import DistributedDataParallel as DDP

def run(rank, size):
    # Set up the distributed environment
    dist.init_process_group(backend='nccl', init_method='tcp://127.0.0.1:8000', rank=rank, world_size=size)
    
    # Set up the model and optimizer
    model = nn.Linear(10, 1)
    model = DDP(model, device_ids=[rank])
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    
    # Set up the data loader (in this example, we use random data)
    dataset = torch.randn(1000, 10)
    sampler = torch.utils.data.distributed.DistributedSampler(dataset, num_replicas=size, rank=rank)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=4, sampler=sampler)
    
    # Train the model for multiple epochs
    for epoch in range(10):
        for i, data in enumerate(dataloader):
            inputs, targets = data
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = nn.functional.mse_loss(outputs, targets)
            loss.backward()
            optimizer.step()
            
            # Synchronize the model weights
            for param in model.parameters():
                dist.all_reduce(param.grad.data, op=dist.reduce_op.SUM)
                param.grad.data /= size
        
        print('Rank', rank, 'completed epoch', epoch)
        
    dist.destroy_process_group()

if __name__ == '__main__':
    # Set up the multiprocessing environment
    mp.spawn(run, args=(4, ), nprocs=4, join=True)
```

In this example, we use PyTorch’s DistributedDataParallel module to distribute the model across multiple machines, and PyTorch's torch.distributed module to synchronize the model weights.

We first initialize the distributed environment using dist.init_process_group, which sets up the communication backend and assigns a unique rank to each machine. We then set up the model, optimizer, and data loader, and wrap the model in DistributedDataParallel to distribute it across the machines.

During training, we loop over the data loader and perform a forward pass, backward pass, and optimization step for each batch. We then synchronize the model weights using dist.all_reduce, which performs an all-reduce operation across all the machines to compute the average gradients. We divide the gradients by the number of machines to compute the average gradient, which ensures that all the machines have the same gradient.

Finally, we loop over multiple epochs and print the completion status after each epoch. We use mp.spawn to start multiple processes, each with a unique rank, and pass the run function as the target function to be executed in each process.

In conclusion, distributed training is a powerful technique for accelerating the training of machine learning models on large datasets. By dividing the data and model across multiple machines or devices, distributed training allows for faster training times and the ability to scale to larger datasets and more complex models.

PyTorch provides a convenient interface for implementing distributed training using data parallelism, with modules such as DistributedDataParallel and torch.distributed.
