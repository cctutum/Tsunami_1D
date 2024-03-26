#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 15:57:44 2024

@author: ctutum
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
import subprocess
# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument('input_file', help='text file output by tsunami simulator')
# args = parser.parse_args()

# Create a folder for saving figures to create an animation
figures_dir = "figures_png"
if not os.path.exists(figures_dir):
    os.makedirs(figures_dir)

def plot_and_save_figure(h, time_step, file_counter, save=figures_dir):
    fig = plt.figure(figsize=(8, 3))
    ax = fig.add_axes((0.12, 0.2, 0.8, 0.7))
    plt.ylim(-0.2, 1.2)
    plt.xlim(1, 100)
    plt.xticks(range(25, 125, 25))
    plt.yticks(np.arange(-0.2, 1.4, 0.2))
    x = np.arange(1, 101)
    plt.plot(x, h[time_step], 'b-')
    plt.fill_between(x, -0.5, h[time_step], color='b', alpha=0.4)
    plt.grid()
    plt.xlabel('Distance [m]')
    plt.ylabel('Water elevation [m]')
    plt.title(r'Water elevation [m], time step ' + str(time_step))
    plt.savefig(f'{save}/water_height_{file_counter:04d}.png', dpi=150)
    plt.close(fig)
    
def animate(figures_dir, output_dir, output_format):
    ffmpeg_command = f"ffmpeg -r 10 -i {figures_dir}/water_height_%04d.png "
    ffmpeg_command += f"-b:v 10000000 {output_dir}/tsunami.{output_format}"
    subprocess.call(ffmpeg_command, shell=True)

matplotlib.use('Agg')
matplotlib.rcParams.update({'font.size': 16})

# read the output file from tsunami executable
# (./tsunami > tsunami_output.txt)
input_file = "tsunami_output.txt"

# read data into a list
data = [line.rstrip().split() for line in open(input_file).readlines()]
# get time steps
time = [float(line[0]) for line in data]

h = np.array([[float(x) for x in line[1:]] for line in data])
x = np.arange(1, h.shape[1]+1)

# save figures
file_counter = 0
for t in range(0, len(time), 5):
    plot_and_save_figure(h, t, file_counter)
    file_counter += 1
    
# make video using ffmpeg
videos_dir = "videos"
if not os.path.exists(videos_dir):
    os.makedirs(videos_dir)

# create and save the animation file
animate(figures_dir, videos_dir, "gif")

    
    
    

