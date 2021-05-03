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

# import gdlog_parser

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, prevent_initial_callbacks=True)

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
    dcc.Upload(
        id='input_upload_data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '98%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    html.Hr(), # horizontal line
    html.Label([
        "Data",
        dcc.Dropdown(
            id='io_data_dropdown',
            multi=True,
            placeholder="Select Data",
        ),
    ]),
    dcc.Store(id='df_header_list_sorted'),
    dcc.Graph(
        id='clientside_graph_px'
    ),
    dcc.Store(
        id='clientside_figure_store_px'
    ),
    html.Hr(),
    html.Details([
        html.Summary('Input File Details'),
        html.Div(id='output_data_upload')
    ],
    open=True),
])

def parse_contents(contents, filename, date):
    global df
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), low_memory=False)
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
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
        df = df[df['rosTime'] > 1577840400] # Ignore data before 2020년 January 1일 Wednesday AM 1:00:00
        df.columns = df.columns.str.strip()
        df['dateTime'] = pd.to_datetime(df['rosTime'], unit='s') + pd.DateOffset(hours=9)
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
        html.Hr(), # horizontal line
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ]), df_header_list_sorted


@app.callback(Output('output_data_upload', 'children'),
              Output('df_header_list_sorted', 'data'),
              Output('io_data_dropdown', 'options'),
              Input('input_upload_data', 'contents'),
              State('input_upload_data', 'filename'),
              State('input_upload_data', 'last_modified'))
def update_data_upload(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children, df_header_list_sorted = parse_contents(list_of_contents, list_of_names, list_of_dates)
        options=[ {'label': df_header, 'value': df_header} for df_header in df_header_list_sorted ]
        return children, df_header_list_sorted, options


@app.callback(
    Output('clientside_figure_store_px', 'data'),
    Input('io_data_dropdown', 'value')
)
def update_store_data(df_header):
    global df
    try:
        figure = go.Figure()
        if len(df_header) > 0:
            x_title = 'dateTime'
            for y_title in df_header:
                figure.add_trace(go.Scatter(x=df[x_title], y=df[y_title], name=y_title)) # deleteTraces, FigureWidget
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
    Output('clientside_graph_px', 'figure'),
    Input('clientside_figure_store_px', 'data')
)


if __name__ == '__main__':
    app.run_server(debug=True)