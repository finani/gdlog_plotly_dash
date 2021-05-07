#!/usr/bin/env python3

import os
import sys
import signal
import base64
import datetime
import io
import struct
import csv

import numpy as np

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import plotly.graph_objects as go


def signal_handler(signal, frame):
    print('\npressed ctrl + c!!!\n')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                prevent_initial_callbacks=True)

df = pd.DataFrame()
df_pc = pd.DataFrame()
df_header_list_sorted = []
fcMcMode_index = []
fcMcMode_value = []
fcMcMode_color = []

bin_data_type = 'dBBBBBBffffffffffffBBBBBdddffffffffHBHBddddddddddddfffffffffffBBBffffffffffffffffffffffffffffffffBfBddfddfffffffffffffffffffffffffffffffffBBfffHH'

csv_header_list = ['rosTime', 'flightMode', 'ctrlDeviceStatus',
                   'fcMcMode', 'nSat', 'gpsFix', 'jobSeq',
                   'velNedGps_mps_0', 'velNedGps_mps_1', 'velNedGps_mps_2',
                   'posNed_m_0', 'posNed_m_1', 'posNed_m_2',
                   'velNed_mps_0', 'velNed_mps_1', 'velNed_mps_2',
                   'rpy_0', 'rpy_1', 'rpy_2',
                   'yawSpType',
                   'ctrlUser', 'ctrlStruct', 'ctrlSetpointType', 'ctrlOutputType',
                   'ctrlSp_0', 'ctrlSp_1', 'ctrlSp_2',
                   'ctrlOp_0', 'ctrlOp_1', 'ctrlOp_2', 'yawSp',
                   'rcRPYT_0', 'rcRPYT_1', 'rcRPYT_2', 'rcRPYT_3',
                   'gpsNSV', 'rtkHealthFlag', 'gpsFusedNSV', 'gpHealth',
                   'posGPS_m_0', 'posGPS_m_1', 'posGPS_m_2',
                   'posRTK_m_0', 'posRTK_m_1', 'posRTK_m_2',
                   'posGpsFused_m_0', 'posGpsFused_m_1', 'posGpsFused_m_2',
                   'posGp_m_0', 'posGp_m_1', 'posGp_m_2',
                   'errLatMix', 'errLatVis', 'errLatLid', 'cmdLatVelIgain', 'cmdLatVelMix',
                   'errLatMixRate', 'errLatMixCov00', 'errLatMixCov11',
                   'vbxyz_mps_0', 'vbxyz_mps_1', 'vbxyz_mps_2',
                   'acWarnStat', 'acHorWarnAC', 'acVerWarnAC',
                   'acXYZRel_0', 'acXYZRel_1', 'acXYZRel_2',
                   'acHorWarnRange', 'acHorWarnAngle', 'acVerWarnRange', 'acVerWarnAngle',
                   'lidarDist', 'lidarAngle',
                   'lidarRaw_0', 'lidarRaw_1', 'lidarRaw_2', 'lidarRaw_3', 'lidarRaw_4', 'lidarRaw_5', 'lidarRaw_6', 'lidarRaw_7',
                   'velCmdLongLatHeave_mps_0', 'velCmdLongLatHeave_mps_1', 'velCmdLongLatHeave_mps_2',
                   'velCtrlIuvw_mps_0', 'velCtrlIuvw_mps_1', 'velCtrlIuvw_mps_2',
                   'posCtrlINED_m_0', 'posCtrlINED_m_1', 'posCtrlINED_m_2',
                   'gimbalRPYCmd_0', 'gimbalRPYCmd_1', 'gimbalRPYCmd_2',
                   'gimbalRPY_0', 'gimbalRPY_1', 'gimbalRPY_2',
                   'windStatus', 'windSpeed', 'windAngle', 'windQueryTime', 'windResponseTime',
                   'acousticTemp', 'tempQueryTime', 'tempResponseTime',
                   'accBody_mpss_0', 'accBody_mpss_1', 'accBody_mpss_2',
                   'trajUnitVectorTNB0_0', 'trajUnitVectorTNB1_0', 'trajUnitVectorTNB2_0',
                   'trajUnitVectorTNB0_1', 'trajUnitVectorTNB1_1', 'trajUnitVectorTNB2_1',
                   'trajUnitVectorTNB0_2', 'trajUnitVectorTNB1_2', 'trajUnitVectorTNB2_2',
                   'trajCmdTNB_0', 'trajCmdTNB_1', 'trajCmdTNB_2',
                   'stdJobLongPidErr', 'stdJobLongPidRate', 'stdJobLongPidIgain',
                   'guideModeLongPidErr', 'guideModeLongPidRate', 'guideModeLongPidIgain',
                   'pqr_A_0', 'pqr_B_1', 'pqr_C_2',
                   'rpdCmd_0', 'rpdCmd_1', 'rpdCmd_2',
                   'velCmdNav_mps_0', 'velCmdNav_mps_1', 'velCmdNav_mps_2',
                   'posCmdNed_m_0', 'posCmdNed_m_1', 'posCmdNed_m_2',
                   'missionType', 'jobType',
                   'bladeTravelDistance',
                   'trajTimeCur', 'trajTimeMax', 'pad_1', 'pad_2']

