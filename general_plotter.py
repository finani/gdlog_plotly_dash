#!/usr/bin/env python3

import sys
import signal
import base64
import datetime
import io

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

prev_slide_ranger_clicks = 0
slide_ranger_toggle = True

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
    html.Label([
        dcc.Dropdown(
            id='io_data_dropdown',
            multi=False,
            placeholder="Select X Data"
        ),
    ]),
    html.Label([
        dcc.Dropdown(
            id='io_data_dropdown_2',
            multi=True,
            placeholder="Select Y Data"
        )
    ]),
    html.Button('slide_ranger: true',
                id='input_slide_ranger_button',
                n_clicks=0),
    dcc.Graph(id='graph_go')
])


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
            if 'csv' in filename:
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')),
                                    low_memory=False)
                parsing_log = parsing_log + 'csv file!\n'
            elif 'bin' in filename:
                parsing_log = parsing_log + 'bin file! (not supported)\n'
            elif 'xls' in filename:
                df = pd.read_excel(io.BytesIO(decoded))
                parsing_log = parsing_log + 'xls file!\n'

            # dataFrame Post-Processing
            df = df.drop([0])  # delete data with initial value
            df = df.dropna(axis=0)  # delete data with NaN
            df = df.reset_index(drop=True)
            df.columns = df.columns.str.strip()
            df_header_list_sorted = sorted(df.columns.tolist())
            strNames = strNames + filename + '\n'
            strDates = strDates + \
                str(datetime.datetime.fromtimestamp(date)) + '\n'
            strDecoded = strDecoded + str(decoded[0:100]) + '...\n'
        except Exception as e:
            print('[parse_contents::read_files] ' + str(e))
            return html.Div([
                'There was an error processing this file.'
            ])
        confirm_msg = '[Parsing Log]\n' + parsing_log + \
                      '\n[File Names]\n' + strNames + \
                      '\n[Raw Contents]\n' + strDecoded
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
    Input('io_data_dropdown_2', 'value')
)
def update_graph_data(df_header, df_header_2):
    global df
    figure = go.Figure()
    figure.update_layout(height=600,
                         margin=dict(r=20, b=10, l=10, t=10))
    try:
        x_title = df_header
        for y_title in df_header_2:
            figure.add_trace(go.Scatter(
                x=df[x_title], y=df[y_title], name=y_title,
                mode='lines',
                line=dict(width=3)),
            )
    except Exception as e:
        print('[update_graph_data::df_headers] ' + str(e))
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


if __name__ == '__main__':
    while(True):
        try:
            app.run_server(debug=True, host='127.0.0.1')
        except Exception as e:
            print('[__main__::run_server] ' + str(e))
