import argparse
import torch
import typing
import numpy as np
import collections
import os

parser=argparse.ArgumentParser()

parser.add_argument('--data_path', type=str, default='data/')
parser.add_argument('--dataset', type=str, default='data_NAX_new',
                    help='Data_1999_2019, Data_1999_2019_NA_Factor, Data_2001_2019_NA_Time_Vix, data_NAX, data_NAX_new')
parser.add_argument('--data_mode', type=str, default='return', help='[price, standardized, return]')
parser.add_argument('--bs', type=int, default=128, help='batch size')
parser.add_argument('--ehs', type=int, default=64, help='dimension of Encoder hidden state')
parser.add_argument('--dhs', type=int, default=64, help='dimension of Decoder hidden state')
parser.add_argument('--t', type=int, default=10, help='number of time steps')
parser.add_argument('--q', type=int, default=19, help='predictions day from input')

parser.add_argument('--lr', type=float, default=0.01, help='learning rate')
parser.add_argument('--epoch', type=int, default=10000, help='Epoch')
parser.add_argument('--testing_epoch', type=int, default=100)

parser.add_argument('--test', dest='test', action='store_true')
parser.set_defaults(test=False)

parser.add_argument('--bin', dest='bin', action='store_true')
parser.set_defaults(bin=False)

opt = parser.parse_args()

opt.device='cuda' if torch.cuda.is_available() else 'cpu'
print("==========================================================")
print(opt)

if not os.path.exists('plots'):
    os.makedirs('plots')
if not os.path.exists('saves'):
    os.makedirs('saves')


class TrainConfig(typing.NamedTuple):
    T: int
    Q: int
    train_size: int
    batch_size: int
    loss_func: typing.Callable


class TrainData(typing.NamedTuple):
    feats: np.ndarray
    targs: np.ndarray


DaRnnNet = collections.namedtuple("DaRnnNet", ["encoder", "decoder", "enc_opt", "dec_opt"])
