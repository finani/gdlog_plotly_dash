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
from plotly.subplots import make_subplots


def signal_handler(signal, frame):
    print('\npressed ctrl + c!!!\n')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                prevent_initial_callbacks=True)

df = pd.DataFrame()
df_pc = pd.DataFrame()
fcMcMode_index = []
fcMcMode_value = []
fcMcMode_color = []

prev_mission_clicks = 0
prev_gps_clicks = 0
prev_rpd_roll_clicks = 0
prev_rpd_pitch_clicks = 0
prev_rpd_down_clicks = 0
prev_vel_u_clicks = 0
prev_vel_v_clicks = 0
prev_vel_w_clicks = 0
prev_pos_n_clicks = 0
prev_pos_e_clicks = 0
prev_pos_d_clicks = 0

bin_data_length = 616
bin_data_type = 'dBBBBBBffffffffffffBBBBBdddffffffffHBHBddddddddddddfffffffffffBBBffffffffffffffffffffffffffffffffBfBddfddfffffffffffffffffffffffffffffffffBBfffBBBB'
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
                   'trajTimeCur', 'trajTimeMax', 'pad_1', 'pad_2', 'pad_3', 'pad_4']

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
                ),
            ]),
            html.Label([
                dcc.Dropdown(
                    id='io_data_dropdown_2',
                    multi=True,
                    placeholder="Select Data"
                )
            ]),
            html.Button('mission', 
                        id='input_mission_button',
                        n_clicks=0),
            html.Button('gps', 
                        id='input_gps_button', 
                        n_clicks=0),
            html.Button('rpd_roll', 
                        id='input_rpd_roll_button', 
                        n_clicks=0),
            html.Button('rpd_pitch', 
                        id='input_rpd_pitch_button', 
                        n_clicks=0),
            html.Button('rpd_down', 
                        id='input_rpd_down_button', 
                        n_clicks=0),
            html.Button('vel_u', 
                        id='input_vel_u_button', 
                        n_clicks=0),
            html.Button('vel_v', 
                        id='input_vel_v_button', 
                        n_clicks=0),
            html.Button('vel_w', 
                        id='input_vel_w_button', 
                        n_clicks=0),
            html.Button('pos_n', 
                        id='input_pos_n_button', 
                        n_clicks=0),
            html.Button('pos_e', 
                        id='input_pos_e_button', 
                        n_clicks=0),
            html.Button('pos_d', 
                        id='input_pos_d_button', 
                        n_clicks=0),
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
    ])
])


def data_type_to_length(bin_data_type):
    bin_data_length_from_type = 0
    for c in bin_data_type:
        type_length = 0
        if c == 'd':
            type_length = 8
        elif c == 'f':
            type_length = 4
        elif c == 'H':
            type_length = 2
        elif c == 'B':
            type_length = 1
        bin_data_length_from_type = bin_data_length_from_type + type_length
    return bin_data_length_from_type


