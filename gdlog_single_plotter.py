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
prev_submit_clicks = 0
prev_slide_ranger_clicks = 0

slide_ranger_toggle = True

bin_data_length = 616
bin_data_type = 'dBBBBBBffffffffffffBBBBBdddffffffffHBHBddddddddddddfffffffffffBBBffffffffffffffffffffffffffffffffBfBddfddfffffffffffffffffffffffffffffffffBBfffBBBB'
csv_header_list = ['rosTime', 'flightMode', 'ctrlDeviceStatus',
                   'fcMcMode', 'nSat', 'gpsFix', 'jobSeq',
                   'velNEDGps_mps_0', 'velNEDGps_mps_1', 'velNEDGps_mps_2',
                   'posNED_m_0', 'posNED_m_1', 'posNED_m_2',
                   'velNED_mps_0', 'velNED_mps_1', 'velNED_mps_2',
                   'rpy_deg_0', 'rpy_deg_1', 'rpy_deg_2',
                   'yawSpType',
                   'ctrlUser', 'ctrlStruct', 'ctrlSpType', 'ctrlOpType',
                   'ctrlSp_0', 'ctrlSp_1', 'ctrlSp_2',
                   'ctrlOp_0', 'ctrlOp_1', 'ctrlOp_2', 'yawSp_deg',
                   'rcRPYT_0', 'rcRPYT_1', 'rcRPYT_2', 'rcRPYT_3',
                   'gpsNSV', 'rtkHealthFlag', 'gpsFusedNSV', 'gpHealthStrength',
                   'posGPS_degE7_degE7_mm_0', 'posGPS_degE7_degE7_mm_1', 'posGPS_degE7_degE7_mm_2',
                   'posRTK_deg_deg_m_0', 'posRTK_deg_deg_m_1', 'posRTK_deg_deg_m_2',
                   'posGpsFused_rad_rad_m_0', 'posGpsFused_rad_rad_m_1', 'posGpsFused_rad_rad_m_2',
                   'posGP_deg_deg_m_0', 'posGP_deg_deg_m_1', 'posGP_deg_deg_m_2',
                   'StdJobLatCtrlPIDErrLatMix', 'StdJobLatCtrlPIDErrLatVis',
                   'StdJobLatCtrlPIDErrLatLidNorm', 'StdJobLatCtrlCmdVelLatIgain',
                   'StdJobLatCtrlCmdVelLatMix', 'StdJobLatCtrlPIDErrLatMixRate',
                   'StdJobLatCtrlPIDErrLatMixCov00', 'StdJobLatCtrlPIDErrLatMixCov11',
                   'velUVW_mps_0', 'velUVW_mps_1', 'velUVW_mps_2',
                   'AcWarnStat', 'AcHorWarnAC', 'AcVerWarnAC',
                   'AcXYZRel_m_0', 'AcXYZRel_m_1', 'AcXYZRel_m_2',
                   'AcHorWarnRange_m', 'AcHorWarnAngle_deg', 'AcVerWarnRange_m', 'AcVerWarnAngle_deg',
                   'LidarDist_m', 'LidarAngle_deg',
                   'LidarRaw_m_0', 'LidarRaw_m_1', 'LidarRaw_m_2', 'LidarRaw_m_3',
                   'LidarRaw_m_4', 'LidarRaw_m_5', 'LidarRaw_m_6', 'LidarRaw_m_7',
                   'llhVelCmd_1', 'llhVelCmd_0', 'llhVelCmd_2',
                   'velCtrlHdgI_0', 'velCtrlHdgI_1', 'velCtrlHdgI_2',
                   'posCtrlNEDI_0', 'posCtrlNEDI_1', 'posCtrlNEDI_2',
                   'gimbalRpyCmd_deg_0', 'gimbalRpyCmd_deg_1', 'gimbalRpyCmd_deg_2',
                   'gimbalRpy_deg_0', 'gimbalRpy_deg_1', 'gimbalRpy_deg_2',
                   'windStatus', 'windSpeed', 'windAngle', 'windQueryTime', 'windResponseTime',
                   'acousticTemp', 'tempQueryTime', 'tempResponseTime',
                   'accBody_mpss_0', 'accBody_mpss_1', 'accBody_mpss_2',
                   'trajUnitVectorT_0', 'trajUnitVectorT_1', 'trajUnitVectorT_2',
                   'trajUnitVectorN_0', 'trajUnitVectorN_1', 'trajUnitVectorN_2',
                   'trajUnitVectorB_0', 'trajUnitVectorB_1', 'trajUnitVectorB_2',
                   'trajVelCmdTNB_mps_0', 'trajVelCmdTNB_mps_1', 'trajVelCmdTNB_mps_2',
                   'StdJobLongPIDErr', 'StdJobLongPIDRate', 'StdJobLongPIDIgain',
                   'GuideModeLongPIDErr', 'GuideModeLongPIDRate', 'GuideModeLongPIDIgain',
                   'pqr_dps_0', 'pqr_dps_1', 'pqr_dps_2',
                   'rpdCmd_deg_deg_mps_0', 'rpdCmd_deg_deg_mps_1', 'rpdCmd_deg_deg_mps_2',
                   'velCmdHdg_mps_0', 'velCmdHdg_mps_1', 'velCmdHdg_mps_2',
                   'posCmdNED_m_0', 'posCmdNED_m_1', 'posCmdNED_m_2',
                   'missionType', 'jobType',
                   'bladeTravelDistance',
                   'trajTimeCur', 'trajTimeMax', 'pad_1', 'pad_2', 'pad_3', 'pad_4']

