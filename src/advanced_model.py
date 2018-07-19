# full assembly of the sub-parts to form the complete net
import torch
import torch.nn as nn
from torch.autograd import Variable
import numpy as np
from PIL import Image
from torch.nn.functional import sigmoid
from advanced_model_modules import *


class CleanU_Net(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(CleanU_Net, self).__init__()
        self.Conv_down1 = Conv_down(in_channels, 32)
        self.Conv_down2 = Conv_down(32, 64)
        self.Conv_down3 = Conv_down(64, 128)
        self.Conv_down4 = Conv_down(128, 256)
        self.Conv_down5 = Conv_down(256, 512)
        self.Conv_up1 = Conv_up(512, 256)
        self.Conv_up2 = Conv_up(256, 128)
        self.Conv_up3 = Conv_up(128, 64)
        self.Conv_up4 = Conv_up(64, 32)
        self.Conv_out = nn.Conv2d(32, out_channels, 1, padding=0, stride=1)

    def forward(self, x):

        x, conv1 = self.Conv_down1(x)
        #print("dConv1 => down1|", x.shape)
        x, conv2 = self.Conv_down2(x)
        #print("dConv2 => down2|", x.shape)
        x, conv3 = self.Conv_down3(x)
        #print("dConv3 => down3|", x.shape)
        x, conv4 = self.Conv_down4(x)
        #print("dConv4 => down4|", x.shape)
        _, x = self.Conv_down5(x)
        #print("dConv5|", x.shape)
        x = self.Conv_up1(x, conv4)
        #print("up1 => uConv1|", x.shape)
        x = self.Conv_up2(x, conv3)
        #print("up2 => uConv2|", x.shape)
        x = self.Conv_up3(x, conv2)
        #print("up3 => uConv3|", x.shape)
        x = self.Conv_up4(x, conv1)
        x = self.Conv_out(x)

        return x


if __name__ == "__main__":
    # A full forward pass
    im = torch.randn(1, 1, 572, 572)
    model = CleanU_Net(1, 2)
    x = model(im)
    print(x.shape)
    del model
    del x
    # print(x.shape)
