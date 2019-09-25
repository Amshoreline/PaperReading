## Zhang Chenbin
- MRI浏览工具
    - [ITK-SNAP](http://www.itksnap.org/pmwiki/pmwiki.php) all platforms
    - [RadiAnt](https://www.radiantviewer.com) windows onlys
    - [MitkWorkbench](http://mitk.org/wiki/The_Medical_Imaging_Interaction_Toolkit_(MITK)) all platforms
    - [Slicer](https://www.slicer.org) all platforms
- 比赛信息
    - [CHAOS:organ_segmentation](https://chaos.grand-challenge.org)
        - 肝脏分割(CT-MRI)
        - 肝脏分割(仅CT)
        - 肝脏分割(只适用于MRI)
        - 腹部器官分割(CT+MRI)
        - 腹部器官分割(仅MRI)
    - [Anatomy3](http://www.visceral.eu/closed-benchmarks/anatomy3/)
        - 分割目标：左/右肾、脾、肝、左/右肺、膀胱、腹直肌、第一腰椎、胰腺、左/右腰肌、胆囊、胸骨、主动脉、气管、左/右肾上腺。
    - [CT-VIE19](http://aapmchallenges.cloudapp.net/competitions/35)
        - 肺部分割
    - [ACDC](https://www.creatis.insa-lyon.fr/Challenge/acdc/index.html)
        - 心脏分割+分类
    - [SLAWT](http://www.doc.ic.ac.uk/~rkarim/la_lv_framework/wall/index.html)
        - 心脏分割
    - [HVSMR](http://segchd.csail.mit.edu/index.html)
        - 分割血液池和心肌

- 损失函数
    - [JunMa11/SegLoss](https://github.com/JunMa11/SegLoss)
        - crossentropy loss
        - dice loss
        - boundary loss
        - focal loss
        - lovasz loss (cvpr workshop)
            - 是一个比较通用的loss，收敛较慢
    - [NifTK/NiftyNet](https://github.com/NifTK/NiftyNet/blob/dev/niftynet/layer/loss_segmentation.py) (偏野路子, 是一个TFboy，我们可能需要用torch重新实现一下)
        - undecided_loss
        - volume_enforcement loss
        - volume_enforcement_fin loss
        - generalised_dice_loss
        - dice_plus_xent_loss
        - sensitivity_specificity_loss
        - cross_entropy
        - cross_entropy_dense
        - wasserstein_disagreement_map
        - generalised_wasserstein_dice_loss
        - dice loss
        - dice_nosquare loss
        - tversky
        - dice_dense
        - dice_dense_nosquare

- 超参数调节的trick
    - 关于MRI
        - 数据预处理更加重要，对噪声的处理比较关键（比赛数据则不必担心）
    - 如何训练
        - 观察训练趋势，metric和loss的曲线
        - 根据任务和数据不同，loss的值会有差别
        - 停止训练的标志：验证集上指标曲线达到高点且平稳
    - 调参的trick，详见[kaggle总结](https://mp.weixin.qq.com/s/gf6Ebj9Nnh-QH7fLurH_WA)，原文网址[fast.ai](https://blog.floydhub.com/ten-techniques-from-fast-ai/)
        1. 使用Fast.ai库[fastai](https://github.com/fastai/fastai)
            - 效果较好的模型实现
            - Pytorch实现
        2. 使用多个而不是单一学习率
            - 差分学习率（Differential Learning rates）
            - 基于已有模型来训练深度学习网络
            - 大部分已有网络（如Resnet、VGG和Inception等）都是在ImageNet数据集训练的，因此我们要根据所用数据集与ImageNet图像的相似性，来适当改变网络权重。
        3. 如何找到合适的学习率
            - 周期性学习率，[Cyclical Learning Rates for Training Neural Networks](https://arxiv.org/abs/1506.01186)
        4. 余弦退火
            - 用余弦函数来降低学习率
        5. 带重启的SGD算法
            - 梯度下降算法可以通过突然提高学习率
            - [SGDR: Stochastic Gradient Descent with Warm Restarts](https://arxiv.org/abs/1608.03983)
        6. 更多内置函数：Dropout层、TTA
            - TTA: 为原始图像造出多个不同版本，包括不同区域裁剪和更改缩放程度等，并将它们输入到模型中；然后对多个版本进行计算得到平均输出，作为图像的最终输出分数
        

