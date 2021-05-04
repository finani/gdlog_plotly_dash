#!/usr/bin/env python3

import os
import sys
import signal
import base64
import datetime
import io
import struct
import csv

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
            multiple=False
        ),
        html.Div([
            html.A(html.Img(height='100%', src='https://s3.us-west-2.amazonaws.com/secure.notion-static.com/31b49635-00f1-43f3-b0fb-6063080f3b9e/nearthlab-logo-black-large.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20210503%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210503T021850Z&X-Amz-Expires=86400&X-Amz-Signature=689d1b968b057dc2c71d7d13af424d7cbb1532d69fa24d95c1aa44abd69c41ec&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22nearthlab-logo-black-large.png%22'), href='https://www.nearthlab.com/')
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
    html.Hr(),  # horizontal line
    dcc.Tabs([
        dcc.Tab(label='Data Plot', children=[
            html.Label([
                dcc.Dropdown(
                    id='io_data_dropdown',
                    multi=True,
                    placeholder="Select Data"
                )
            ]),
            dcc.Graph(id='clientside_graph_go')
        ]),
        dcc.Tab(label='3D Data Plot', children=[
            dcc.Checklist(
                id='output_select_data_checklist',
                options=[
                    {'label': 'Flight Path', 'value': 'Flight_Path'},
                    {'label': 'Lidar Data', 'value': 'Lidar_Data'}],
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
                         'type': 'bar', 'name': u'Montréal'}
                    ]
                }
            )
        ])
    ]),
    dcc.Store(id='df_header_list_sorted'),
    dcc.Store(id='clientside_figure_store_go'),
    html.Hr(),
    html.Details([
        html.Summary('Input File Details'),
        html.Div(id='output_parsing_log'),
        html.Div(id='output_data_upload')
    ],
        open=True
    )
])


def parse_contents(contents, filename, date):
    global df
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), low_memory=False)
            parsing_log = 'read csv file done'
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
            parsing_log = 'read/parsing bin file done'
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
            parsing_log = 'read xls file done'
        # Ignore data before 2020년 January 1일 Wednesday AM 1:00:00
        df = df[df['rosTime'] > 1577840400]
        df.columns = df.columns.str.strip()
        df['dateTime'] = pd.to_datetime(
            df['rosTime'], unit='s') + pd.DateOffset(hours=9)
        # df_header_list = df.columns.tolist()
        df_header_list_sorted = sorted(df.columns.tolist())
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return html.Div([
        html.P('[File Name] ' + filename),
        html.P('[Last Modified] ' + str(datetime.datetime.fromtimestamp(date))),
        html.Hr(),  # horizontal line
        html.Div('Raw Content'),
        html.Pre(str(decoded[0:200]) + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ]), df_header_list_sorted, parsing_log


@app.callback(Output('output_data_upload', 'children'),
              Output('df_header_list_sorted', 'data'),
              Output('io_data_dropdown', 'options'),
              Output('output_parsing_log', 'children'),
              Input('input_upload_data', 'contents'),
              State('input_upload_data', 'filename'),
              State('input_upload_data', 'last_modified'))
def update_data_upload(list_of_contents, list_of_names, list_of_dates):
    global df
    if list_of_contents is not None:
        children, df_header_list_sorted, parsing_log = parse_contents(
            list_of_contents, list_of_names, list_of_dates)
        options = [{'label': df_header, 'value': df_header}
                   for df_header in df_header_list_sorted]
        parsing_children = html.Div(parsing_log)
        return children, df_header_list_sorted, options, parsing_children


@app.callback(
    Output('clientside_figure_store_go', 'data'),
    Input('io_data_dropdown', 'value')
)
def update_store_data(df_header):
    global df
    try:
        figure = go.Figure()
        figure.update_layout(height=550,
                             margin=dict(r=20, b=10, l=10, t=10))
        if len(df_header) > 0:
            x_title = 'dateTime'
            for y_title in df_header:
                # deleteTraces, FigureWidget
                figure.add_trace(go.Scatter(
                    x=df[x_title], y=df[y_title], name=y_title))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error plotting data.'
        ])
    return figure


app.clientside_callback(
    """
    function(figure) {
        if(figure === undefined) {
            return {'data': [], 'layout': {}};
        }
        const fig = Object.assign({}, figure, {
            'layout': {
                ...figure.layout,
                'yaxis': {
                    ...figure.layout.yaxis
                }
             }
        });
        return fig;
    }
    """,
    Output('clientside_graph_go', 'figure'),
    Input('clientside_figure_store_go', 'data')
)


@app.callback(
    Output("graph_go_3d_pos", "figure"),
    [Input("output_select_data_checklist", "value")])
def display_animated_graph(value):
    global df
    figure_3d = go.Figure()
    figure_3d.update_layout(scene=dict(
        xaxis_title='y_East',
        yaxis_title='x_North',
        zaxis_title='-z_Up'),
        height=550,
        margin=dict(r=20, b=10, l=10, t=10))
    if 'Flight_Path' in value:
        if 'posNed_0' in df.columns:
            figure_3d.add_trace(go.Scatter3d(
                x=df['posNed_1'], y=df['posNed_0'], z=-df['posNed_2'],
                mode='lines',
                line=dict(color=-df['rosTime'], colorscale='Viridis', width=6)))
        elif 'posNed_m_0' in df.columns:
            figure_3d.add_trace(go.Scatter3d(
                x=df['posNed_m_1'], y=df['posNed_m_0'], z=-df['posNed_m_2'],
                mode='lines',
                line=dict(color=-df['rosTime'], colorscale='Viridis', width=6)))
    if 'Lidar_Data' in value:
        print('Lidar_Data')
    return figure_3d


if __name__ == '__main__':
    while(True):
        try:
            app.run_server(debug=True, host='192.168.0.221')
        except Exception as e:
            print(e)