def parse_contents(list_of_contents, list_of_names, list_of_dates):
    global df, df_pc, fcMcMode_index, fcMcMode_value, fcMcMode_color, \
        bin_data_length, bin_data_type, csv_header_list
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
                    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')),
                                     low_memory=False)
                    parsing_log = parsing_log + 'gdLog csv file!\n'
                elif 'bin' in filename:
                    with open(filename.split('.')[0] + '.csv', 'w', encoding='utf-8') as f_csv:
                        if chr(decoded[0]) == 'n':
                            print("New_Format")
                            FcLogHeaderSize = decoded[2] << 8 | decoded[1]
                            FcLogTypeListSize = decoded[4] << 8 | decoded[3]
                            FcLogDataSize = decoded[6] << 8 | decoded[5]
                            FcLogHeader = \
                                decoded[7:7+FcLogHeaderSize].decode('ascii')
                            FcLogTypeList = \
                                decoded[7+FcLogHeaderSize:7+FcLogHeaderSize+FcLogTypeListSize]\
                                .decode('ascii')

                            csv_header_list = FcLogHeader.split(",")
                            bin_data_type = FcLogTypeList
                            bin_data_length = FcLogDataSize

                            bin_data_length_from_type = \
                                data_type_to_length(bin_data_type)
                            for idx in range(bin_data_length
                                             - bin_data_length_from_type
                                             - 20):  # structure padding size: 20
                                csv_header_list.append('pad_'+str(idx))
                                bin_data_type = bin_data_type + 'B'

                            decoded = decoded[7+FcLogHeaderSize
                                              + FcLogTypeListSize
                                              + FcLogDataSize:]
                        chunk = decoded[0:len(decoded)
                                        // bin_data_length*bin_data_length]
                        data_count = 0
                        wr = csv.writer(f_csv)
                        wr.writerow(csv_header_list)
                        for unpacked_chunk in struct.iter_unpack(bin_data_type, chunk):
                            wr.writerow(list(unpacked_chunk))
                            if data_count % 3000 == 0:
                                print("data_count: " + str(data_count))
                            data_count += 1
                        print("data_count: " + str(data_count) +
                              ", total_time: " + str(data_count/50) + " s (50Hz)")
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
                if 'rosTime' in df.columns:
                    df['dateTime'] = pd.to_datetime(df['rosTime'], unit='s') + \
                        pd.DateOffset(hours=9)
                    df['diffTime'] = df['rosTime'].diff()

                if 'fcMcMode' in df.columns:
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

                if 'jobType' in df.columns:
                    df.loc[df.jobType == 0, 'strJobType'] = 'INIT'
                    df.loc[df.jobType == 1, 'strJobType'] = 'STANDARD'
                    df.loc[df.jobType == 2, 'strJobType'] = 'TURN'
                    df.loc[df.jobType == 3, 'strJobType'] = 'CAM'
                    df.loc[df.jobType == 4, 'strJobType'] = 'WAYPOINT'
                    df.loc[df.jobType == 5, 'strJobType'] = 'TRAJECTORY'
                    df.loc[df.jobType == 6, 'strJobType'] = 'REFSIGTEST'
                    df.loc[df.jobType == 7, 'strJobType'] = 'TAKEOFF'
                    df.loc[df.jobType == 8, 'strJobType'] = 'LAND'
                    df.loc[df.jobType == 9, 'strJobType'] = 'RTB'
                    df.loc[df.jobType == 10, 'strJobType'] = 'PATHPLANNING'
                    df.loc[df.jobType == 11, 'strJobType'] = 'SKELETONMODELESTIMATION'
                    df.loc[df.jobType == 12, 'strJobType'] = 'HOPPINGBLADESURFACE'
                    df.loc[df.jobType == 13, 'strJobType'] = 'BLADEFOLLOWING'
                    df.loc[df.jobType == 255, 'strJobType'] = 'NONE'

                if 'missionType' in df.columns:
                    df.loc[df.missionType == 0, 'strMissionType'] = 'MISSION_TYPE_5_1'
                    df.loc[df.missionType == 1, 'strMissionType'] = 'MISSION_TYPE_5_2'
                    df.loc[df.missionType == 2, 'strMissionType'] = 'MISSION_TYPE_4_1'
                    df.loc[df.missionType == 3, 'strMissionType'] = 'MISSION_TYPE_4_2'
                    df.loc[df.missionType == 4, 'strMissionType'] = 'MISSION_TYPE_4_3'
                    df.loc[df.missionType == 5, 'strMissionType'] = 'MISSION_TYPE_WP'
                    df.loc[df.missionType == 6, 'strMissionType'] = 'MISSION_TYPE_3_1'
                    df.loc[df.missionType == 7, 'strMissionType'] = 'MISSION_TYPE_3_2'
                    df.loc[df.missionType == 8, 'strMissionType'] = 'MISSION_TYPE_6_1'
                    df.loc[df.missionType == 9, 'strMissionType'] = 'MISSION_TYPE_6_2'
                    df.loc[df.missionType == 10, 'strMissionType'] = 'MISSION_TYPE_6_1_SP'
                    df.loc[df.missionType == 11, 'strMissionType'] = 'MISSION_TYPE_6_2_SP'
                    df.loc[df.missionType == 12, 'strMissionType'] = 'MISSION_TYPE_HI'

                if 'gpsFix' in df.columns:
                    df.loc[df.gpsFix == 0, 'strGpsFix'] = 'No_GPS'
                    df.loc[df.gpsFix == 1, 'strGpsFix'] = 'NO_FIX'
                    df.loc[df.gpsFix == 2, 'strGpsFix'] = '2D_FIX'
                    df.loc[df.gpsFix == 3, 'strGpsFix'] = '3D_FIX'
                    df.loc[df.gpsFix == 4, 'strGpsFix'] = '3D_DGPS/SBAS_AIDED'
                    df.loc[df.gpsFix == 5, 'strGpsFix'] = '3D_RTK_FLOAT'
                    df.loc[df.gpsFix == 6, 'strGpsFix'] = '3D_RTK_FIXED'
                    df.loc[df.gpsFix == 7, 'strGpsFix'] = '3D_STATIC'
                    df.loc[df.gpsFix == 8, 'strGpsFix'] = '3D_PPP'

                if 'ctrlStruct' in df.columns:
                    df.loc[df.ctrlStruct == 0, 'strCtrlStruct'] = 'CTRL_STRUCT_NONE'
                    df.loc[df.ctrlStruct == 1, 'strCtrlStruct'] = 'VELI_PID0_ATTI_RPD'
                    df.loc[df.ctrlStruct == 2, 'strCtrlStruct'] = 'VELI_PID0CA_ATTI_RPD'
                    df.loc[df.ctrlStruct == 3, 'strCtrlStruct'] = 'VELB_PID0_ATTI_RPD'
                    df.loc[df.ctrlStruct == 4, 'strCtrlStruct'] = 'VELB_PID0CA_ATTI_RPD'
                    df.loc[df.ctrlStruct == 5, 'strCtrlStruct'] = 'VELB_0_VELB'
                    df.loc[df.ctrlStruct == 6, 'strCtrlStruct'] = 'VELB_0CA_VELB'
                    df.loc[df.ctrlStruct == 7, 'strCtrlStruct'] = 'VELI_0CA_VELI'
                    df.loc[df.ctrlStruct == 8, 'strCtrlStruct'] = 'POSI_PID0CA_VELI'
                    df.loc[df.ctrlStruct == 9, 'strCtrlStruct'] = 'POSI_PID0CA_ATTI'
                    df.loc[df.ctrlStruct == 10, 'strCtrlStruct'] = 'POSBVELB_PID0CA_ATTI'
                    df.loc[df.ctrlStruct == 11, 'strCtrlStruct'] = 'POSI_0_POSI'
                    df.loc[df.ctrlStruct == 12, 'strCtrlStruct'] = 'POSI_CA_POSI'
                    df.loc[df.ctrlStruct == 13, 'strCtrlStruct'] = 'TRAJ_PID0AC_ATTI_RPD'
                    df.loc[df.ctrlStruct == 14, 'strCtrlStruct'] = 'ATTI_0_ATTI'

                if 'ctrlSetpointType' in df.columns:
                    df.loc[df.ctrlSetpointType == 0, 'strCtrlSetpointType'] = 'CTRL_VECTYPE_NONE'
                    df.loc[df.ctrlSetpointType == 1, 'strCtrlSetpointType'] = 'LLH_POS'
                    df.loc[df.ctrlSetpointType == 2, 'strCtrlSetpointType'] = 'NEDABS_POS'
                    df.loc[df.ctrlSetpointType == 3, 'strCtrlSetpointType'] = 'NEALTABS_POS'
                    df.loc[df.ctrlSetpointType == 4, 'strCtrlSetpointType'] = 'NEALTREL_POS'
                    df.loc[df.ctrlSetpointType == 5, 'strCtrlSetpointType'] = 'XYALT_POS'
                    df.loc[df.ctrlSetpointType == 6, 'strCtrlSetpointType'] = 'XYD_POS'
                    df.loc[df.ctrlSetpointType == 7, 'strCtrlSetpointType'] = 'NED_VEL'
                    df.loc[df.ctrlSetpointType == 8, 'strCtrlSetpointType'] = 'UVW_VEL'
                    df.loc[df.ctrlSetpointType == 9, 'strCtrlSetpointType'] = 'EULER_ATT'
                    df.loc[df.ctrlSetpointType == 10, 'strCtrlSetpointType'] = 'TRAJ_VEC'

                if 'ctrlSpType' in df.columns:
                    df.loc[df.ctrlSpType == 0, 'strCtrlSpType'] = 'CTRL_VECTYPE_NONE'
                    df.loc[df.ctrlSpType == 1, 'strCtrlSpType'] = 'LLH_POS'
                    df.loc[df.ctrlSpType == 2, 'strCtrlSpType'] = 'NEDABS_POS'
                    df.loc[df.ctrlSpType == 3, 'strCtrlSpType'] = 'NEALTABS_POS'
                    df.loc[df.ctrlSpType == 4, 'strCtrlSpType'] = 'NEALTREL_POS'
                    df.loc[df.ctrlSpType == 5, 'strCtrlSpType'] = 'XYALT_POS'
                    df.loc[df.ctrlSpType == 6, 'strCtrlSpType'] = 'XYD_POS'
                    df.loc[df.ctrlSpType == 7, 'strCtrlSpType'] = 'NED_VEL'
                    df.loc[df.ctrlSpType == 8, 'strCtrlSpType'] = 'UVW_VEL'
                    df.loc[df.ctrlSpType == 9, 'strCtrlSpType'] = 'EULER_ATT'
                    df.loc[df.ctrlSpType == 10, 'strCtrlSpType'] = 'TRAJ_VEC'

                if 'ctrlOutputType' in df.columns:
                    df.loc[df.ctrlOutputType == 0, 'strCtrlOutputType'] = 'CTRL_VECTYPE_NONE'
                    df.loc[df.ctrlOutputType == 1, 'strCtrlOutputType'] = 'LLH_POS'
                    df.loc[df.ctrlOutputType == 2, 'strCtrlOutputType'] = 'NEDABS_POS'
                    df.loc[df.ctrlOutputType == 3, 'strCtrlOutputType'] = 'NEALTABS_POS'
                    df.loc[df.ctrlOutputType == 4, 'strCtrlOutputType'] = 'NEALTREL_POS'
                    df.loc[df.ctrlOutputType == 5, 'strCtrlOutputType'] = 'XYALT_POS'
                    df.loc[df.ctrlOutputType == 6, 'strCtrlOutputType'] = 'XYD_POS'
                    df.loc[df.ctrlOutputType == 7, 'strCtrlOutputType'] = 'NED_VEL'
                    df.loc[df.ctrlOutputType == 8, 'strCtrlOutputType'] = 'UVW_VEL'
                    df.loc[df.ctrlOutputType == 9, 'strCtrlOutputType'] = 'EULER_ATT'
                    df.loc[df.ctrlOutputType == 10, 'strCtrlOutputType'] = 'TRAJ_VEC'

                if 'ctrlOpType' in df.columns:
                    df.loc[df.ctrlOpType == 0, 'strCtrlOpType'] = 'CTRL_VECTYPE_NONE'
                    df.loc[df.ctrlOpType == 1, 'strCtrlOpType'] = 'LLH_POS'
                    df.loc[df.ctrlOpType == 2, 'strCtrlOpType'] = 'NEDABS_POS'
                    df.loc[df.ctrlOpType == 3, 'strCtrlOpType'] = 'NEALTABS_POS'
                    df.loc[df.ctrlOpType == 4, 'strCtrlOpType'] = 'NEALTREL_POS'
                    df.loc[df.ctrlOpType == 5, 'strCtrlOpType'] = 'XYALT_POS'
                    df.loc[df.ctrlOpType == 6, 'strCtrlOpType'] = 'XYD_POS'
                    df.loc[df.ctrlOpType == 7, 'strCtrlOpType'] = 'NED_VEL'
                    df.loc[df.ctrlOpType == 8, 'strCtrlOpType'] = 'UVW_VEL'
                    df.loc[df.ctrlOpType == 9, 'strCtrlOpType'] = 'EULER_ATT'
                    df.loc[df.ctrlOpType == 10, 'strCtrlOpType'] = 'TRAJ_VEC'

                if 'yawOpType' in df.columns:
                    df.loc[df.yawOpType == 0, 'strYawOpType'] = 'ANGLE_REL'
                    df.loc[df.yawOpType == 1, 'strYawOpType'] = 'ANGLE_ABS'
                    df.loc[df.yawOpType == 2, 'strYawOpType'] = 'RATE'
                    df.loc[df.yawOpType == 3, 'strYawOpType'] = 'FOWARD'

                df_header_list_sorted = sorted(df.columns.tolist())
            elif 'pointCloud' in filename:
                if 'csv' in filename:
                    np_pc = np.loadtxt(io.StringIO(decoded.decode('utf-8')),
                                       delimiter=',')
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


@app.callback(Output('io_data_dropdown', 'options'),
              Output('io_data_dropdown_2', 'options'),
              Output('confirm', 'displayed'),
              Output('confirm', 'message'),
              Input('input_upload_data', 'contents'),
              State('input_upload_data', 'filename'),
              State('input_upload_data', 'last_modified')
)
def update_data_upload(list_of_contents, list_of_names, list_of_dates):
    global df
    if list_of_contents is not None:
        confirm_msg, df_header_list_sorted = \
            parse_contents(list_of_contents, list_of_names, list_of_dates)
        options = [{'label': df_header, 'value': df_header}
                   for df_header in df_header_list_sorted]
        return options, options, True, confirm_msg


@app.callback(
    Output('graph_go', 'figure'),
    Output('graph_go', 'config'),
    Input('io_data_dropdown', 'value'),
    Input('io_data_dropdown_2', 'value'),
    Input('input_mission_button', 'n_clicks'),
    Input('input_gps_button', 'n_clicks'),
    Input('input_rpd_roll_button', 'n_clicks'),
    Input('input_rpd_pitch_button', 'n_clicks'),
    Input('input_rpd_down_button', 'n_clicks'),
    Input('input_vel_u_button', 'n_clicks'),
    Input('input_vel_v_button', 'n_clicks'),
    Input('input_vel_w_button', 'n_clicks'),
    Input('input_pos_n_button', 'n_clicks'),
    Input('input_pos_e_button', 'n_clicks'),
    Input('input_pos_d_button', 'n_clicks')
)
def update_graph_data(df_header, df_header_2, 
                      mission_clicks, gps_clicks, 
                      rpd_roll_clicks, rpd_pitch_clicks, rpd_down_clicks, 
                      vel_u_clicks, vel_v_clicks, vel_w_clicks, 
                      pos_n_clicks, pos_e_clicks, pos_d_clicks):
    global df, fcMcMode_index, fcMcMode_value, fcMcMode_color
    global prev_mission_clicks, prev_gps_clicks
    global prev_rpd_roll_clicks, prev_rpd_pitch_clicks, prev_rpd_down_clicks
    global prev_vel_u_clicks, prev_vel_v_clicks, prev_vel_w_clicks
    global prev_pos_n_clicks, prev_pos_e_clicks, prev_pos_d_clicks
    if prev_mission_clicks != mission_clicks:
        df_header = ['jobSeq']
        df_header_2 = ['strJobType', 'strMissionType']
        prev_mission_clicks = mission_clicks
    elif prev_gps_clicks != gps_clicks:
        df_header = ['nSat', 'gpsNSV', 'gpHealthStrength']
        df_header_2 = ['strGpsFix']
        prev_gps_clicks = gps_clicks
    elif prev_rpd_roll_clicks != rpd_roll_clicks:
        if 'rpy_0' in df.columns:
            df_header = ['rpy_0', 'rpdCmd_0']
        else:
            df_header = ['RPY_deg[0]', 'rpdCmd_deg_deg_mps[0]']
        if 'strCtrlSpType' in df.columns:
            df_header_2 = ['strCtrlStruct', 'strCtrlSpType']
        else:
            df_header_2 = ['strCtrlStruct', 'ctrlSetpointType']
        prev_rpd_roll_clicks = rpd_roll_clicks
    elif prev_rpd_pitch_clicks != rpd_pitch_clicks:
        if 'rpy_1' in df.columns:
            df_header = ['rpy_1', 'rpdCmd_1']
        else:
            df_header = ['RPY_deg[1]', 'rpdCmd_deg_deg_mps[1]']
        if 'strCtrlSpType' in df.columns:
            df_header_2 = ['strCtrlStruct', 'strCtrlSpType']
        else:
            df_header_2 = ['strCtrlStruct', 'ctrlSetpointType']
        prev_rpd_pitch_clicks = rpd_pitch_clicks
    elif prev_rpd_down_clicks != rpd_down_clicks:
        if 'velNed_2' in df.columns:
            df_header = ['velNed_2', 'velCmdNav_2']
        else:
            df_header = ['velUVW_mps[2]', 'velCmdUVW_mps[2]']
        if 'strCtrlSpType' in df.columns:
            df_header_2 = ['strCtrlStruct', 'strCtrlSpType']
        else:
            df_header_2 = ['strCtrlStruct', 'ctrlSetpointType']
        prev_rpd_down_clicks = rpd_down_clicks
    elif prev_vel_u_clicks != vel_u_clicks:
        df_header = ['velUVW_mps[0]', 'velCmdUVW_mps[0]']
        if 'strCtrlSpType' in df.columns:
            df_header_2 = ['strCtrlStruct', 'strCtrlSpType']
        else:
            df_header_2 = ['strCtrlStruct', 'ctrlSetpointType']
        prev_vel_u_clicks = vel_u_clicks
    elif prev_vel_v_clicks != vel_v_clicks:
        df_header = ['velUVW_mps[1]', 'velCmdUVW_mps[1]']
        if 'strCtrlSpType' in df.columns:
            df_header_2 = ['strCtrlStruct', 'strCtrlSpType']
        else:
            df_header_2 = ['strCtrlStruct', 'ctrlSetpointType']
        prev_vel_v_clicks = vel_v_clicks
    elif prev_vel_w_clicks != vel_w_clicks:
        df_header = ['velUVW_mps[2]', 'velCmdUVW_mps[2]']
        if 'strCtrlSpType' in df.columns:
            df_header_2 = ['strCtrlStruct', 'strCtrlSpType']
        else:
            df_header_2 = ['strCtrlStruct', 'ctrlSetpointType']
        prev_vel_w_clicks = vel_w_clicks
    elif prev_pos_n_clicks != pos_n_clicks:
        if 'posNed_0' in df.columns:
            df_header = ['posNed_0', ' posCmdNed_0']
        else:
            df_header = ['posNED_m[0]', 'posCmdNED_m[0]']
        if 'strCtrlSpType' in df.columns:
            df_header_2 = ['strCtrlStruct', 'strCtrlSpType']
        else:
            df_header_2 = ['strCtrlStruct', 'ctrlSetpointType']
        prev_pos_n_clicks = pos_n_clicks
    elif prev_pos_e_clicks != pos_e_clicks:
        if 'posNed_1' in df.columns:
            df_header = ['posNed_1', ' posCmdNed_1']
        else:
            df_header = ['posNED_m[1]', 'posCmdNED_m[1]']
        if 'strCtrlSpType' in df.columns:
            df_header_2 = ['strCtrlStruct', 'strCtrlSpType']
        else:
            df_header_2 = ['strCtrlStruct', 'ctrlSetpointType']
        prev_pos_e_clicks = pos_e_clicks
    elif prev_pos_d_clicks != pos_d_clicks:
        if 'posNed_2' in df.columns:
            df_header = ['posNed_2', ' posCmdNed_2']
        else:
            df_header = ['posNED_m[2]', 'posCmdNED_m[2]']
        if 'strCtrlSpType' in df.columns:
            df_header_2 = ['strCtrlStruct', 'strCtrlSpType']
        else:
            df_header_2 = ['strCtrlStruct', 'ctrlSetpointType']
        prev_pos_d_clicks = pos_d_clicks
        
    figure = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True
    )
    figure.update_layout(height=675,
                         margin=dict(r=20, b=10, l=10, t=10))
    if len(df_header) > 0:
        if 'diffTime' in df_header:
            figure.add_trace(go.Histogram(x=df['diffTime']), 
                             row=1, 
                             col=1)
        else:
            x_title = 'dateTime'
            try:
                for y_title in df_header:
                    figure.add_trace(go.Scatter(
                        x=df[x_title], y=df[y_title], name=y_title,
                        mode='lines',
                        line=dict(width=3)), 
                        row=1, 
                        col=1)
            except Exception as e:
                print(e)
            try:
                for y_title in df_header_2:
                    figure.add_trace(go.Scatter(
                        x=df[x_title], y=df[y_title], name=y_title,
                        mode='lines',
                        line=dict(width=3)), 
                        row=2, 
                        col=1)
            except Exception as e:
                print(e)
            for idx in range(len(fcMcMode_index)-1):
                figure.add_vrect(
                    x0=df.iloc[fcMcMode_index[idx]].dateTime,
                    x1=df.iloc[fcMcMode_index[idx+1]].dateTime,
                    line_width=0,
                    annotation_text=fcMcMode_value[idx],
                    annotation_position="top left",
                    fillcolor=fcMcMode_color[idx],
                    layer="below",
                    opacity=0.2)
            figure.update_layout(
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
    [Input("output_select_data_checklist", "value")]
)
def update_3d_graph_data(value):
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
                    x=df_jobSeq['posNed_1'],
                    y=df_jobSeq['posNed_0'],
                    z=-df_jobSeq['posNed_2'],
                    name='Flight Path (jobSeq = ' + str(job_idx) + ')',
                    mode='lines',
                    line=dict(color=-df_jobSeq['rosTime'],
                              colorscale='Viridis', width=6),
                    text=df_jobSeq['strFcMcMode'],
                    hovertemplate='fcMcMode: <b>%{text}</b><br>' +
                    'X: %{x}<br>' +
                    'Y: %{y}<br>' +
                    'Z: %{z}'))
        elif 'posNED_m[0]' in df.columns:
            for job_idx in df['jobSeq'].unique():
                df_jobSeq = df[df['jobSeq'] == job_idx]
                figure_3d.add_trace(go.Scatter3d(
                    x=df_jobSeq['posNED_m[1]'],
                    y=df_jobSeq['posNED_m[0]'],
                    z=-df_jobSeq['posNED_m[2]'],
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
            x=df_pc['y'], y=df_pc['x'], z=-df_pc['z'],
            name='Lidar Point Cloud',
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