app.layout = html.Div([
    html.Div([
        dcc.ConfirmDialog(
            id='confirm_parsing_data',
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
            html.Button('slide_ranger: true',
                        id='input_slide_ranger_button',
                        n_clicks=0,
                        style={
                            'float': 'right'
                        }),
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
                            print("New_Format v" + str(decoded[1]))
                            FcLogHeaderSize = decoded[3] << 8 | decoded[2]
                            FcLogTypeListSize = decoded[5] << 8 | decoded[4]
                            FcLogDataSize = decoded[7] << 8 | decoded[6]
                            FcLogHeader = \
                                decoded[8:8+FcLogHeaderSize].decode('ascii')
                            FcLogTypeList = \
                                decoded[8+FcLogHeaderSize:8+FcLogHeaderSize+FcLogTypeListSize]\
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

                            decoded = \
                                decoded[8+FcLogHeaderSize+FcLogTypeListSize+FcLogDataSize:]
                        chunk = \
                            decoded[0:len(decoded)//bin_data_length*bin_data_length]
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
                        parsing_log = parsing_log + 'data_count : ' + str(data_count) + \
                            '\ntotal_time : ' + str(data_count/50) + ' s (50Hz)\n'
                    df = pd.read_csv(filename.split('.')[0] + '.csv')
                    parsing_log = parsing_log + 'gdLog bin file!\n'
                elif 'xls' in filename:
                    df = pd.read_excel(io.BytesIO(decoded))
                    parsing_log = parsing_log + 'gdLog xls file!\n'

                # dataFrame Post-Processing
                # Ignore data before 2020 January 1st Wednesday AM 1:00:00
                df = df.drop([0])  # delete data with initial value
                df = df[df['rosTime'] > 1577840400]
                df = df.dropna(axis=0)  # delete data with NaN
                df = df.reset_index(drop=True)
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
                      '\n[File Names]\n' + strNames + \
                      '\n[Raw Contents]\n' + strDecoded + \
                      '\n[Do you want to use only the Guide/Auto Data?]\n'
    return confirm_msg, df_header_list_sorted


@app.callback(
    Output('io_data_dropdown', 'options'),
    Output('io_data_dropdown_2', 'options'),
    Output('confirm_parsing_data', 'displayed'),
    Output('confirm_parsing_data', 'message'),
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
    Output('confirm_parsing_data', 'cancel_n_clicks'),  # dummy output
    Input('confirm_parsing_data', 'submit_n_clicks')
)
def update_df_data(submit_clicks):
    global df, fcMcMode_index, fcMcMode_value, fcMcMode_color
    global prev_submit_clicks

    if submit_clicks != prev_submit_clicks:
        for idx in range(len(fcMcMode_index)-1):
            if fcMcMode_value[idx] == 'Guide':
                cut_begin_idx = idx
                cut_begin = fcMcMode_index[idx]
                break
        for idx in reversed(range(len(fcMcMode_index)-1)):
            if fcMcMode_value[idx] == 'Guide':
                cut_end_idx = idx
                cut_end = fcMcMode_index[idx]
                break
        df = df[cut_begin:cut_end]
        df = df.reset_index(drop=True)
        fcMcMode_index = fcMcMode_index[cut_begin_idx:cut_end_idx] - fcMcMode_index[cut_begin_idx]
        fcMcMode_value = fcMcMode_value[cut_begin_idx:cut_end_idx]
        fcMcMode_color = fcMcMode_color[cut_begin_idx:cut_end_idx]
        
        prev_submit_clicks = submit_clicks
    return 0


@app.callback(
    Output('input_slide_ranger_button', 'children'),
    Input('input_slide_ranger_button', 'children'),
    Input('input_slide_ranger_button', 'n_clicks')
)
def update_graph_data(prev_slide_ranger_children, slide_ranger_clicks):
    global prev_slide_ranger_clicks, slide_ranger_toggle
    strSlideRanger = prev_slide_ranger_children

    if prev_slide_ranger_clicks != slide_ranger_clicks:
        slide_ranger_toggle = not slide_ranger_toggle
        strSlideRanger = 'slide_ranger: ' + str(slide_ranger_toggle)
        prev_slide_ranger_clicks = slide_ranger_clicks
    return strSlideRanger


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
        df_header = ['nSat', 'gpsNSV']
        df_header_2 = ['strGpsFix']
        prev_gps_clicks = gps_clicks
    elif prev_rpd_roll_clicks != rpd_roll_clicks:
        df_header = ['rpy_deg_0', 'rpdCmd_deg_deg_mps_0']
        df_header_2 = ['strCtrlStruct']
        prev_rpd_roll_clicks = rpd_roll_clicks
    elif prev_rpd_pitch_clicks != rpd_pitch_clicks:
        df_header = ['rpy_deg_1', 'rpdCmd_deg_deg_mps_1']
        df_header_2 = ['strCtrlStruct']
        prev_rpd_pitch_clicks = rpd_pitch_clicks
    elif prev_rpd_down_clicks != rpd_down_clicks:
        df_header = ['velUVW_mps_2', 'velCmdUVW_mps_2']
        df_header_2 = ['strCtrlStruct']
        prev_rpd_down_clicks = rpd_down_clicks
    elif prev_vel_u_clicks != vel_u_clicks:
        df_header = ['velUVW_mps_0', 'velCmdUVW_mps_0']
        df_header_2 = ['strCtrlStruct']
        prev_vel_u_clicks = vel_u_clicks
    elif prev_vel_v_clicks != vel_v_clicks:
        df_header = ['velUVW_mps_1', 'velCmdUVW_mps_1']
        df_header_2 = ['strCtrlStruct']
        prev_vel_v_clicks = vel_v_clicks
    elif prev_vel_w_clicks != vel_w_clicks:
        df_header = ['velUVW_mps_2', 'velCmdUVW_mps_2']
        df_header_2 = ['strCtrlStruct']
        prev_vel_w_clicks = vel_w_clicks
    elif prev_pos_n_clicks != pos_n_clicks:
        df_header = ['posNED_m_0', 'posCmdNED_m_0']
        df_header_2 = ['strCtrlStruct']
        prev_pos_n_clicks = pos_n_clicks
    elif prev_pos_e_clicks != pos_e_clicks:
        df_header = ['posNED_m_1', 'posCmdNED_m_1']
        df_header_2 = ['strCtrlStruct']
        prev_pos_e_clicks = pos_e_clicks
    elif prev_pos_d_clicks != pos_d_clicks:
        df_header = ['posNED_m_2', 'posCmdNED_m_2']
        df_header_2 = ['strCtrlStruct']
        prev_pos_d_clicks = pos_d_clicks

    figure = make_subplots(
        specs=[[{"secondary_y": True}]],
        shared_xaxes=True
    )
    figure.update_layout(height=675,
                         margin=dict(r=20, b=10, l=10, t=10))
    x_title = 'dateTime'
    try:
        if 'diffTime' in df_header:
            figure.add_trace(go.Histogram(x=df['diffTime']))
            config = dict({'displaylogo': False})
            return figure, config
        else:
            for y_title in df_header:
                figure.add_trace(go.Scatter(
                    x=df[x_title], y=df[y_title], name=y_title,
                    mode='lines',
                    line=dict(width=3)),
                    secondary_y=False
                )
    except Exception as e:
        print(e)
    try:
        for y_title in df_header_2:
            figure.add_trace(go.Scatter(
                x=df[x_title], y=df[y_title], name=y_title,
                mode='lines',
                line=dict(width=3)),
                secondary_y=True
            )
    except Exception as e:
        print(e)
    try:
        plot_secondary_y = False
        if (df_header is None) or (len(df_header) == 0):
            plot_secondary_y = True
        elif (df_header_2 is None) or (len(df_header_2) == 0):
            plot_secondary_y = False
        for idx in range(len(fcMcMode_index)-1):
            figure.add_vrect(
                x0=df.iloc[fcMcMode_index[idx]].dateTime,
                x1=df.iloc[fcMcMode_index[idx+1]].dateTime,
                line_width=0,
                annotation_text=fcMcMode_value[idx],
                annotation_position="top left",
                fillcolor=fcMcMode_color[idx],
                layer="below",
                opacity=0.2,
                secondary_y=plot_secondary_y
            )
    except Exception as e:
        print(e)
    figure.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=slide_ranger_toggle,
                thickness=0.1
            )
        )
    )
    config = dict({'displaylogo': False,
                   'scrollZoom': True
                   })
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
        height=630,
        margin=dict(r=20, b=10, l=10, t=10))
    if 'Flight_Path' in value:
        try:
            for job_idx in df['jobSeq'].unique():
                df_jobSeq = df[df['jobSeq'] == job_idx]
                figure_3d.add_trace(go.Scatter3d(
                    x=df_jobSeq['posNED_m_1'],
                    y=df_jobSeq['posNED_m_0'],
                    z=-df_jobSeq['posNED_m_2'],
                    name='Flight Path (jobSeq = ' + str(job_idx) + ')',
                    mode='lines',
                    line=dict(color=-df_jobSeq['rosTime'],
                              colorscale='Viridis', width=6),
                    text=df_jobSeq['strFcMcMode'],
                    customdata=df_jobSeq['dateTime'],
                    hovertemplate=
                        'fcMcMode: <b>%{text}</b><br>' +
                        'X: %{x}<br>' +
                        'Y: %{y}<br>' +
                        'Z: %{z}<br>' +
                        'Time: %{customdata}'
                ))
        except Exception as e:
            print(e)
    if 'Lidar_PC' in value:
        try:
            figure_3d.add_trace(go.Scatter3d(
                x=df_pc['y'], y=df_pc['x'], z=-df_pc['z'],
                name='Lidar Point Cloud',
                mode='markers',
                marker=dict(size=3)))
        except Exception as e:
            print(e)
    config_3d = dict({'displaylogo': False})
    return figure_3d, config_3d


if __name__ == '__main__':
    while(True):
        try:
            app.run_server(debug=True, host='127.0.0.1')
        except Exception as e:
            print(e)
