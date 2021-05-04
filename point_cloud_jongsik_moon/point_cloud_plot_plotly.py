#!/usr/bin/env python

import numpy as np
import sys
import csv
import plotly.graph_objects as go
import datetime
import os
currDir = os.getcwd()
dataDir = currDir
def plotCSV():
    pointcloudFromOctomapFileName = "point_cloud_jongsik_moon/pointCloudFromOctomap.csv"
    pointcloudOctomapDir = os.path.join(dataDir, pointcloudFromOctomapFileName)
    pointcloudOctomapf = open(pointcloudOctomapDir, 'r')
    rdr = csv.reader(pointcloudOctomapf)
    for line in rdr:
      pc = np.array(line)
    pc = pc.reshape(-1,3)
    size = pc.size/3
    pointcloudOctomapX = np.array(pc[0:,0], dtype=float)
    pointcloudOctomapY = np.array(pc[0:,1], dtype=float)
    pointcloudOctomapZ = np.array(pc[0:,2], dtype=float)
    pointclouddata = go.Scatter3d(
        x=pointcloudOctomapX,
        y=pointcloudOctomapY,
        z=pointcloudOctomapZ,
        marker=go.scatter3d.Marker(size=3),
        mode='markers'
    )
    data1 = []
    data1.append(pointclouddata)
    layout1 = go.Layout(
                 scene=dict(
                     aspectmode='data'
             ))
    fig1=go.Figure(data=data1, layout=layout1)
    fig1.show()
def main():
    plotCSV()
if __name__ == '__main__':
  main()