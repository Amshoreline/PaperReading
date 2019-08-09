import os
import torch
import torch.nn as nn
import itertools

class DeformRoI(nn.Module):
    def __init__()

class DeformConv(nn.Module):
    def __init__(
        self, in_channels, out_channels, kernel_size, stride=1, padding=0,
    ):
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.weights = nn.Parameter(
            torch.Tensor(out_channels, in_channels, kernel_size ** 2)
        )
        self.weights.data.uniform_(-0.1, 0.1)
        self.biases = nn.Parameter(torch.Tensor(out_channels))
        self.stride = stride
        self.padding = torch.nn.ZeroPad2d(padding)
        self.conv = nn.Conv2d(
            in_channels, in_channels * 2, kernel_size=3, stride=1, padding=1
        )
    
    # x.size() = (b, c, h, w)
    # res.size() = (b, m, h_new, w_new)
    def forward(self, x):
        x = self.padding(x)
        b, c, h, w = x.size()
        offset_field = self.conv(x).view(b, self.in_channels, 2, h * w)
        offset_field = offset_field.permute(0, 1, 3, 2)  # (b, c, h * w, 2)
        h_new = (h - self.kernel_size) // self.stride + 1
        w_new = (w - self.kernel_size) // self.stride + 1
        res = []
        new_coords = torch.tensor(
            [coord for coord in itertools.product(range(h_new), range(w_new))]
        )
        new_coords_unfolded = torch.tensor(range(h_new * w_new))
        ps = torch.tensor(
            [
                coord for coord in itertools.product(
                    range(self.kernel_size), range(self.kernel_size)
                )
            ]
        )   # size() = (k * k, 2)
        ps_unfolded = torch.tensor(range(self.kernel_size * self.kernel_size))
        for i, new_coord in enumerate(new_coords):
            p0 = new_coord * self.stride
            p0_unfolded = new_coords_unfolded[i] * self.stride
            ori_p = (ps + p0.view(1, *p0.size())).float()   # (k * k, 2)
            ori_p_unfoled = (ps_unfolded + p0_unfolded).long() # (k * k, )
            delta_p = offset_field[:, :, ori_p_unfoled, :]  # (b, c, k * k, 2)
            ori_p = ori_p.view(1, 1, *ori_p.size())
            p = delta_p + ori_p
            conv_result = self.deform_conv(x, p, self.weights) + self.biases
            conv_result = conv_result.view(1, *conv_result.size()) # (1, b, m)
            res.append(conv_result)
        res = torch.cat(res, 0).permute(1, 2, 0)
        res = res.view(b, self.out_channels, h_new, w_new)
        return res

    # Bilinear interpolation
    # Input: Q.size() = (h * w, 2), P.size() = (b * c * k * k, 2)
    # Output: torch tensor with size = (b * c * k * k, h * w)
    def bilinear_interpolation(self, Q, P):
        P = P.view(P.size(0), 1, P.size(1))
        Q = Q.view(1, Q.size(0), Q.size(1))
        abs_diff = torch.abs(Q - P)
        res = 1 - abs_diff
        res[res <= 0] = 0
        return torch.prod(res, 2)

    # Sample
    # Input: feature_map.size() = (b, c, h, w), P.size() = (b, c, k * k, 2)
    # Output: res.size() = (b, c, k * k)
    def sample(self, feature_map, P):
        assert feature_map.size(0) == P.size(0)
        assert feature_map.size(1) == P.size(1)
        b, c, h, w = feature_map.size()
        coords = [coord for coord in itertools.product(range(h), range(w))]
        Q = torch.tensor(coords).float()
        bi_inter = self.bilinear_interpolation(Q, P.view(-1, P.size(-1)))
        bi_inter = bi_inter.view(b, c, P.size(2), h, w)
        feature_map = feature_map.view(b, c, 1, h, w)
        res = (bi_inter * feature_map).sum(dim=4).sum(dim=3)
        return res

    # A filter's deformable convololution
    # Input: feature_map.size() = (b, c, h, w), P.size() = (b, c, k * k, 2),
    #        W.size() = (c, k * k)
    # Output: a float value
    def deform_filter_conv(self, feature_map, P, W):
        sampled_feature = self.sample(feature_map, P)
        W = W.view(1, *W.size())
        return torch.sum(sampled_feature * W)

    # Deformable convolution
    # Input: feature_map.size() = (b, c, h, w), P.size() = (b, c, k * k, 2),
    #        Ws.size() = (m, c, k * k)
    # Output: res.size() = (b, m, )
    def deform_conv(self, feature_map, P, Ws):
        sampled_feature = self.sample(feature_map, P)   # (b, c, k * k)
        sampled_feature = sampled_feature.view(
            sampled_feature.size(0), 1, sampled_feature.size(1),
            sampled_feature.size(2)
        )
        Ws = Ws.view(1, *Ws.size())
        res = (sampled_feature * Ws)
        res = res.view(res.size(0), res.size(1), -1)
        return torch.sum(res, 2)


class Tester:
    def __init__(self, ):
        self.conv = DeformConv(
            in_channels=3, out_channels=4, kernel_size=3, padding=1,
        )
    
    # def test_bilinear(self, ):
    #     Q = torch.tensor([[0, 0], [0, 1], [1, 0], [1, 1]]).float()
    #     P = torch.tensor(
    #         [[[0, 0], [1, 0], [0, 1], [1, 1]],[[0, 0], [1, 0], [0, 1], [1, 1]]]
    #     ).float()
    #     print(self.conv.bilinear_interpolation(Q, P))

    # def test_sample(self):
    #     # batch_size = 2, channel_size = 2, height = 3, width = 2
    #     feature_map = torch.tensor(range(24)).view(2, 2, 3, 2).float()
    #     print('feature_map')
    #     print(feature_map)
    #     P = torch.tensor(
    #         [[[0, 0], [1, 0], [0, 1], [1, 1]],[[0, 0], [1, 0], [0, 1], [1, 1]]]
    #     ).float()
    #     x_p = self.conv.sample(feature_map, P)
    #     print(x_p.size())
    #     print(x_p)

    # def test_deform_filter(self, ):
    #     # batch_size = 2, channel_size = 2, height = 3, width = 2
    #     feature_map = torch.tensor(range(24)).view(2, 2, 3, 2).float()
    #     P = torch.tensor(
    #         [[[0, 0], [1, 0], [0, 1], [1, 1]],[[0, 0], [1, 0], [0, 1], [1, 1]]]
    #     ).float()
    #     W = torch.ones((2, 4))
    #     print(self.conv.deform_filter_conv(feature_map, P, W))

    def test_deform(self, ):
        # batch_size = 2, channel_size = 2, height = 3, width = 2, k = 1
        feature_map = torch.tensor(range(24)).view(2, 2, 3, 2).float()
        feature_map.requires_grad = True
        P = torch.zeros(8).view((2, 2, 1, 2))
        Ws = torch.ones((2, 2, 4))
        Ws.requires_grad = True
        res = self.conv.deform_conv(feature_map, P, Ws)
        print(res)
        loss = torch.sum(res)
        loss.backward()
        print(Ws.grad)
        print(feature_map.grad)

    def test_conv(self, ):
        x = torch.ones((2, 3, 512, 512))
        x.requires_grad = True
        print(x.size())
        output = self.conv(x)
        loss = torch.sum(output)
        loss.backward()
        print(output.size())
        print(not x.grad is None)

if __name__ == '__main__':
    tester = Tester()
    # tester.test_bilinear()
    # tester.test_sample()
    # tester.test_deform_filter()
    # tester.test_deform()
    tester.test_conv()