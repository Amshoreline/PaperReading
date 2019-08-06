<font face='微软雅黑' >

# 2019.8.10
## 1.Learning Transferable Architectures for Scalable Image Recognition
### Abstract
- 概括
  - 搜索模型代价昂贵，本文的策略是先在小数据集上学习building block，之后扩展到大数据集
- 核心贡献
  - NASNet 搜索空间
- 实验内容
  - CIFAR-10 dataset 中设计block，扩展到ImageNet 设计出 NASNet architecture
  - 引入正则化技术 ScheduleDropPath，提高泛化能力
    - 在CIFAR-10上达到 error_rate=2.4% (state of art)
    - 在ImageNet上accuracy: 82.7%(top-1) 96.2%(top-5), top-1的准确率比人工设计网络高1.2%
- 搜索出的模型特点
  - 计算量小的同时达到高泛化能力
    - 控制计算量的方法：1.控制Normal Block个数；2.控制初始filter个数
  - 可以迁移至其他任务：如分割检测
    - 在COCO检测数据集上，达到43.1%mAP，比第二名高4%

### Method
- 搜索方式

<img src="pictures/1_1.png" width=512 height=256 />

*这里的probability计算方式是softmax*

- 可扩展的理由
  - 人工设计的网络结构多为重复的motifs
  - 每个motif是一系列conv_layer nonlinear的拼接，加上一些额外的连接组成
- 网络结构的实现就是一系列convolutional cells的重复
- 两种convolutional cell(为了能扩展到multiscalar images)
  - Normal Cell
   - Reduction Cell (Stride=2)
      - Trick: Double the number of filters whenever the spatial activation size is reduced in order to **maintain roughly constant hidden state dimension**
- 搜索细节
  - 强化学习的搜索方式
  - 随机搜索方式

<img src="pictures/1_2.png" />

<img src="pictures/1_3.png" />


### Experiments
- Controlled RNN训练方式
  - Proximal Plicy Optimization
- ScheduleDropPath
  - 在一个cell中，每个通路都按照一定概率关闭，该概率随着训练轮次增加增大
- CIFAR-10
  - 运行五轮计算平均误差为2.40%（最好一次是2.19%），之前的记录是2.56%
  - 使用了cutout data augmentation涨点
- ImageNet
  - 更少的计算量达到更好的准确率
  - 自行学习残差
- Object detection
  - 对比mobile-optimized网络：29.6% vs 24.5% (mAP at mini-val)
  - 对比其他网络：mini-val 43.2% vs 41.3%; test-dev 43.1% vs 40.7%
- RS和RL的对比
  - RS是brute-force random search
  - RL最佳模型比RS最佳模型好1%
  - RL找到的模型普遍比RS找到的好

### 补充
- mAP的计算方法

## 2.Deformable Convolutional Networks
### Method

<img src='pictures/2_1.png' />

- deformable convolution

<img src='pictures/2_2.png' />

- deformable RoI pooling

<img src='pictures/2_3.png' />

- deformable PS RoI pooling
  - PS: Position sensitive
<img src='pictures/2_4.png' />


## 3.Rich feature hierarchies for accurate object detection and semantic segmentation
### Abstract
- RCNN
  - Regions with CNN features

### Introduction
- PASCAL VOC 2010
  - RCNN 53.7% vs Selective search for object recognition 35.1%
- ILSVRC2013
  - RCNN 31.4% vs OverFeat 24.3%
- Segmentation on PASCAL VOC 2010
  - 47.9%

### Methods
- System
  - 为不同类独立生成候选区域的模块
  - 大型卷积神经网络，为每个区域提取出定长特征
  - 一系列SVM分类器，个数等于类别个数

<img src='pictures/3_1.png' />



</font>