app.layout = html.Div([
    html.Div([
        dcc.ConfirmDialog(
            id='confirm',
        ),
        dcc.Upload(
            id='input_upload_data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')]),
            style={
                'width': '60%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px',
                'float': 'left'},
            multiple=True
        ),
        html.Div([
            html.A(html.Img(src=app.get_asset_url('nearthlab-logo-black-large.png'),
                            style={'height': '100%'}),
                   href='https://www.nearthlab.com/')
        ],
            style={
                'height': '40px',
                'textAlign': 'center',
                'padding-top': '20px'
        }),
    ],
        style={
            'display': 'inline'
    }
    ),
    html.Hr(),
    dcc.Tabs([
        dcc.Tab(label='2D Data Plot', children=[
            html.Label([
                dcc.Dropdown(
                    id='io_data_dropdown',
                    multi=True,
                    placeholder="Select Data"
                )
            ]),
            dcc.Graph(id='graph_go')
        ]),
        dcc.Tab(label='3D Data Plot', children=[
            dcc.Checklist(
                id='output_select_data_checklist',
                options=[
                    {'label': 'Flight Path', 'value': 'Flight_Path'},
                    {'label': 'Lidar Point Cloud', 'value': 'Lidar_PC'}],
                labelStyle={'display': 'inline-block'}
            ),
            dcc.Graph(id='graph_go_3d_pos')
        ]),
        dcc.Tab(label='Reserved', children=[
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [2, 4, 3],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [5, 4, 3],
                         'type': 'bar', 'name': 'Montreal'}
                    ]
                }
            )
        ])
    ]),
    dcc.Store(id='df_header_list_sorted')
])


