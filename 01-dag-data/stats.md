# 算法知识图谱 DAG 数据统计

生成日期：2026-08-21

## 总览

| 指标 | 值 |
|---|---|
| 组数 groups | 60 |
| 节点数 nodes | 372 |
| 边数 edges | 318 |
| 拓扑环检测（prerequisite 边） | 无环 (DAG 合法) |
| 严格环检测（prerequisite+combination 边） | 存在互向环: combination-number, lucas-theorem |

> 说明：严格检测将 combination 边视为排序边，其中 `lucas-theorem ↔ combination-number` 互为反向——该对是『Lucas 定理加速大组合数取模』与『组合数基础』的互补关系，非先后依赖，学习路径不构成环。DAG 合法性以 prerequisite 边为准。

| 内容缺失节点 | 0 |

## 组分布

| 组 | 领域 | 覆盖阶段 | 节点数 |
|---|---|---|---|
| G-A-1 排序与基础算法族 | 基础算法 | basic/intermediate | 20 |
| G-A-10 哈希与链表族 | 数据结构 | basic/intermediate | 3 |
| G-A-11 动态规划基础族 | 动态规划 | basic/intermediate | 15 |
| G-A-12 DP优化族 | 动态规划 | intermediate/advanced | 9 |
| G-A-13 高级DP族 | 动态规划 | advanced/frontier | 3 |
| G-A-14 搜索算法族 | 搜索算法 | basic/advanced | 9 |
| G-A-2 栈队列与单调结构族 | 数据结构 | basic/intermediate | 4 |
| G-A-3 堆与优先队列族 | 数据结构 | basic/advanced | 6 |
| G-A-4 并查集族 | 数据结构 | basic/advanced | 3 |
| G-A-5 区间查询与分块族 | 数据结构 | basic/advanced | 4 |
| G-A-6 线段树族 | 数据结构 | intermediate/advanced | 4 |
| G-A-7 可持久化数据结构族 | 数据结构 | intermediate/advanced | 1 |
| G-A-8 平衡二叉搜索树族 | 数据结构 | intermediate/advanced | 9 |
| G-A-9 高级树结构族 | 数据结构 | advanced/frontier | 2 |
| G-B-1 图基础与遍历 | 图论 | basic | 6 |
| G-B-2 最短路族 | 图论 | basic/advanced | 8 |
| G-B-3 生成树族 | 图论 | basic/advanced | 6 |
| G-B-4 连通性族 | 图论 | intermediate/advanced | 7 |
| G-B-5 网络流族 | 图论 | intermediate/advanced | 6 |
| G-B-6 二分图与匹配族 | 图论 | basic/advanced | 5 |
| G-B-7 树算法族 | 图论 | basic/advanced | 10 |
| G-B-8 欧拉与哈密顿族 | 图论 | intermediate/advanced | 3 |
| G-B-9 图论高级专题 | 图论 | intermediate/advanced | 5 |
| G-C-1 字符串匹配族 | 字符串 | intermediate/advanced | 5 |
| G-C-10 组合计数基础族 | 数学 | basic/intermediate | 5 |
| G-C-11 组合进阶族 | 数学 | intermediate/advanced | 8 |
| G-C-12 多项式与FFT族 | 数学 | advanced/frontier | 9 |
| G-C-13 生成函数族 | 数学 | advanced/frontier | 7 |
| G-C-14 线性代数族 | 数学 | intermediate/advanced | 9 |
| G-C-15 概率族 | 数学 | intermediate/advanced | 4 |
| G-C-16 数值方法族 | 数学 | intermediate/advanced | 3 |
| G-C-18 大整数与数制族 | 数学 | basic/intermediate | 4 |
| G-C-2 字典树与AC自动机族 | 字符串 | intermediate/advanced | 2 |
| G-C-3 后缀结构族 | 字符串 | advanced/frontier | 4 |
| G-C-4 后缀自动机族 | 字符串 | advanced/frontier | 3 |
| G-C-5 回文族 | 字符串 | intermediate/advanced | 2 |
| G-C-6 Lyndon与周期族 | 字符串 | advanced/frontier | 3 |
| G-C-7 数论基础族 | 数学 | basic/intermediate | 10 |
| G-C-8 数论进阶族 | 数学 | intermediate/advanced | 8 |
| G-C-9 数论高级族 | 数学 | advanced/frontier | 11 |
| G-D-1 凸包族 | 计算几何 | intermediate/advanced | 7 |
| G-D-10 调度与其他专题 | 高级专题 | intermediate/advanced | 4 |
| G-D-2 平面扫描与几何求交 | 计算几何 | intermediate/advanced | 10 |
| G-D-3 计算几何基础与度量 | 计算几何 | basic/advanced | 7 |
| G-D-4 树链剖分与动态树 | 高级数据结构 | advanced/frontier | 3 |
| G-D-5 可持久化数据结构 | 高级数据结构 | advanced | 5 |
| G-D-6 分块与根号算法 | 高级数据结构 | intermediate/advanced | 6 |
| G-D-7 莫队算法族 | 高级数据结构 | intermediate/frontier | 7 |
| G-D-8 高级线段树与离线 | 高级数据结构 | advanced/frontier | 5 |
| G-D-9 专题(topic 域) | 高级专题 | intermediate/advanced | 3 |
| G-E-1 IO与常数优化族 | 技巧 | basic/intermediate | 4 |
| G-E-10 前沿趋势组 | 前沿 | advanced/frontier | 6 |
| G-E-2 位运算族 | 技巧 | basic/advanced | 4 |
| G-E-3 Python竞赛特性族 | 语言特性 | basic/intermediate | 8 |
| G-E-4 调试与对拍族 | 竞赛策略 | basic/intermediate | 5 |
| G-E-5 随机化与元启发式族 | 技巧 | intermediate/advanced | 5 |
| G-E-6 博弈论族 | 数学/博弈 | intermediate/advanced | 7 |
| G-E-7 离线与杂项技巧族 | 杂项技巧 | intermediate/advanced | 18 |
| G-E-8 竞赛策略族 | 竞赛策略 | basic/intermediate | 6 |
| G-E-9 工具链族 | 工具 | basic/intermediate | 7 |

## 优先级分布

| 优先级 | 节点数 |
|---|---|
| P0 | 94 |
| P1 | 113 |
| P2 | 116 |
| P3 | 49 |

## Stage 分布

| Stage | 层 | 节点数 |
|---|---|---|
| basic | L0 | 69 |
| intermediate | L1 | 121 |
| advanced | L2 | 153 |
| frontier | L3 | 29 |

## 边类型分布

| 类型 | 数量 | 说明 |
|---|---|---|
| prerequisite | 113 | 前置/先修 |
| variant | 101 | 变体/衍生 |
| combination | 56 | 组合/依赖 |
| cooccurrence | 48 | 同现/并列 |

## 深度档分布（stage × depth_tier）

| Stage | depth_tier | 节点数 |
|---|---|---|
| advanced | brief | 18 |
| advanced | deep | 4 |
| advanced | standard | 131 |
| basic | deep | 60 |
| basic | standard | 9 |
| frontier | brief | 25 |
| frontier | standard | 4 |
| intermediate | brief | 5 |
| intermediate | deep | 41 |
| intermediate | standard | 75 |
