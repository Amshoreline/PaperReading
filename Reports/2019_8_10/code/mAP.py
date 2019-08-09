import numpy as np

def computeAP(recalls, precisions):
    mrec = np.concatenate([0.], recalls, [1.])
    mpre = np.concatenate([0.], precisions, [0.])
    for i in range(mpre.size - 1, 0, -1):
        mpre[i - 1] = np.max(mpre[i - 1], mpre[i])
    i =  np.where(mrec[1: ] != mrec[: -1])[0]
    ap = np.sum((mrec[i + 1] - mrec[i]) * mpre[i + 1])
    return ap