def parse_contents(list_of_contents, list_of_names, list_of_dates):
    global df, df_pc, fcMcMode_index, fcMcMode_value, fcMcMode_color, df_header_list_sorted
    parsing_log = ''
    strNames = ''
    strDates = ''
    strDecoded = ''
    for contents, filename, date in zip(list_of_contents, list_of_names, list_of_dates):
        try:
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            if 'gdLog' in filename:
                if 'csv' in filename:
                    df = pd.read_csv(
                        io.StringIO(decoded.decode('utf-8')), low_memory=False)
                    parsing_log = parsing_log + 'gdLog csv file!\n'
                elif 'bin' in filename:
                    chunk = decoded[0:len(decoded)//616*616]
                    data_count = 0
                    with open(filename.split('.')[0] + '.csv', 'w', encoding='utf-8') as f_csv:
                        wr = csv.writer(f_csv)
                        wr.writerow(csv_header_list)
                        for unpacked_chunk in struct.iter_unpack(bin_data_type, chunk):
                            wr.writerow(list(unpacked_chunk))
                            if data_count % 3000 == 0:
                                print("data_count: " + str(data_count))
                            data_count += 1
                        print("Saved: " + f_csv.name)
                    df = pd.read_csv(filename.split('.')[0] + '.csv')
                    parsing_log = parsing_log + 'gdLog bin file!\n'
                elif 'xls' in filename:
                    df = pd.read_excel(io.BytesIO(decoded))
                    parsing_log = parsing_log + 'gdLog xls file!\n'
                # dataFrame Post-Processing
                # Ignore data before 2020 January 1st Wednesday AM 1:00:00
                df = df[df['rosTime'] > 1577840400]
                df.columns = df.columns.str.strip()
                df['dateTime'] = pd.to_datetime(
                    df['rosTime'], unit='s') + pd.DateOffset(hours=9)
                df['diffTime'] = df['rosTime'].diff()

                df.loc[df.fcMcMode == 0, 'strFcMcMode'] = 'RC'
                df.loc[df.fcMcMode == 1, 'strFcMcMode'] = 'Guide'
                df.loc[df.fcMcMode == 2, 'strFcMcMode'] = 'Auto'
                df.loc[df.fcMcMode == 3, 'strFcMcMode'] = 'Boot'
                df.loc[df.fcMcMode == 0, 'colorFcMcMode'] = 'yellow'
                df.loc[df.fcMcMode == 1, 'colorFcMcMode'] = 'Blue'
                df.loc[df.fcMcMode == 2, 'colorFcMcMode'] = 'turquoise'
                df.loc[df.fcMcMode == 3, 'colorFcMcMode'] = 'LightPink'
                df['diffFcMcMode'] = df['fcMcMode'].diff()

                fcMcMode_index = df.index[df['diffFcMcMode'] != 0].tolist()
                fcMcMode_index = fcMcMode_index - fcMcMode_index[0]
                fcMcMode_index = np.append(fcMcMode_index, len(df)-1)
                fcMcMode_value = df.iloc[fcMcMode_index].strFcMcMode.tolist()
                fcMcMode_color = df.iloc[fcMcMode_index].colorFcMcMode.tolist()

                df_header_list_sorted = sorted(df.columns.tolist())
            elif 'pointCloud' in filename:
                if 'csv' in filename:
                    np_pc = np.loadtxt(
                        io.StringIO(decoded.decode('utf-8')), delimiter=',')
                    np_pc = np_pc.astype(np.float)
                    np_pc = np_pc.reshape(-1, 3)
                    df_pc = pd.DataFrame(np_pc, columns=['x', 'y', 'z'])
                    parsing_log = parsing_log + 'pointCloud csv file!\n'
            strNames = strNames + filename + '\n'
            strDates = strDates + \
                str(datetime.datetime.fromtimestamp(date)) + '\n'
            strDecoded = strDecoded + str(decoded[0:100]) + '...\n'
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])
        confirm_msg = '[Parsing Log]\n' + parsing_log + \
            '\n[File Names]\n' + strNames + '\n[Raw Contents]\n' + strDecoded
    return confirm_msg, df_header_list_sorted


@app.callback(Output('df_header_list_sorted', 'data'),
              Output('io_data_dropdown', 'options'),
              Output('confirm', 'displayed'),
              Output('confirm', 'message'),
              Input('input_upload_data', 'contents'),
              State('input_upload_data', 'filename'),
              State('input_upload_data', 'last_modified'))
def update_data_upload(list_of_contents, list_of_names, list_of_dates):
    global df
    if list_of_contents is not None:
        confirm_msg, df_header_list_sorted = parse_contents(
            list_of_contents, list_of_names, list_of_dates)
        options = [{'label': df_header, 'value': df_header}
                   for df_header in df_header_list_sorted]
        return df_header_list_sorted, options, True, confirm_msg


