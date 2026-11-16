# Understand the training system: precision, memory, parallelism, and recovery

Source: https://ml-biomat.com/tutorials/machine-learning/m26/en/
Language: en

Locate time and memory costs before distributing a correct training objective across more resources.

## When training is slow, find out who is waiting

A restaurant may not serve meals faster simply by hiring more cooks. Ingredients might still need preparation, every stove might be occupied, or the packing station might be unable to keep up. Neural-network training has a similar division of work. Data must be read, decoded, and batched; a model performs forward and backward computations; an optimizer updates parameters; and multiple devices exchange information. Training systems coordinate these activities. Their design determines how many experiments fit into the available research time and whether a model can fit into memory and train reliably at all.

Hardware constraints have also influenced model design. D2L discusses how the original AlexNet divided computation when GPU memory was limited. Data parallelism later became a common starting point for scaling training. The 2020 PyTorch Distributed paper examines gradient bucketing and overlapping communication with computation: mathematically identical gradient averaging can produce different waiting times when scheduled differently. Increasing scale therefore involves more than adding parameters. It requires decisions about data flow, storage ownership, and communication timing. Understanding those decisions helps identify the actual contribution of a proposed optimization.

$$
\mathcal T=\frac{n}{t},\qquad S_k=\frac{t_1}{t_k},\qquad \eta_k=\frac{S_k}{k}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a6949af36f16986b61ff8e11.svg) | Throughput, processed examples, and elapsed time; units examples/s, examples, and seconds. |
| ![Formula](https://ml-biomat.com/static/agent-math/2ffd5956fec03f6c157ead5e.svg) | k is device count; t1 and tk are seconds for the same workload on one and k devices. |
| ![Formula](https://ml-biomat.com/static/agent-math/9e5bf4c99d933c2bd4d88b49.svg) | Speedup and parallel efficiency, both dimensionless. |

Processing 960 examples in two seconds gives 480 examples/s. If the same workload takes four seconds on one device and 1.5 seconds on four, speedup is 2.67 and efficiency 0.667. Keeping only local batch size fixed changes the global workload.

Throughput measures completed examples per unit time, while latency measures the wait for a request or an update. Larger batches can improve throughput while making individual examples wait longer. A speed comparison should specify batch size, optimizer updates, numerical precision, model, and hardware. GPU execution is asynchronous: the CPU may finish submitting work before the device finishes computing it, requiring synchronization or device events for meaningful timing. Compilation, initial allocation, and cache warm-up also belong to a different measurement phase from steady execution.

![Actual CPU profiling and separate timing. Top: three warmed-up Adam steps with profiler ranges. Lower left: operator self CPU time. Lower right: 12 groups of five complete SGD updates, with median lines. Different optimizers and instrumentation mean the range durations are not the timing benchmark.](https://ml-biomat.com/static/tutorials/machine-learning/figures/1b668f3726f618806cd95385.svg?v=1b668f3726f6)

Figure 1Actual CPU profiling and separate timing. Top: three warmed-up Adam steps with profiler ranges. Lower left: operator self CPU time. Lower right: 12 groups of five complete SGD updates, with median lines. Different optimizers and instrumentation mean the range durations are not the timing benchmark.

This chapter runs a 54,147-parameter network on CPU. The upper figure uses profiler ranges from three real training steps to separate forward computation, loss, backward computation, and Adam updates. The lower-right panel independently times complete SGD updates in twelve groups of five. Profiling introduces overhead, and the two measurements use different optimizers, so their durations should not be combined. The aim is to establish an understandable cost breakdown before asking whether a change in precision, storage, or parallel execution preserves the intended computation.

## Deliver data before the computation needs it

A single request for the next training batch can hide several operations. Images need file reading, decompression, cropping, and tensor conversion; text needs tokenization and padding; tables may require string parsing and type conversion. Faster matrix multiplication will not remove waiting if these operations take longer than model computation. A Dataset defines how examples are obtained, while a DataLoader organizes sampling, batching, and optional worker processes. Keeping those responsibilities distinct makes it easier to measure data preparation separately from computation and to decide which stage should change.

Batching reduces repeated scheduling and gives a matrix operation more examples to process at once. Variable-length sequences create another cost: placing a length-20 sentence alongside a length-2,000 document may devote most padded positions to no useful work. Length grouping, masks, or batches defined by valid-token count can control that workload. The loss must then use a matching denominator. Two devices with eight documents each may contain very different numbers of valid tokens, so averaging their local document-level or token-level losses expresses different objectives. Data layout and mathematical reduction are connected decisions.

Caching suits expensive results that remain unchanged, such as deterministic decoding or fixed tokenization. Caching the first randomly cropped and augmented image would also freeze the intended variation in later epochs. Normalization statistics must likewise be fitted using training data. Additional loader workers can prepare examples ahead of time but introduce startup, copying, and scheduling overhead; tiny in-memory datasets may not benefit. With GPUs, pinned host memory and appropriate asynchronous transfers can overlap movement with computation. Their benefit should be visible in the actual transfer sizes and timeline rather than inferred from the option names.

The program stores the same 768 by 32 numeric array as CSV and NPY, times warmed-up full-array reading, and separately times copying 96 cached rows. Comparing CSV with NPY exposes parsing and binary-reading costs. The cache operation represents batch access after preparation is already complete. Its smaller workload is stated explicitly, so it is not interpreted as a file-format speedup. For a small dataset, moving deterministic preparation outside the training loop often creates a clearer intervention than adding worker processes whose startup and communication costs dominate the work.

## Split a batch without changing its objective

If a large batch does not fit into memory, process part of it at a time, accumulate gradients, and update parameters once. Distinguish the number of backward passes from the number of optimizer updates. Calling optimizer.step after every microbatch changes parameters before subsequent microbatches are evaluated. Gradient accumulation instead differentiates every microbatch at the same parameter values. Clear gradients at the beginning of the effective batch, add contributions during its microbatches, and update after all contributions arrive. This sequence reproduces the desired average when the objective decomposes over examples.

$$
B_{\rm eff}=RKA,\qquad \nabla_\theta L=\sum_{j=1}^{m}\frac{n_j}{N}\nabla_\theta L_j,\quad N=\sum_{j=1}^{m}n_j
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a3576044580388006267924f.svg) | Effective examples per update, number of data-parallel replicas, examples per replica microbatch, and accumulation count; dimensionless counts. |
| ![Formula](https://ml-biomat.com/static/agent-math/cfa030f8ff794ca3a6b386c6.svg) | j indexes microbatches, m is their count, nj their individual sizes, and N the total. |
| ![Formula](https://ml-biomat.com/static/agent-math/eed48cd34399b8bb5c47bae6.svg) | Theta contains model parameters; L and Lj are full and microbatch mean losses, differentiated with respect to the same parameters. Cross-entropy and parameters are dimensionless here. |

Four replicas with eight examples per microbatch and three accumulation steps use 96 examples per update. Splitting 96 into 17,31,48 requires weights 17/96,31/96,48/96. An unweighted average of the three means overweights examples in the smaller batches.

The experiment starts from identical parameters and computes a mean cross-entropy gradient over 96 examples. It then repeats the calculation using microbatches of 17, 31, and 48 examples. The correct implementation sums each microbatch loss and divides by 96 before backpropagation. An intentionally incorrect comparison averages the three microbatch means equally. Correct accumulation differs from the full-batch gradient by approximately 7.45×10⁻⁹, reflecting floating-point summation order; the incorrect version differs by 0.01188 because example weights changed. Calling both operations an average does not make their denominators equivalent.

The equivalence also depends on the computation decomposing over examples. BatchNorm uses the current batch statistics, so smaller batches change its forward outputs. Cross-example contrastive losses change when the available negative set changes. Random operations such as Dropout introduce another correspondence to consider. The equivalence experiment therefore disables Dropout and uses a network without BatchNorm, isolating the sample-mean objective and its reduction. A separate recovery experiment activates Dropout to test saved random state. Each experiment answers a specific question rather than mixing numerical and sampling differences.

Accumulation combines with data parallelism. Four replicas processing eight examples each for three accumulation steps use an effective batch of 96. Incomplete local batches should be weighted using actual example or valid-token counts. DDP’s no_sync can avoid intermediate gradient synchronization and synchronize on the final accumulation step; the corresponding forward computation belongs inside that context as well. Learning-rate schedules and reported step counts should specify whether they count microbatches or optimizer updates. Otherwise, identical-looking configurations can advance their schedules on different timescales.

## Store fewer bits, or recompute intermediate values

A floating-point format has a limited number of bits and must balance representable range against spacing between nearby values. FP16 and BF16 both use sixteen bits but allocate them differently. BF16 has an exponent range close to FP32 and a shorter significand; FP16 generally resolves nearby values more finely at similar magnitudes but is more exposed to small-gradient underflow and large-value overflow. The real conversions in the figure make this distinction concrete. Casting 1e−8 to FP16 yields zero, while BF16 preserves an approximation; casting 1.001 to BF16 can round it to exactly one.

$$
\tilde L=sL,\qquad \tilde g=\nabla_\theta\tilde L=sg,\qquad g=\tilde g/s
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/0e3d81b121b61d9889e7e249.svg) | Original and scaled loss and positive scale s; s is dimensionless and may be adapted during training. |
| ![Formula](https://ml-biomat.com/static/agent-math/7a28a623c4c68e362e8f21c5.svg) | Parameters, original gradient, and scaled gradient, with matching shapes. Unscale before updating or clipping in the original gradient scale. |

Casting 1e−8 directly to FP16 gives zero. Multiplying by 65,536 first, casting, then dividing in FP32 recovers approximately 9.99717e−9. Scaling preserves small gradients; overflow requires reducing the scale and skipping the invalid update.

Automatic mixed precision does not simply convert the entire model to a half-precision file. Autocast selects types by operation, allowing suitable matrix computations to use lower precision while some reductions and losses retain more stable types. FP16 training often scales the loss before differentiation and unscales gradients afterward; clipping should use the unscaled gradient. The CPU BF16 example uses autocast without a scaler. Our program places the forward pass and loss inside the CPU autocast context, performs backward outside it, and observes a maximum gradient difference of approximately 0.000817 relative to FP32.

On this CPU and these small matrices, the median BF16 update takes approximately 10.48 ms, compared with 0.60 ms for FP32 and 1.19 ms with recomputation. Lower precision is slower in this measured configuration. Instruction support, kernel implementations, matrix dimensions, and conversion overhead jointly determine performance. These numbers describe one run and vary with system load. The gradient comparison answers a separate numerical question: how much did the computation change? Effects on learning should be evaluated using the same data partitions and training objective rather than inferred from a faster or smaller representation.

![Left: unique non-parameter backing storage retained for backward after forward, including full input storage retained by a slice; this is not process peak memory. Upper right compares gradients except the DDP row, which compares parameters after SGD. Lower right shows real type conversions. All checks use the same 96 examples and parameter initialization.](https://ml-biomat.com/static/tutorials/machine-learning/figures/b8d5b08c1823885c1eafabde.svg?v=b8d5b08c1823)

Figure 2Left: unique non-parameter backing storage retained for backward after forward, including full input storage retained by a slice; this is not process peak memory. Upper right compares gradients except the DDP row, which compares parameters after SGD. Lower right shows real type conversions. All checks use the same 96 examples and parameter initialization.

Activation checkpointing changes what forward computation retains for backward. Ordinary execution stores intermediate tensors; checkpointing keeps required inputs and recreates intermediate values when backward reaches that region. It exchanges extra computation for less retained storage. Wrapping the four-layer feature network in a non-reentrant checkpoint gives zero gradient difference in this example and reduces retained non-parameter backing storage from 302,212 to 154,756 bytes. The inventory deduplicates storage addresses and includes the complete underlying input array retained by a slice. It describes storage retained after forward, while peak memory, communication buffers, and optimizer state require separate measurements.

## Data parallelism computes locally and updates together

Data parallelism places a complete model replica on every device and gives each replica different examples. Local gradients are aggregated, then every replica applies the same global gradient using matching optimizer state. The models consequently remain aligned. This resembles dividing a survey between several people and combining totals and counts to calculate a common mean. Establish which quantities are summed and where division occurs before memorizing a distributed API. Incorrect reduction can change the objective even when the program successfully communicates and every device remains busy.

$$
g=\frac1R\sum_{r=1}^{R}g_r,\qquad \theta_{\rm new}=\theta-\lambda g
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/50ec721002628c3a35b08389.svg) | R counts equal-batch replicas, r indexes them, gr is a local mean gradient, and g the global mean, with the same vector shape as theta. |
| ![Formula](https://ml-biomat.com/static/agent-math/70b0887f0d88757fc638b64a.svg) | Parameter vectors before and after the update; lambda is learning rate, 0.05 in the SGD experiment and 0.1 in the interactive example, for a dimensionless model. |

Gradients [1,3] and [3,1] sum to [4,4] and average to [2,2]. With theta=[1,1] and rate 0.1, both replicas update to [0.8,0.8]. Matching parameter initialization, aggregated gradients, and optimizer state keeps replicas aligned.

![Original teaching diagram of two-GPU data splitting, local gradients, aggregation, and updates.](https://ml-biomat.com/static/tutorials/machine-learning/figures/352f8a76a448da8309835eb4.svg?v=352f8a76a448)

Figure 3D2L figure 13.5.3: local gradients on two GPUs are aggregated before synchronized updates. Unmodified original from Dive into Deep Learning, Training on Multiple GPUs, CC BY-SA 4.0. The original hardware illustrates data flow; this chapter runs two CPU processes.

The program actually starts two local CPU processes and creates a Gloo process group, with 48 examples per process. DDP synchronizes local mean gradients during backward, and both replicas perform one SGD update with learning rate 0.05. Their final parameters agree exactly and differ from the single-process 96-example update by approximately 7.45×10⁻⁹. An additional integer-vector all-reduce sums [1,1] and [2,3], returning [3,4] to both processes as an independently checkable communication example. The experiment verifies synchronization and update semantics; its CPU processes are not a measurement of two-GPU throughput.

DDP synchronizes the initial model state and organizes gradients into buckets. As backward computes gradients, a completed bucket can begin communicating while other layers continue computing. Very large buckets may delay that overlap; very small ones increase communication startup frequency. All processes must participate in collective operations in compatible order. If one exits early, skips a branch, or encounters an unhandled exception, others may wait indefinitely. Distributed stalls therefore often involve execution paths, data counts, and collective ordering as well as hardware performance.

Sampling also needs explicit partitioning. Replicas traversing identical examples merely duplicate work. A distributed sampler assigns examples to processes and needs its shuffle state advanced across epochs. Padding a validation sampler by repeating records can distort metrics if repeated examples are counted as new observations. DDP handles replica synchronization, while data partitions, effective loss denominators, and evaluation statistics remain responsibilities of the training program. Checking one small batch with a known reference update makes discrepancies between those responsibilities much easier to diagnose before the workload grows.

## Which training state must each device keep?

Weights are only part of training storage. A parameter may also have a gradient, Adam first and second moments, and an FP32 master copy used for updates. Activations, temporary workspaces, and communication buffers add more. Data parallelism replicates complete state, so adding devices does not automatically shrink the individual model. ZeRO addresses the redundant copies by progressively partitioning optimizer state, gradients, and finally parameters. The devices then own different portions of state instead of each storing every persistent tensor.

$$
M_{\rm DDP}=P(b_w+b_g+b_o),\quad M_1=P(b_w+b_g+b_o/R),\quad M_2=P(b_w+b_g/R+b_o/R),\quad M_3=P(b_w+b_g+b_o)/R
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/6c04a51457034e5d812d0a8f.svg) | P is parameter count and R sharding-device count; both are dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/7faaeb05f8055dcd7d9fc9c5.svg) | Bytes per parameter for weights, gradients, and master weights plus optimizer state: 2,2,12 here, with 12=4 for master weights plus two 4-byte Adam moments. |
| ![Formula](https://ml-biomat.com/static/agent-math/392337d6f3490ca179980f20.svg) | Persistent bytes per device for replication and ZeRO stages 1,2,3; activations, temporary full parameters, communication buffers, and allocator overhead are separate. |

For 100 million parameters on four devices, DDP requires 1.6 GB and the three stages 0.7,0.55,0.4 GB, where GB means 10⁹ bytes. Determine actual gradient and master-weight policies before choosing the byte counts.

A byte budget begins with implementation assumptions. The illustrated example uses two-byte weights, two-byte gradients, a four-byte master weight, and eight bytes for two Adam moments: sixteen bytes per parameter. For 100 million parameters across four devices, full replication takes 1.6 GB per device; progressive sharding gives 0.7, 0.55, and 0.4 GB. This is an analytical persistent-state budget. FP32 gradients, the absence of a separate master copy, or a different optimizer change the inputs to that calculation. Sixteen bytes per parameter is a specified configuration, not a universal property of training.

FSDP connects sharded state to model execution. Before a module computes, all-gather materializes the parameters that the module needs. Backward produces local gradients, and reduce-scatter aggregates them while distributing portions to the devices responsible for their updates. Each optimizer manages its local shard. Parameters are gathered again when later computation needs them. Sharding reduces persistent storage but introduces communication and temporary full parameters. Prefetching a subsequent module can hide waiting while increasing concurrent residency. Module granularity therefore affects communication frequency, peak storage, and available overlap.

The interactive example combines a small gradient calculation with the persistent-state budget. Each process’s local gradient follows an explicit formula; stepping through the calculation exposes local values, their mean, and updated weights. Changing sharding stages changes the persistent state assigned to each device. These are data-flow and byte-accounting calculations, while actual temporary peaks and communication durations belong to measured execution. Identifying whether an intervention removes weight copies, optimizer copies, or retained activations helps determine whether it addresses the current memory bottleneck.

## How local gradients become a shared update

Illustrative gradients multiply the process index plus one by the parameter index plus one, then divide by ten. Initial weights are one, learning rate 0.1, and local batches are equal. A separate storage budget uses the chosen parameter count with 2-byte weights, 2-byte gradients, and 12-byte master weights plus Adam state.

[Figure: How local gradients become a shared update](https://ml-biomat.com/tutorials/machine-learning/m26/en/#M26-plot)

Manual stepping reveals computation stages. Sharding changes state ownership while preserving the mathematical update. Persistent budgets are equal across devices; activations and temporary buffers are separate.

## Partition a tensor, a sequence of layers, or a set of experts

Tensor parallelism divides a large matrix operation between devices. Splitting weight columns corresponding to output features gives each device distinct outputs that can be concatenated. Splitting the input-feature dimension produces partial sums of the same output, which must be added. That distinction determines communication. Frameworks commonly store a linear weight matrix as output-by-input, so a row or column label should be interpreted alongside the actual multiplication and storage layout. Writing the input, weight, and output shapes first prevents a storage-axis name from replacing the underlying mathematical meaning.

$$
X[W_1\ W_2]=[XW_1\ XW_2],\qquad [X_1\ X_2]\begin{bmatrix}V_1\\V_2\end{bmatrix}=X_1V_1+X_2V_2
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/5a413b9be6c9314d81d66a65.svg) | X is B by d input; W1 and W2 are d by h1 and d by h2 output-column shards. |
| ![Formula](https://ml-biomat.com/static/agent-math/3b1e83b6383456601d77026e.svg) | X1 and X2 are B by h1 and B by h2 input-feature shards; V1 and V2 are h1 by o and h2 by o weight-row shards. |
| ![Formula](https://ml-biomat.com/static/agent-math/16c8746d45b4db3ecf180d6c.svg) | B is batch size and the other dimensions are feature counts; brackets concatenate along the indicated axes and plus adds matching tensors elementwise. Values are dimensionless here. |

Input [2,3] multiplied by columns [1,4] and [5,6] gives 14 and 28, concatenated as [14,28]. A following weighted sum with coefficients 1 and 2 produces partial results 14 and 56, which must add to 70. Column sharding produces distinct outputs; row sharding produces partial sums.

Pipeline parallelism partitions the model into layer stages. A microbatch leaving stage one can enter stage two while stage one begins another microbatch. During startup, later stages have no input; during draining, earlier stages run out of work. These idle periods are pipeline bubbles. More microbatches improve ideal utilization but alter scheduling and activation-storage requirements. GPipe processes a group of forward passes before backward passes, while 1F1B alternates forward and backward work after warm-up. Different schedules change intermediate storage and waiting even when the same network and data are used.

$$
U_{\rm forward}=\frac{m}{m+p-1},\qquad V_{\rm ring}\approx 2\frac{R-1}{R}G
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/2ad69b22eb61d6cb4d522b0f.svg) | Ideal forward-pipeline utilization, microbatch count, and equal-duration stage count. U is dimensionless; the model includes one forward pass, no communication, and equal stage duration. |
| ![Formula](https://ml-biomat.com/static/agent-math/3d589cb45d7033d3fb72f837.svg) | Approximate bytes sent per process by ring all-reduce, process count, and full gradient-message bytes; excludes received bytes, protocol headers, and latency. |

Four microbatches through three equal stages require six slots, with four active slots per stage: utilization 2/3. Separately, ring all-reduce of 200 MB across four processes sends approximately 300 MB per process. This is a volume model, not a measured duration.

![Two analytical diagrams. Left: persistent-state budget for 100M parameters over four devices, assuming 2-byte weights, 2-byte gradients, and 12-byte master weights plus Adam state; activations and temporary buffers are separate. Right: ideal forward scheduling for four microbatches and three equal-duration stages, labeled by microbatch, not a measured GPU trace.](https://ml-biomat.com/static/tutorials/machine-learning/figures/afc8d7a054a0e83665d62c41.svg?v=afc8d7a054a0)

Figure 4Two analytical diagrams. Left: persistent-state budget for 100M parameters over four devices, assuming 2-byte weights, 2-byte gradients, and 12-byte master weights plus Adam state; activations and temporary buffers are separate. Right: ideal forward scheduling for four microbatches and three equal-duration stages, labeled by microbatch, not a measured GPU trace.

Four microbatches crossing three equal-duration stages require six forward slots, with each stage active for four: utilization is two-thirds. This diagram includes only forward computation and ignores communication. Complete training also includes backward, unequal stage durations, and scheduling dependencies. The ring all-reduce expression is similarly a volume model. Four processes reducing 200 MB of gradients each send approximately 300 MB, but the formula does not specify milliseconds. Bandwidth, startup latency, network topology, and overlap with computation determine how much of that communication appears on the critical path.

Expert parallelism exploits conditional computation. A router selects a small number of experts for a token and sends its representation to the devices hosting them. Results return to the original sequence positions afterward. Sparse expert systems such as Switch Transformers separate total parameter count from the parameters activated for each token. Routing introduces token movement and load-balancing concerns. If most tokens select one expert, that device becomes a bottleneck. Capacity limits, auxiliary balancing objectives, and overflow handling can affect both system efficiency and the computation actually optimized during training.

These strategies can occupy different dimensions of a device mesh. Tensor parallelism exchanges layer-level results frequently and benefits from fast communication within a group. Data parallelism or state sharding can use another dimension, with pipeline stages providing another partition. The effective batch must count data-parallel replicas rather than every device involved in a sample’s computation. If an eight-device job uses four devices together for each model-partition group, it has two data-parallel replicas. Total devices, model partitions, and independently processed batches represent different quantities, even when they all appear in the same launch configuration.

## Saving weights is different from saving a training process

A bookmark records where reading should resume; training has several kinds of bookmark. Model parameters, Adam moments, scheduler position, a mixed-precision scale, random state, and data-sampling position can all affect the next update. Weights alone are useful for inference or for beginning another training procedure. Continuing the previous trajectory requires restoring the state that determines its next step. Saving after a complete optimizer update creates a clean boundary. Saving during gradient accumulation additionally requires the accumulated gradients and current microbatch position.

The recovery experiment trains a Dropout network for twelve Adam updates and saves model, optimizer, random state, and update count after update six. One path continues uninterrupted; another constructs a fresh network, loads the complete checkpoint, and resumes from the saved random state. Their subsequent losses and final parameters agree exactly. A comparison restores weights and the same RNG but discards Adam state, isolating the effect of missing optimizer history. Its final parameter difference is approximately 0.02484 and its trajectory diverges. A lower loss on that alternative path does not change the test’s purpose: it is a different optimization process.

![Left: checkpoint after six Adam updates. Full recovery matches uninterrupted training; weights-only recovery keeps the same RNG but discards Adam state and diverges. Right: warmed-up data-operation timing. CSV and NPY read all 768 by 32 values; the cache operation copies only the current 96 rows, distinguishing full preparation from batch access.](https://ml-biomat.com/static/tutorials/machine-learning/figures/d2ba89f820e987bd8e057ca3.svg?v=d2ba89f820e9)

Figure 5Left: checkpoint after six Adam updates. Full recovery matches uninterrupted training; weights-only recovery keeps the same RNG but discards Adam state and diverges. Right: warmed-up data-operation timing. CSV and NPY read all 768 by 32 values; the cache operation copies only the current 96 rows, distinguishing full preparation from batch access.

Distributed recovery requires a consistent progress point across processes. Saved shards must belong to the same update version, and restarted models, optimizer shards, and data partitions must agree. A changed device count may require checkpoint resharding and different sampling assignments. One practical scheme writes temporary files, verifies that the required shards are complete, and only then updates a manifest identifying the completed version. Recovery selects a version through that manifest. Timeouts and failure handling should also make every participant terminate or restart coherently rather than allowing one process to proceed with stale state.

Checkpoint frequency balances costs. Frequent writes consume bandwidth and storage; long intervals increase lost work after interruption. Measuring checkpoint duration and choosing an acceptable amount of recomputation gives the interval a concrete basis. Actually saving, restarting, and comparing the next update is more informative than checking that a file exists. Activation checkpointing and persistent training checkpoints share a name but serve different purposes: the former recomputes intermediate values inside backward, while the latter stores training state for a newly started process.

## Find the same computation in PyTorch, JAX, and Keras

When changing frameworks, preserve the objective, parameter state, and data layout. Typical PyTorch code stores parameters in a Module, lets loss.backward populate their gradient fields, and asks an optimizer to update them. JAX often passes parameters into a function and uses value_and_grad to return both loss and gradients before explicitly producing a new parameter structure. Randomness is commonly represented with explicit keys. Despite these different styles, a two-example scalar model provides a common calculation for checking whether implementations use the same reduction and update rule.

$$
L(w)=\frac{(w\cdot1-2)^2+(w\cdot2-4)^2}{2},\qquad \left.\frac{dL}{dw}\right|_{w=1}=-5,\qquad w_{\rm new}=1-0.1(-5)=1.5
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/623266ad2e97a6418b22b401.svg) | Scalar linear-model weight, updated weight, and mean squared error over two examples, all dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/b215ca6388be117e2b4987b8.svg) | Inputs are 1 and 2, targets 2 and 4, learning rate 0.1; dL/dw is the derivative with respect to the weight. |

At w=1, errors are −1 and −2 and mean squared error is 2.5. Averaging twice error times input gives derivative −5. Frameworks using the same reduction, shapes, and update rule should compute the same answer.

JAX grad transforms a scalar-valued function into a gradient function; vmap maps a single-example computation over a batch; jit compiles traceable computation. The first call may compile while subsequent calls reuse executable code, so timings should distinguish these phases and wait for asynchronous results to finish. For device layout, Mesh describes the devices and PartitionSpec describes which array axes are sharded across mesh axes. An unused mesh axis may hold replicated values. Sharding a batch axis while replicating feature axes expresses a data-parallel arrangement, and changing that layout can introduce communication.

Keras provides the high-level fit interface and also permits custom train_step implementations. With a TensorFlow backend, a GradientTape records forward and loss computation, produces derivatives, and passes them to the optimizer. training=True controls training behavior in layers such as Dropout. TensorFlow’s MirroredStrategy maintains synchronous data-parallel replicas, while MultiWorkerMirroredStrategy extends the pattern across workers. Keras supports additional backends, so naming Keras alone does not specify the execution engine or distribution strategy. Comparisons should identify the backend, loss reduction, random behavior, and numerical types.

| Responsibility | PyTorch | JAX | Keras / TensorFlow |
| --- | --- | --- | --- |
| Differentiate | autograd and backward | grad / value_and_grad | GradientTape |
| Batch computation | Tensor batch axes and DataLoader | Array batch axes and vmap | tf.data and batch tensors |
| Compile | torch.compile | jit | tf.function and compilation settings |
| Device layout | DDP, FSDP, DeviceMesh | Mesh and sharding specifications | distribute.Strategy |

These correspondences identify responsibilities rather than interchangeable syntax. Changing a mean to a sum, broadcasting targets across an unintended axis, or forgetting training mode can change updates even with the same optimizer name. This chapter executes the full PyTorch experiment; the JAX and Keras/TensorFlow comparison explains their official computation and layout interfaces. A port can begin by reproducing loss 2.5, gradient −5, and updated weight 1.5 from the worked example, then add batching, compilation, and distribution. Each added feature then has a clear numerical reference.

## Verify first, measure next, then scale

The program generates 768 inputs with 32 features and assigns three labels using a fixed linear teacher with noise. The first 576 examples supply training batches, and the last 192 evaluate the model. Four hidden layers have width 128. Twelve recovery-test updates reach 133/192 correct test predictions, approximately 69.27%, confirming an actual learning process. Equivalence and two-process DDP checks instead fix the first 96 examples so sampling differences do not enter the system comparison. Each CPU process uses two threads, with library versions and device details recorded in the numeric summary.

### Complete CPU experiment: equivalent updates, two-process DDP, profiling, and recovery

Run this complete file from a terminal with --output and --language. The first run measures all experiments; add --render-only to render another language from the same measurements. Two local CPU processes perform real Gloo gradient synchronization. Outputs include profiler ranges, a stochastic training checkpoint, weights, and data.

```
"""Measure and verify CPU training: accumulation, real DDP, precision and recovery."""
import argparse
import copy
import json
import platform
import time
import uuid
from pathlib import Path
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.checkpoint import checkpoint
import torch.distributed as dist
import torch.multiprocessing as mp
from torch.nn.parallel import DistributedDataParallel
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

torch.set_num_threads(2)


class Net(nn.Module):
    def __init__(self, dropout=0.):
        super().__init__()
        self.features=nn.Sequential(nn.Linear(32,128),nn.ReLU(),nn.Dropout(dropout),
            nn.Linear(128,128),nn.ReLU(),nn.Dropout(dropout),
            nn.Linear(128,128),nn.ReLU(),nn.Dropout(dropout),
            nn.Linear(128,128),nn.ReLU())
        self.head=nn.Linear(128,3)

    def forward(self,x,recompute=False):
        hidden=checkpoint(self.features,x,use_reentrant=False) if recompute else self.features(x)
        return self.head(hidden)


def make_data():
    generator=torch.Generator().manual_seed(26)
    x=torch.randn(768,32,generator=generator)
    teacher=torch.randn(32,3,generator=generator)
    y=(x@teacher+.25*torch.randn(768,3,generator=generator)).argmax(1)
    return x,y


def new_model(dropout=0.):
    torch.manual_seed(260)
    return Net(dropout)


def flatten(model,grad=False):
    return torch.cat([(p.grad if grad else p).detach().flatten()for p in model.parameters()])


def max_error(a,b):return float((a-b).abs().max())


def gradient_experiments(x,y):
    full=new_model();F.cross_entropy(full(x[:96]),y[:96]).backward();reference=flatten(full,True)
    accumulated=new_model();wrong=new_model();offset=0
    for size in [17,31,48]:
        xb,yb=x[offset:offset+size],y[offset:offset+size]
        (F.cross_entropy(accumulated(xb),yb,reduction='sum')/96).backward()
        (F.cross_entropy(wrong(xb),yb)/3).backward();offset+=size
    bf=new_model()
    with torch.autocast('cpu',dtype=torch.bfloat16):loss=F.cross_entropy(bf(x[:96]),y[:96])
    loss.backward()
    result={'accumulation_gradient_error':max_error(reference,flatten(accumulated,True)),
        'unweighted_microbatch_error':max_error(reference,flatten(wrong,True)),
        'bf16_gradient_error':max_error(reference,flatten(bf,True))}
    opt=torch.optim.SGD(full.parameters(),lr=.05);opt.step()
    return result,flatten(full),reference


def ddp_worker(rank,init_method,output):
    torch.set_num_threads(2)
    dist.init_process_group('gloo',rank=rank,world_size=2,init_method=init_method)
    try:
        x,y=make_data();model=DistributedDataParallel(new_model())
        optimizer=torch.optim.SGD(model.parameters(),lr=.05)
        sl=slice(rank*48,(rank+1)*48)
        optimizer.zero_grad();F.cross_entropy(model(x[sl]),y[sl]).backward();optimizer.step()
        total=torch.tensor([rank+1.,2.*rank+1.]);dist.all_reduce(total)
        torch.save({'parameters':flatten(model.module),'reduction':total},Path(output)/f'ddp-rank{rank}.pt')
    finally:dist.destroy_process_group()


def retained_storage(x,y,recompute):
    model=new_model();saved={};parameter_pointers={p.untyped_storage().data_ptr()for p in model.parameters()}
    def pack(tensor):
        storage=tensor.untyped_storage();ptr=storage.data_ptr()
        if ptr not in parameter_pointers:saved[ptr]=storage.nbytes()
        return tensor
    with torch.autograd.graph.saved_tensors_hooks(pack,lambda t:t):
        loss=F.cross_entropy(model(x[:96],recompute=recompute),y[:96])
    retained=sum(saved.values());loss.backward()
    return retained,flatten(model,True)


def train_steps(model,optimizer,x,y,start,end):
    losses=[]
    for _ in range(start,end):
        index=torch.randperm(576)[:96]
        optimizer.zero_grad();loss=F.cross_entropy(model(x[index]),y[index]);loss.backward();optimizer.step();losses.append(float(loss.detach()))
    return losses


def recovery(x,y,out):
    model=new_model(.2);optimizer=torch.optim.Adam(model.parameters(),lr=.003)
    torch.manual_seed(2026)
    first=train_steps(model,optimizer,x,y,0,6)
    checkpoint_data={'model':copy.deepcopy(model.state_dict()),'optimizer':copy.deepcopy(optimizer.state_dict()),
        'rng_state':torch.get_rng_state(),'completed_updates':6,'architecture':{'inputs':32,'hidden':128,'hidden_layers':4,'outputs':3,'dropout':.2},'learning_rate':.003}
    torch.save(checkpoint_data,out/'training-checkpoint.pt')
    later=train_steps(model,optimizer,x,y,6,12);reference=flatten(model)
    saved=torch.load(out/'training-checkpoint.pt',weights_only=True)
    restored=Net(.2);restored.load_state_dict(saved['model']);restored_opt=torch.optim.Adam(restored.parameters(),lr=.003);restored_opt.load_state_dict(saved['optimizer'])
    torch.set_rng_state(saved['rng_state']);restored_loss=train_steps(restored,restored_opt,x,y,6,12)
    weights_only=Net(.2);weights_only.load_state_dict(saved['model']);fresh_opt=torch.optim.Adam(weights_only.parameters(),lr=.003)
    torch.set_rng_state(saved['rng_state']);weights_loss=train_steps(weights_only,fresh_opt,x,y,6,12)
    model.eval()
    with torch.no_grad():test_accuracy=float((model(x[576:]).argmax(1)==y[576:]).float().mean())
    torch.save(model.state_dict(),out/'trained-model.pt')
    return {'resume_parameter_error':max_error(reference,flatten(restored)),'weights_only_parameter_error':max_error(reference,flatten(weights_only)),
        'resume_loss_error':float(np.max(abs(np.array(later)-restored_loss))),'test_accuracy':test_accuracy},np.array(first+later),np.array(first+restored_loss),np.array(first+weights_loss)


def measure(function,repeats=12,inner=5):
    for _ in range(3):function()
    values=[]
    for _ in range(repeats):
        start=time.perf_counter()
        for _ in range(inner):function()
        values.append((time.perf_counter()-start)*1000/inner)
    return np.array(values)


def timings(x,y,out):
    np.savetxt(out/'features.csv',x.numpy(),delimiter=',',fmt='%.9g');np.save(out/'features.npy',x.numpy())
    paths={'Parse CSV':lambda:np.loadtxt(out/'features.csv',delimiter=',',dtype=np.float32),
           'Read NPY':lambda:np.load(out/'features.npy'),
           'Cached rows':lambda:x[:96].clone()}
    data={k:measure(fn,inner=3)for k,fn in paths.items()}
    steps={}
    for name,amp,recompute in [('FP32',False,False),('CPU BF16',True,False),('Recompute',False,True)]:
        model=new_model();optimizer=torch.optim.SGD(model.parameters(),lr=.05)
        def step():
            optimizer.zero_grad()
            with torch.autocast('cpu',dtype=torch.bfloat16,enabled=amp):loss=F.cross_entropy(model(x[:96],recompute=recompute),y[:96])
            loss.backward();optimizer.step()
        steps[name]=measure(step)
    return data,steps


def profile(x,y,out):
    model=new_model();opt=torch.optim.Adam(model.parameters(),lr=.003)
    for _ in range(3):
        opt.zero_grad();F.cross_entropy(model(x[:96]),y[:96]).backward();opt.step()
    with torch.profiler.profile(activities=[torch.profiler.ProfilerActivity.CPU],record_shapes=True) as prof:
        for _ in range(3):
            opt.zero_grad()
            with torch.profiler.record_function('forward'):prediction=model(x[:96])
            with torch.profiler.record_function('loss'):loss=F.cross_entropy(prediction,y[:96])
            with torch.profiler.record_function('backward'):loss.backward()
            with torch.profiler.record_function('optimizer'):opt.step()
    events=[{'name':e.name,'start_us':e.time_range.start,'duration_us':e.time_range.end-e.time_range.start}for e in prof.events()if e.name in ['forward','loss','backward','optimizer']]
    start=events[0]['start_us']
    for e in events:e['start_us']-=start
    operators=sorted([{'name':e.key,'self_cpu_us':e.self_cpu_time_total,'calls':e.count}for e in prof.key_averages()if e.key.startswith('aten::')],key=lambda e:e['self_cpu_us'],reverse=True)
    (out/'profile.json').write_text(json.dumps({'events':events,'operators':operators},indent=2),encoding='utf-8')
    trace=[{'name':e['name'],'cat':'training','ph':'X','ts':e['start_us'],'dur':e['duration_us'],'pid':0,'tid':0}for e in events]
    (out/'trace.json').write_text(json.dumps({'traceEvents':trace}),encoding='utf-8')
    return events,operators


def draw(out,lang,summary,data_timing,step_timing,events,operators,curves):
    zh=lang=='zh';plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
    colors=['#266d86','#dd8b38','#8a63a2','#4c9276']
    def save(fig,name):
        fig.savefig(out/f'{name}-{lang}.svg',bbox_inches='tight',facecolor='white');fig.savefig(out/f'{name}-{lang}.png',dpi=155,bbox_inches='tight',facecolor='white');plt.close(fig)
    fig=plt.figure(figsize=(12.7,8.1),layout='constrained');gs=fig.add_gridspec(2,2,height_ratios=[.85,1])
    ax=fig.add_subplot(gs[0,:]);stages=['forward','loss','backward','optimizer'];names=['前向','损失','反向','参数更新']if zh else['Forward','Loss','Backward','Optimizer']
    for j,e in enumerate(events):
        i=stages.index(e['name']);ax.broken_barh([(e['start_us']/1000,e['duration_us']/1000)],(j//4-.28,.56),facecolors=colors[i])
    for i,n in enumerate(names):ax.plot([],[],lw=7,color=colors[i],label=n)
    ax.set_yticks([0,1,2],['1','2','3']);ax.invert_yaxis();ax.set_ylabel('训练步'if zh else'Training step');ax.set_xlabel('从首个前向开始 / ms'if zh else'Time from first forward / ms');ax.legend(ncols=4,frameon=False,loc='upper center',bbox_to_anchor=(.5,1.26));ax.set_title('CPU 实际分析器范围（包含测量开销）'if zh else'Actual CPU profiler ranges (including measurement overhead)',pad=42)
    ax=fig.add_subplot(gs[1,0]);top=operators[:7];ax.barh(range(len(top)),[o['self_cpu_us']/1000 for o in top],color=colors[0]);ax.set_yticks(range(len(top)),[o['name'] for o in top]);ax.invert_yaxis();ax.set_xlabel('三步累计自身 CPU 时间 / ms'if zh else'Self CPU time across three steps / ms')
    ax=fig.add_subplot(gs[1,1]);labels=['FP32','CPU BF16','重计算'if zh else'Recompute']
    for i,(name,v)in enumerate(step_timing.items()):ax.scatter(np.full(len(v),i)+np.linspace(-.08,.08,len(v)),v,color=colors[i],s=18,alpha=.7);ax.plot([i-.2,i+.2],[np.median(v)]*2,color='#243749',lw=2)
    ax.set_xticks(range(3),labels);ax.set_ylabel('每次更新 / ms'if zh else'Milliseconds per update');ax.set_title('12组计时，每组5次更新'if zh else'12 timing groups, five updates each')
    save(fig,'profile')
    fig=plt.figure(figsize=(12.4,6.6),layout='constrained');gs=fig.add_gridspec(2,2,width_ratios=[1,1.35]);ax=fig.add_subplot(gs[:,0])
    bars=[summary['saved_storage_plain_bytes']/1024,summary['saved_storage_checkpoint_bytes']/1024]
    ax.bar([0,1],bars,color=colors[:2],width=.6);ax.set_xticks([0,1],['普通前向','激活重计算']if zh else['Normal forward','Checkpointed']);ax.set_ylabel('保留的非参数张量存储 / KiB'if zh else'Retained non-parameter storage / KiB');ax.set_title('同一96样本前向，按存储地址去重'if zh else'Same 96 examples; unique storage addresses')
    for i,v in enumerate(bars):ax.text(i,v+4,f'{v:.1f}',ha='center')
    ax.set_ylim(0,max(bars)*1.18)
    ax=fig.add_subplot(gs[0,1]);gradkeys=['accumulation_gradient_error','unweighted_microbatch_error','bf16_gradient_error','checkpoint_gradient_error','ddp_update_error'];labels=['加权累积','等权平均小批','BF16','重计算','两进程 DDP']if zh else['Weighted accumulation','Unweighted microbatches','BF16','Recompute','Two-process DDP']
    vals=[summary[k]for k in gradkeys];ax.barh(range(5),np.maximum(vals,1e-10),color=[colors[0],colors[1],colors[2],colors[0],colors[0]]);ax.set_xscale('log');ax.set_yticks(range(5),labels);ax.invert_yaxis();ax.set_xlabel('最大绝对差（0显示在1e-10）'if zh else'Max absolute difference (zero drawn at 1e-10)')
    for i,v in enumerate(vals):ax.text(max(v,1e-10)*1.25,i,f'{v:.2g}',va='center',fontsize=9)
    ax.set_xlim(7e-11,max(vals)*20)
    ax=fig.add_subplot(gs[1,1]);v=np.array([1e-8,1e-5,.1,1.001,1000.1],dtype=np.float32);bf=torch.tensor(v).bfloat16().float().numpy();fp=torch.tensor(v).half().float().numpy();table=[[f'{n:g}',f'{p:.7g}',f'{b:.7g}']for n,p,b in zip(v,fp,bf)];ax.axis('off');t=ax.table(cellText=table,colLabels=['FP32','FP16','BF16'],loc='center',cellLoc='center');t.auto_set_font_size(False);t.set_fontsize(11);t.scale(1,1.7);ax.set_title('真实类型转换：范围与精度是两件事'if zh else'Actual conversions: range and precision differ')
    save(fig,'memory')
    fig,axes=plt.subplots(1,2,figsize=(12.4,5),layout='constrained')
    names=['不中断','完整恢复','只恢复权重']if zh else['Uninterrupted','Full recovery','Weights only']
    for i,c in enumerate(curves):axes[0].plot(np.arange(1,13),c,label=names[i],color=colors[i],lw=2,ls=['-','--',':'][i],marker='o',ms=3)
    axes[0].axvline(6.5,color='gray',ls=':');axes[0].set_xlabel('参数更新次数'if zh else'Optimizer updates');axes[0].set_ylabel('抽样批次交叉熵'if zh else'Sampled-batch cross-entropy');axes[0].legend(frameon=False);axes[0].set_xticks([1,3,6,9,12])
    for i,(name,v)in enumerate(data_timing.items()):axes[1].scatter(np.full(len(v),i)+np.linspace(-.08,.08,len(v)),v,color=colors[i],s=18,alpha=.7);axes[1].plot([i-.2,i+.2],[np.median(v)]*2,color='#243749',lw=2)
    axes[1].set_yscale('log');axes[1].set_xticks([0,1,2],['CSV全量解析','NPY全量读取','缓存96行复制']if zh else['Parse all CSV','Read all NPY','Copy 96 cached rows']);axes[1].tick_params(axis='x',labelsize=9);axes[1].set_ylabel('每次操作 / ms（对数轴）'if zh else'Milliseconds per operation (log scale)');axes[1].set_title('预热后的读取与解析成本'if zh else'Warm-cache reading and parsing costs')
    save(fig,'recovery')
    fig,axes=plt.subplots(1,2,figsize=(12.4,5.4),layout='constrained')
    n=1e8;devices=4;memory=np.array([[2,2,12],[2,2,12/devices],[2,2/devices,12/devices],[2/devices,2/devices,12/devices]])*n/1e9
    base=np.zeros(4)
    for j,label in enumerate(['参数','梯度','主权重 + Adam 状态']if zh else['Parameters','Gradients','Master weights + Adam state']):axes[0].bar(range(4),memory[:,j],bottom=base,color=colors[j],label=label);base+=memory[:,j]
    axes[0].set_xticks(range(4),['DDP','ZeRO-1','ZeRO-2','ZeRO-3']);axes[0].set_ylabel('每设备持久状态 / GB'if zh else'Persistent state per device / GB');axes[0].legend(frameon=False,fontsize=9);axes[0].set_title('解析预算：1亿参数、4设备、混合精度'if zh else'Analytical budget: 100M parameters, four devices')
    stages,micro=3,4
    for stage in range(stages):
        for mb in range(micro):
            axes[1].broken_barh([(stage+mb,1)],(stage-.32,.64),facecolors=colors[mb]);axes[1].text(stage+mb+.5,stage,str(mb+1),ha='center',va='center',color='white')
    axes[1].set_yticks(range(stages),['阶段1','阶段2','阶段3']if zh else['Stage 1','Stage 2','Stage 3']);axes[1].invert_yaxis();axes[1].set_xticks(range(7));axes[1].set_xlim(0,6);axes[1].set_xlabel('理想化前向时间槽（等时阶段）'if zh else'Idealized forward slots (equal stage times)');axes[1].set_title('4个微批，3阶段：利用率4/6'if zh else'Four microbatches, three stages: utilization 4/6')
    save(fig,'parallel')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--language',choices=['zh','en'],default='en');parser.add_argument('--render-only',action='store_true',help='Render another language from already measured outputs');args=parser.parse_args();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    if args.render_only:
        summary=json.loads((out/'summary.json').read_text());stored=np.load(out/'data.npz');pr=json.loads((out/'profile.json').read_text())
        data_timing={k:stored['data_'+k.replace(' ','_')]for k in ['Parse CSV','Read NPY','Cached rows']};step_timing={k:stored['step_'+k.replace(' ','_')]for k in ['FP32','CPU BF16','Recompute']}
        curves=[stored[k]for k in ['loss_full','loss_restored','loss_weights_only']]
        draw(out,args.language,summary,data_timing,step_timing,pr['events'],pr['operators'],curves);return
    x,y=make_data();summary,reference_update,reference_gradient=gradient_experiments(x,y)
    rendezvous=out/('rendezvous-'+uuid.uuid4().hex)
    mp.spawn(ddp_worker,args=(rendezvous.as_uri(),str(out)),nprocs=2,join=True)
    ranks=[torch.load(out/f'ddp-rank{k}.pt',weights_only=True)for k in range(2)]
    summary.update({'ddp_update_error':max_error(reference_update,ranks[0]['parameters']),'ddp_replica_error':max_error(ranks[0]['parameters'],ranks[1]['parameters']),'all_reduce_hand':ranks[0]['reduction'].tolist()})
    if rendezvous.exists():rendezvous.unlink()
    plain,plain_gradient=retained_storage(x,y,False);saved,checkpoint_gradient=retained_storage(x,y,True)
    summary.update({'saved_storage_plain_bytes':plain,'saved_storage_checkpoint_bytes':saved,'checkpoint_gradient_error':max_error(plain_gradient,checkpoint_gradient)})
    recovery_summary,*curves=recovery(x,y,out);summary.update(recovery_summary)
    data_timing,step_timing=timings(x,y,out);events,operators=profile(x,y,out)
    summary.update({'parameter_count':sum(p.numel()for p in new_model().parameters()),'timing_median_ms':{k:float(np.median(v))for k,v in step_timing.items()},'data_median_ms':{k:float(np.median(v))for k,v in data_timing.items()},'fp16_tiny':float(torch.tensor(1e-8).half()),'scaled_fp16_recovered':float((torch.tensor(1e-8)*65536).half().float()/65536),'bf16_tiny':float(torch.tensor(1e-8).bfloat16()),'memory_budget_gb':[1.6,.7,.55,.4],'pipeline_forward_utilization':4/6,'effective_batch_hand':4*8*3,
        'environment':{'device':'CPU','threads_per_process':2,'ddp_processes':2,'backend':'gloo','torch':str(torch.__version__),'numpy':np.__version__,'python':platform.python_version(),'os':platform.system()}})
    np.savez(out/'data.npz',features=x.numpy(),labels=y.numpy(),loss_full=curves[0],loss_restored=curves[1],loss_weights_only=curves[2],**{'step_'+k.replace(' ','_'):v for k,v in step_timing.items()},**{'data_'+k.replace(' ','_'):v for k,v in data_timing.items()})
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    draw(out,args.language,summary,data_timing,step_timing,events,operators,curves)
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
```

The initial run performs measurements and saves summary.json, raw timing samples, profiler ranges, model weights, and a training checkpoint. The --render-only option produces another figure language from those same measurements. profile.json contains phase durations and operator self times; trace.json stores the three steps in a common timeline format for inspection. Persistent-state budgets and ideal pipeline scheduling are calculated from their stated assumptions and labeled separately from measured CPU execution. This keeps an illustrative resource model distinct from a benchmark of particular hardware.

For a larger model, follow the same progression: establish the single-device gradient and denominator, verify accumulated and synchronized updates, measure time and peak memory, then choose the required sharding and parallel strategy. Build recovery into the smallest experiment as well. An optimization can then be understood as reduced waiting, reduced persistent state, increased recomputation, or changed numerical error, while the objective that training is meant to learn remains explicit throughout.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M26.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [Dive into Deep Learning: Training on Multiple GPUs](https://d2l.ai/chapter_computational-performance/multiple-gpus.html)

   Sections 13.5.1–13.5.4 and figure 13.5.3: partitioning and gradient aggregation.

   D2L original figure CC BY-SA4.0; full notice included.
2. [PyTorch Distributed design note](https://docs.pytorch.org/docs/2.15/notes/ddp.html)

   Internal Design: initial broadcast, gradient buckets, all-reduce, and optimizer consistency.
3. [PyTorch Distributed: Experiences on Accelerating Data Parallel Training](https://arxiv.org/abs/2006.15704)

   Original 2020 paper abstract: bucketing, computation–communication overlap, and skipped synchronization.
4. [PyTorch Automatic Mixed Precision](https://docs.pytorch.org/docs/2.15/amp.html)

   CPU training, BF16, autocast scope, and operation-specific types.
5. [PyTorch activation checkpointing](https://docs.pytorch.org/docs/2.15/checkpoint.html)

   Non-reentrant checkpointing, RNG preservation, and recomputation behavior.
6. [PyTorch data loading](https://docs.pytorch.org/docs/2.15/data.html)

   Dataset/DataLoader, batching, workers, and distributed sampling interfaces.
7. [Getting Started with FSDP2](https://docs.pytorch.org/tutorials/intermediate/FSDP_tutorial.html)

   Parameter all-gather, gradient reduce-scatter, sharded optimizer state, and prefetching.
8. [ZeRO: Memory Optimizations Toward Training Trillion Parameter Models](https://arxiv.org/abs/1910.02054)

   Abstract and sharded-state idea; plotted budgets independently calculated under explicit byte assumptions.
9. [PyTorch Tensor Parallel tutorial](https://docs.pytorch.org/tutorials/intermediate/TP_tutorial.html)

   Column/row sharding, layout communication, and composition with FSDP.
10. [PyTorch Pipeline Parallel tutorial](https://docs.pytorch.org/tutorials/intermediate/pipelining_tutorial.html)

    Stages, microbatches, GPipe, and 1F1B schedules.
11. [Switch Transformers](https://arxiv.org/abs/2101.03961)

    Original 2021 paper abstract: sparse expert routing and communication.
12. [JAX: grad and vmap](https://docs.jax.dev/en/latest/101/transformations.html)

    grad, value_and_grad, vmap, composition with jit, and initial compilation.
13. [JAX: Distributed arrays and automatic parallelization](https://docs.jax.dev/en/latest/201/sharding.html)

    Mesh, NamedSharding, PartitionSpec, and replicated/sharded/unreduced arrays.
14. [Keras: Customizing fit with TensorFlow](https://keras.io/guides/custom_train_step_in_tensorflow/)

    train_step, GradientTape, training mode, and optimizer application.
15. [TensorFlow: Distributed training](https://www.tensorflow.org/guide/distributed_training)

    MirroredStrategy and synchronous/asynchronous data parallelism.
16. [D2L full figure license](https://github.com/d2l-ai/d2l-en/blob/master/LICENSE)

    Attribution and CC BY-SA 4.0 license for the original figure.

    CC BY-SA4.0
