#!/usr/bin/env python

import argparse
import numpy as np
import matplotlib.pyplot as plt
import json
from matplotlib.font_manager import FontProperties

# csv -> json
def init(fp, exp_range):
    for exp_no in exp_range:
        js = []
        for i in range(1,6):
            data = np.loadtxt("{}/{}.csv".format(exp_no,i),delimiter=",", skiprows=1, usecols=(1,2))
            x_average = np.average(data[:, 0])
            y_average = np.average(data[:, 1])
            x_std = np.std(data[:, 0])
            y_std = np.std(data[:, 1])
            js.append({
                'x_ave': x_average,
                'y_ave': y_average,
                'x_std': x_std,
                'y_std': y_std
            })
            plt.scatter(data[:,0], data[:,1])
            plt.xlabel('X軸(mm)', fontproperties=fp)
            plt.ylabel('Y軸(mm)', fontproperties=fp)
            plt.savefig('images/{}-{}.png'.format(exp_no,i))
            plt.clf()

        json.dump(js, open('{}/result.json'.format(exp_no), 'w'))

# パワースペクトルの画像
def spectral_density(fp, exp_range):
    for exp_no in exp_range:
        for i in range(1,6):
            fig = plt.figure()
            ax = fig.add_subplot(1, 2, 1)
            bx = fig.add_subplot(1, 2, 2)
            data = np.loadtxt("{}/{}.csv".format(exp_no,i), delimiter=",", skiprows=1, usecols=(1,2))
            xs = data[:,0]
            abs_xs = np.absolute(np.fft.fft(xs))
            samp = 90 / len(abs_xs)
            f_x = [(n+1) * samp for n,_ in enumerate(abs_xs)]
            ax.set_xlabel('周波数(Hz)', fontproperties=fp)
            ax.set_ylabel('振幅', fontproperties=fp)
            ax.set_title('X軸', FontProperties=fp)
            bx.set_xlabel('周波数(Hz)', fontproperties=fp)
            bx.set_ylabel('振幅', fontproperties=fp)
            bx.set_title('Y軸', FontProperties=fp)
            ax.set_ylim(0,200)
            ax.set_xlim(0,5)
            ax.plot(f_x, abs_xs)
            bx.set_ylim(0,200)
            bx.set_xlim(0,5)
            ys = data[:,1]
            abs_ys = np.absolute(np.fft.fft(ys))
            samp = 90 / len(abs_ys)
            f_y = [(n+1) * samp for n,_ in enumerate(abs_xs)]
            bx.plot(f_y, abs_ys)
            fig.savefig('images/{}-{}-fourier.png'.format(exp_no, i))
            fig.clf()
            np.savetxt('{exp_no}/{e}-X.txt'.format(exp_no=exp_no,e=i), abs_xs)
            np.savetxt('{exp_no}/{e}-Y.txt'.format(exp_no=exp_no,e=i), abs_ys)

def bar(fp, exp_range):
    for exp_no in exp_range:
        js = json.load(open('{}/result.json'.format(exp_no), 'r'))
        x_aves = [e['x_ave'] for e in js]
        y_aves = [e['y_ave'] for e in js]

        fig = plt.figure()
        ax = fig.add_subplot(1, 2, 1)
        bx = fig.add_subplot(1, 2, 2)
        ax.set_ylabel('重心座標の平均', fontproperties=fp)
        ax.set_title('X軸', FontProperties=fp)
        bx.set_ylabel('重心座標の平均', fontproperties=fp)
        bx.set_title('Y軸', FontProperties=fp)
        ax.bar([x for x in range(1,6)], [e['x_ave'] for e in js], yerr=[e['x_std'] for e in js], color='red', tick_label='x')
        bx.bar([y for y in range(1,6)], [e['y_ave'] for e in js], yerr=[e['y_std'] for e in js], color='blue', tick_label='y')
        plt.savefig('images/{}-bar.png'.format(exp_no))
        fig.clear()
        ax = fig.add_subplot(1, 2, 1)
        bx = fig.add_subplot(1, 2, 2)
        ax.set_title('X軸', FontProperties=fp)
        bx.set_title('Y軸', FontProperties=fp)
        ax.bar([x for x in range(1,6)], [e['x_std'] for e in js], color='red', tick_label='x')
        bx.bar([y for y in range(1,6)], [e['y_std'] for e in js], color='blue', tick_label='y')
        plt.savefig('images/{}-std.png'.format(exp_no))

def main():
    parser = argparse.ArgumentParser(description='生体情報学の画像生成を自動化した奴, -i, -b, -s がなければ全ての画像を出力します．')
    parser.add_argument('-f', '--font', help='日本語のフォントのパスを指定してください.', required=True)
    parser.add_argument('-r', '--range', help='実験番号のレンジを2つの引数で取ります.', nargs=2, type=int, default=range(1,8))
    parser.add_argument('-i', '--init', help='散布図を生成する．<実験番号>/result.jsonに<実験番号>の各実験の結果を出力する．', action="store_true", default=False)
    parser.add_argument('-b', '--bar', help='重心座標の平均を出力する．', action="store_true", default=False)
    parser.add_argument('-s', '--spectral', help='パワースペクトルを出力する．', action="store_true", default=False)
    args = parser.parse_args()
    funcs = {'bar': bar, 'init':init, 'spectral': spectral_density}
    fp = FontProperties(fname=args.font)

    if not(args.init + args.bar + args.spectral):
        args.init = True
        args.bar = True 
        args.spectral = True
    if isinstance(args.range, list):
        args.range = range(args.range[0], args.range[1]+1)
    if args.init:
        funcs['init'](fp, args.range)
    if args.bar:
        funcs['bar'](fp, args.range)
    if args.spectral:
        funcs['spectral'](fp, args.range)

if __name__ == '__main__':
    main()