这是一个将提供的作业说明翻译成中文的 Markdown 版本，其中包含了对源文档的严格引用。

# 作业 1：四核 CPU 上的性能分析

**截止日期：10月3日（星期五）晚上 11:59**

**总分 100 分 + 6 分附加分**

## 概述 ##
本作业旨在帮助您理解现代多核 CPU 中存在的两种主要并行执行形式：
1. 单个处理核心内的 SIMD 执行
2. 使用多个核心的并行执行（您也将看到 Intel 超线程的效果。）

您还将获得测量和推理并行程序性能的经验（这是一项具有挑战性但非常重要的技能，您将在本课程中贯穿使用）。 本作业仅包含少量的编程，但需要大量的分析！

**注意：在 Arm 架构上运行是可选的，且不计入成绩。**

---

## 环境设置 ##
**您需要在基于 Arm 的机器上运行代码，例如 M 系列的 Mac 电脑。**

注意：您首先需要安装 Intel SPMD 程序编译器（ISPC），可在 [http://ispc.github.io/](http://ispc.github.io/) 获取。

开始步骤：

1. 本作业中的许多程序都需要使用 ISPC 进行编译。 可以通过以下步骤轻松地在 myth 机器上安装 ISPC：
* 将 Linux 二进制文件下载到您选择的本地目录中。 
* 您可以从 ISPC [下载页面](https://ispc.github.io/downloads.html)获取适用于 Linux 的 ISPC 编译器二进制文件。 
* 对于 macOS，我们建议您使用 `curl` 或 `wget`（如果未找到，可以通过 Google 快速搜索了解如何在本地获取这些工具）直接从下载页面下载二进制文件。 
* 截至 2025 年秋季第 1 周，以下 `wget` 命令可以正常工作：
> `wget https://github.com/ispc/ispc/releases/download/v1.28.1/ispc-v1.28.1-MacOS.tar.gz`
* 解压下载的文件：`tar -xvf ispc-v1.28.1-MacOS.tar.gz`
* 将 ISPC 的 `bin` 目录添加到您的系统路径中。 
* 例如，如果解压下载的文件生成了目录 `~/Downloads/ispc-v1.28.1-MacOS`，在 bash 中您可以使用以下命令更新路径变量：
> `export PATH=$PATH:${HOME}/Downloads/ispc-v1.28.1-MacOS/bin`
* 上面这行代码可以添加到您的 `.bashrc` 文件中以永久生效。

2. 作业起始代码可在 [https://github.com/stanford-cs149/asst1](https://github.com/stanford-cs149/asst1) 获取。 请使用以下命令克隆作业 1 的起始代码：
> `git clone https://github.com/stanford-cs149/asst1.git`

---

## 程序 1：使用线程的并行分形生成 (20 分) ##
构建并运行代码库中 `prog1_mandelbrot_threads/` 目录下的代码。 （输入 `make` 进行构建，输入 `./mandelbrot` 运行它。）
该程序会生成图像文件 `mandelbrot-serial.ppm`，这是著名的复数集合 Mandelbrot 集的可视化。 图像中的每个像素对应复平面上的一个值，每个像素的亮度与确定该值是否包含在 Mandelbrot 集中所需的计算成本成正比。 要获取图像 2，请使用命令选项 `--view 2`。 （请参阅 `mandelbrotSerial.cpp` 中定义的函数 `mandelbrotSerial()`）。 您可以在 [http://en.wikipedia.org/wiki/Mandelbrot_set](http://en.wikipedia.org/wiki/Mandelbrot_set) 了解更多关于 Mandelbrot 集定义的信息。

您的工作是使用 [std::thread](https://en.cppreference.com/w/cpp/thread/thread) 并行化图像的计算。 位于 `mandelbrotThread.cpp` 中的函数 `mandelbrotThread()` 提供了一段生成一个额外线程的起始代码。 在此函数中，主应用程序线程使用构造函数 `std::thread(function, args...)` 创建另一个额外的线程。 它通过在线程对象上调用 `join` 来等待该线程完成。 目前启动的线程不进行任何计算并立即返回。 您应该向 `workerThreadStart` 函数添加代码来完成此任务。 在本作业中，您无需使用任何其他 std::thread API 调用。

**您需要做什么：**
1. 修改起始代码，使用两个处理器并行化 Mandelbrot 生成。 具体来说，在线程 0 中计算图像的上半部分，在线程 1 中计算图像的下半部分。 这种类型的问题分解被称为*空间分解*，因为图像的不同空间区域由不同的处理器计算。
2. 扩展您的代码以使用 2 到您机器的（Mac 上的性能 CPU 核心数或）机器线程数，并相应地划分图像生成工作（线程应获取图像的块）。 在您的报告中假设为什么是（或不是）这种情况？ （您可能还希望为**视图 2** 制作一个图表，以帮助您得出一个好的答案。 提示：仔细看看三线程数据点。）
3. 为了确认（或反驳）您的假设，请通过在 `workerThreadStart()` 的开头和结尾插入计时代码来测量每个线程完成其工作所需的时间。 您的测量结果如何解释您之前创建的加速图？
4. 修改工作与线程的映射，以尽可能提高 Mandelbrot 集上的加速比。 您在解决方案中不得在线程之间使用任何同步。 我们希望您想出一个能很好适用于所有线程数量的单一工作分解策略——不允许为每种配置硬编码特定的解决方案！ （提示：有一个非常简单的静态分配可以实现此目标，并且不需要线程间的通信/同步。） 在您的报告中，描述您的并行化方法，并报告在使用与您机器性能 CPU 核心数相同线程数的情况下获得的最终 8 线程加速比。
5. 现在使用 2 *（您的性能 CPU 核心数）机器线程运行改进后的代码。 性能是否明显高于使用八个线程运行时的性能？为什么？

---

## 程序 2：使用 SIMD 内置函数向量化代码 (20 分) ##
查看作业 1 代码库 `prog2_vecintrin/main.cpp` 中的函数 `clampedExpSerial`。 `clampedExp()` 函数针对输入数组的所有元素，将 `values[i]` 提升到由 `exponents[i]` 给定的幂，并将结果值限制在 9.999999。 在程序 2 中，您的工作是向量化这段代码，以便它可以在具有 SIMD 向量指令的机器上运行。

为了让事情简单一点，我们不要求您使用真实的 SSE、AVX2 或 Neon 向量内置函数，而是要求您使用定义在 `CS149intrin.h` 中的 CS149 “伪向量内置函数”来实现。 库中提供了对向量值或向量掩码进行操作的指令（它们只是模拟，用于提供更容易调试的反馈）。 `main.cpp` 中提供了 `abs()` 的向量化版本作为示例，但该示例并不能正确处理所有输入！

这里有一些提示：
* 每个向量指令都受一个可选掩码参数的约束。 掩码为 0 的通道被“屏蔽”，不会被覆盖。 如果未指定，则默认不屏蔽任何通道（全 1）。 提示：您将需要使用多个掩码寄存器和库中的掩码操作。
* 提示：在本问题中，使用 `_cs149_cntbits` 函数会很有帮助。
* 考虑如果总循环迭代次数不是 SIMD 向量宽度的倍数会发生什么。 建议使用 `./myexp -s 3` 进行测试，`_cs149_init_ones` 可能会有帮助。
* 提示：使用 `./myexp -l` 在最后打印执行日志，使用 `addUserLog()` 或 `CS149Logger.printLog()` 协助调试。

程序的输出将告诉您结果是否正确，并在出错时打印对比表格。 您的函数输出是 "output ="，应与 "gold =" 匹配。 您应将“总向量指令数”（Total Vector Instructions）视为性能指标（假设每条伪指令花费 1 个周期）。 “向量利用率”（Vector Utilization）显示了启用的通道百分比。

**您需要做什么：**
1. 在 `clampedExpVector` 中实现向量化版本的 `clampedExpSerial`，须兼容任意输入大小 `N` 和向量宽度 `VECTOR_WIDTH`。
2. 运行 `./myexp -s 10000` 并将向量宽度从 2、4、8 扫描到 16（通过更改 `CS149intrin.h` 中的 `#define` 值）。 记录利用率。利用率是增加、减少还是保持不变？为什么？
3. **附加分 (1 分)：** 在 `arraySumVector` 中实现 `arraySumSerial` 的向量化版本（假设宽度是大小的因子）。 目标运行时间为 `(N / VECTOR_WIDTH + VECTOR_WIDTH)` 或 `(N / VECTOR_WIDTH + log2(VECTOR_WIDTH))`。 `hadd` 和 `interleave` 会很有用。

---

## 程序 3：使用 ISPC 的并行分形生成 (20 分) ##
程序 3 利用 ISPC 实现了并行 Mandelbrot 分形生成，同时利用 CPU 的四个核心和每个核心内的 SIMD 执行单元。

在程序 1 中，我们显式地将工作分配给线程（核心）。 程序 3 使用 ISPC 语言结构来描述独立计算（每个像素的计算都是独立的），而 ISPC 编译器和运行时系统负责尽可能高效地生成利用并发资源的程序。

您需要对 C++ 和 ISPC 组合编写的程序 3 进行简单的修复（修复性能问题，而不是正确性问题）。 修复后，您应该观察到比原始顺序版本快 32 倍以上的性能。

### 程序 3，第 1 部分：ISPC 基础知识 (10 分) ###
ISPC 程序的多个实例始终在 CPU 的 SIMD 单元上并行执行。 实例数由编译器决定（内置变量 `programCount`）。 ISPC 代码可通过 `programIndex` 引用实例标识符。 因此，从 C 调用的 ISPC 函数可以被认为是产生了一组并发实例（gang）。

ISPC 提供 `foreach` 结构来表达问题分解，系统自动处理循环迭代的分配，这是一种声明式方法（仅指定要执行的工作）。 建议阅读 ISPC 演练 ([http://ispc.github.io/example.html](http://ispc.github.io/example.html))。

**您需要做什么：**
1. 编译并运行，但在 Makefile 中将 `avx2-i32x8` 更改为 `neon-i32x8` 并将 `x86-64` 更改为 `aarch64`，然后运行 make。 ISPC 编译器当前配置为发出 8 宽的 Neon 向量指令。 根据您对 CPU 的了解，您预期的最大加速比是多少？为什么观察到的数字可能低于理想值？（提示：考虑图像哪些部分的计算对 SIMD 提出了挑战，比较不同视图可能有助于确认假设。）

### 程序 3，第 2 部分：ISPC 任务 (10 分) ###
ISPC 还可以利用多个核心，机制是启动 *ISPC 任务*。
参见 `mandelbrot_ispc_withtasks` 函数中的 `launch[2]` 命令，它启动了处理图像不同区域的两个任务。

**您需要做什么：**
1. 运行带有 `--tasks` 参数的 `mandelbrot_ispc`。 视图 1 的加速比是多少？相对于未使用任务的版本加速了多少？
2. 仅更改 `mandelbrot_ispc_withtasks()` 中的代码以调整任务数，找出性能最好的任务数量。 您是如何确定的？为什么这个数字效果最好？
3. **附加分 (2 分)：** 程序 1 中的线程抽象与 ISPC 任务抽象有何区别？讨论一般情况（例如，启动 10,000 个任务与启动 10,000 个线程会发生什么）。

---

## 程序 4：迭代 `sqrt` (15 分) ##
程序 4 是一个计算 2000 万个随机数 (0-3 之间) 平方根的 ISPC 程序，它使用牛顿法求解方程 $\frac{1}{x^2} - S = 0$。
初始猜测值为 1.0。 输入接近 1 时收敛快，接近 0 或 3 时迭代次数增加。

**您需要做什么：**
1. 修改 Makefile 中的架构参数为 neon 和 aarch64 后构建运行。 报告单核（无任务）和所有核心（有任务）的加速比，并指出由于 SIMD 产生的加速比和由于多核并行化产生的加速比分别是多少。
2. 修改数组内容以构造一个**使相对于顺序代码的加速最大化**的特定输入。 报告加速比，并解释此修改是否提高了 SIMD 加速比或多核加速比以及原因。
3. 构造一个**使 ISPC（无任务）的加速比最小化**的特定输入。 描述此输入、选择它的原因并报告性能。 效率损失的原因是什么？（记住我们使用的是 8 宽 SIMD 指令）。
4. **附加分 (最高 2 分)：** 使用 AVX2 或 Arm Neon 内置函数手动编写您自己的 `sqrt` 版本，速度需要接近或快于 ISPC 生成的二进制文件。

---

## 程序 5：BLAS `saxpy` (10 分) ##
程序 5 实现了操作 `result = scale * X + Y` 的 BLAS `saxpy` 例程，其中向量大小 `N = 2000 万`。 它是一个*微不足道的并行化计算*，具有可预测的内存访问和成本。

**您需要做什么：**
1. 编译并运行，报告无任务和有任务的 ISPC 加速比。 解释程序的性能。 您认为它可以大幅改进吗（例如实现接近线性的加速比）？请说明理由。
2. **附加分 (1 分)：** 尽管每次仅加载 X, Y 并写入 result 元素，但总内存带宽消耗是 `4 * N * sizeof(float)`。 为什么乘数是 4？（提示：考虑 CPU 缓存）。
3. **附加分：** 大幅提升 `saxpy` 性能，描述您的方法和系统上的最佳可能性。

---

## 程序 6：让 `K-Means` 更快 (15 分) ##
程序 6 使用 K-Means 数据聚类算法对一百万个数据点进行聚类。 提供了一个正确的实现，但需要您找出其性能瓶颈并改进它。 

**您需要做什么：**
1. 下载数据（`scp` 命令略）并运行 `kmeans` 报告总运行时间。
2. 使用 `pip install -r requirements.txt` 下载绘图包并运行 `python3 plot.py` 生成起始和结束图像。 （在二维投影下，有些点看似未分配给“最近”的中心点是正常的）。
3. 利用 `CycleTimer::currentSeconds()` 函数分析代码中哪里花费的时间最多。
4. 根据发现进行改进，我们希望加速比达到约 2.1 倍或更高（$\frac{oldRuntime}{newRuntime} >= 2.1$）。 请在报告中以特定格式描述您的步骤和结果。

**限制条件：**
* 仅允许修改 `kmeansThread.cpp`。 不能改变核心接口或停止条件。
* **绝对不要改变实现的算法功能。**
* **重要提示：** 您只允许并行化以下函数中的**一个**：`dist`、`computeAssignments`、`computeCentroids`、`computeCost`。

提示：通常只需修改 20-25 行代码。 如果没有达到性能目标，报告中展示了良好的分析调试技巧，仍能获得大部分分数。

---

## 给好奇的同学 (强烈推荐) ##
ISPC 的联合创建者 Matt Pharr 撰写了一篇关于其开发历史的博客 [The story of ispc](https://pharr.org/matt/blog/2018/04/30/ispc-all)。 强烈推荐阅读！

## 提交流程 ##
通过 [Gradescope](https://www.gradescope.com) 提交。 每个小组提交一份，确保添加合作伙伴姓名。 只需要提交报告 `Assignment 1 (Write-Up)`，无需提交本地运行的代码。 请将 Mac 的结果粘贴在 Myth 服务器报告的后方。

## 资源与说明 ##
* 大量的 ISPC 文档见 [http://ispc.github.io/](http://ispc.github.io/)。
* 缩放 Mandelbrot 图像很有趣。
* Arm Neon 文档见 [https://developer.arm.com/architectures/instruction-sets/intrinsics/](https://developer.arm.com/architectures/instruction-sets/intrinsics/)。