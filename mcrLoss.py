import numpy as np
import torch
import other_func as ofc
from itertools import combinations



class MaximalCodingRateReduction(torch.nn.Module):
    def __init__(self, eff=False, eps=0.01, gam2=0.6):
        super(MaximalCodingRateReduction, self).__init__()
        self.eps = eps
        self.eff = eff
        self.gam2 = gam2

    def compute_discrimn_loss_empirical(self, W, gam1):
        p, m = W.shape
        I = torch.eye(p).cuda()
        scalar = p / (m * self.eps) 
        logdet = torch.logdet(I + gam1 * scalar * W.matmul(W.T))
        return logdet / 2.

    def compute_compress_loss_empirical(self, W, Pi):
        p, m = W.shape
        k, _, _ = Pi.shape
        I = torch.eye(p).cuda()
        compress_loss = 0.
        for j in range(k):
            trPi = torch.trace(Pi[j]) + 1e-8
            scalar = p / (trPi * self.eps)
            log_det = torch.logdet(I + scalar * W.matmul(Pi[j]).matmul(W.T))
            compress_loss += log_det * trPi / m
        return compress_loss / 2.

    def compute_discrimn_loss_theoretical(self, W):
        p, m = W.shape
        I = torch.eye(p).cuda()
        scalar = p / (m * self.eps)
        logdet = torch.logdet(I + scalar * W.matmul(W.T))
        return logdet / 2.

    def compute_compress_loss_theoretical(self, W, Pi):
        p, m = W.shape
        k, _, _ = Pi.shape
        I = torch.eye(p).cuda()
        compress_loss = 0.
        for j in range(k):
            trPi = torch.trace(Pi[j]) + 1e-8
            scalar = p / (trPi * self.eps)
            log_det = torch.logdet(I + scalar * W.matmul(Pi[j]).matmul(W.T))
            compress_loss += trPi / (2 * m) * log_det # 这个和论文的就是一样的了
        return compress_loss

    def forward(self, X, Y, num_classes=None):
        if num_classes is None:
            num_classes = Y.max() + 1
        W = X.T
        Pi = ofc.label_to_membership(Y.numpy(), num_classes)
        Pi = torch.tensor(Pi, dtype=torch.float32).cuda()

        discrimn_loss_empi = self.compute_discrimn_loss_empirical(W, num_classes)
        compress_loss_empi = self.compute_compress_loss_empirical(W, Pi)
        discrimn_loss_theo = self.compute_discrimn_loss_theoretical(W)
        compress_loss_theo = self.compute_compress_loss_theoretical(W, Pi)

        if self.eff:
            total_loss_empi = self.gam2 * - discrimn_loss_empi + (1-self.gam2) * compress_loss_empi
        else:
            total_loss_empi = self.gam2 * - discrimn_loss_empi + compress_loss_empi
        return (total_loss_empi,
                [discrimn_loss_empi.item(), compress_loss_empi.item()],
                [discrimn_loss_theo.item(), compress_loss_theo.item()])