@app.callback(
    Output('graph_go', 'figure'),
    Output('graph_go', 'config'),
    Input('io_data_dropdown', 'value')
)
def update_store_data(df_header):
    global df, fcMcMode_index, fcMcMode_value, fcMcMode_color
    figure = go.Figure()
    figure.update_layout(height=600,
                         margin=dict(r=20, b=10, l=10, t=10))
    if len(df_header) > 0:
        if 'diffTime' in df_header:
            figure.add_trace(go.Histogram(x=df['diffTime']))
        else:
            for idx in range(len(fcMcMode_index)-1):
                figure.add_vrect(
                    x0=df.iloc[fcMcMode_index[idx]
                               ].dateTime, x1=df.iloc[fcMcMode_index[idx+1]].dateTime, line_width=0,
                    annotation_text=fcMcMode_value[idx], annotation_position="top left",
                    fillcolor=fcMcMode_color[idx], opacity=0.2)
            x_title = 'dateTime'
            for y_title in df_header:
                # deleteTraces, FigureWidget
                figure.add_trace(go.Scatter(
                    x=df[x_title], y=df[y_title], name=y_title,
                    mode='lines',
                    line=dict(width=3)))
                figure.update_layout(
                    xaxis_title=x_title,
                    xaxis=dict(
                        rangeslider=dict(
                            visible=True,
                            thickness=0.1
                        )
                    )
                )
    config = dict({'displaylogo': False,
                   'scrollZoom': True,
                   'modeBarButtonsToAdd': ['drawline',
                                           'drawopenpath',
                                           'drawclosedpath',
                                           'drawcircle',
                                           'drawrect',
                                           'eraseshape'
                                           ]})
    return figure, config


@app.callback(
    Output("graph_go_3d_pos", "figure"),
    Output("graph_go_3d_pos", "config"),
    [Input("output_select_data_checklist", "value")])
def display_animated_graph(value):
    global df
    figure_3d = go.Figure()
    figure_3d.update_layout(scene=dict(
        xaxis_title='y_East',
        yaxis_title='x_North',
        zaxis_title='-z_Up'),
        height=600,
        margin=dict(r=20, b=10, l=10, t=10))
    if 'Flight_Path' in value:
        if 'posNed_0' in df.columns:
            for job_idx in df['jobSeq'].unique():
                df_jobSeq = df[df['jobSeq'] == job_idx]
                figure_3d.add_trace(go.Scatter3d(
                    x=df_jobSeq['posNed_1'], y=df_jobSeq['posNed_0'], z=-
                    df_jobSeq['posNed_2'],
                    name='Flight Path (jobSeq = ' + str(job_idx) + ')',
                    mode='lines',
                    line=dict(color=-df_jobSeq['rosTime'],
                              colorscale='Viridis', width=6),
                    text=df_jobSeq['strFcMcMode'],
                    hovertemplate='fcMcMode: <b>%{text}</b><br>' +
                    'X: %{x}<br>' +
                    'Y: %{y}<br>' +
                    'Z: %{z}'))
        elif 'posNed_m_0' in df.columns:
            for job_idx in df['jobSeq'].unique():
                df_jobSeq = df[df['jobSeq'] == job_idx]
                figure_3d.add_trace(go.Scatter3d(
                    x=df_jobSeq['posNed_m_1'], y=df_jobSeq['posNed_m_0'], z=-
                    df_jobSeq['posNed_m_2'],
                    name='Flight Path (jobSeq = ' + str(job_idx) + ')',
                    mode='lines',
                    line=dict(color=-df_jobSeq['rosTime'],
                              colorscale='Viridis', width=6),
                    text=df_jobSeq['strFcMcMode'],
                    hovertemplate='fcMcMode: <b>%{text}</b><br>' +
                    'X: %{x}<br>' +
                    'Y: %{y}<br>' +
                    'Z: %{z}'))
    if 'Lidar_PC' in value:
        figure_3d.add_trace(go.Scatter3d(
            x=df_pc['y'], y=df_pc['x'], z=-df_pc['z'], name='Lidar Point Cloud',
            mode='markers',
            marker=dict(size=3)))
    config_3d = dict({'displaylogo': False})
    return figure_3d, config_3d


if __name__ == '__main__':
    while(True):
        try:
            app.run_server(debug=True, host='10.10.150.22')
        except Exception as e:
            print(e)
