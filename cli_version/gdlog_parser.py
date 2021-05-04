#!/usr/bin/env python3

import os
import sys
import signal
import struct
import csv

def signal_handler(signal, frame):
    print('\npressed ctrl + c!!!\n')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

class GDLOG_PARSER:
    def __init__(self, bin_path_):
        self.my_path = os.getcwd()
        self.bin_path = bin_path_
        self.bin_file_name = self.bin_path.split('/')[-1].split('.')[0]
        self.save_path = self.my_path + '/' + self.bin_file_name + '/'
        self.csv_header_list = []
        self.bin_data_type = 'dBBBBBBffffffffffffBBBBBdddffffffffHBHBddddddddddddfffffffffffBBBffffffffffffffffffffffffffffffffBfBddfddfffffffffffffffffffffffffffffffffBBfffHH'
        self.logging_hz = 50

        self.csv_header_list = ['rosTime', 'flightMode', 'ctrlDeviceStatus', 
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

    def run(self):
        print("")
        print(self.bin_path + " Parsing Start!")
        print("")
        with open(self.bin_path, 'rb') as f_bin:
            chunk = f_bin.read()
            chunk = chunk[0:len(chunk)//616*616]
            print("data_number: " + str(len(chunk)//616))
            data_count = 0
            with open(self.bin_path.split('.')[0] + '.csv', 'w', encoding='utf-8') as f_csv:
                wr = csv.writer(f_csv)
                wr.writerow(self.csv_header_list)
                for unpacked_chunk in struct.iter_unpack(self.bin_data_type, chunk):
                    wr.writerow(list(unpacked_chunk))
                    if data_count % 3000 == 0:
                        print("data_count: " + str(data_count) + "\tlogging_time: " + "%d"%(data_count/self.logging_hz//60) + " m " + "%2.2f"%(data_count/self.logging_hz%60) + " s")
                    data_count += 1
                print("total_data_count: " + str(data_count) + "\ttotal_logging_time: " + "%d"%(data_count/self.logging_hz//60) + " m " + "%2.2f"%(data_count/self.logging_hz%60) + " s")
                print("Saved: " + f_csv.name)


if __name__ == '__main__':
    if len(sys.argv) == 1:  # for test run
        bin_path = "gdLog_210323_172626.bin"
        print("Test run gdlog_parser.py using \'gdLog_210323_172626.bin\'\n")
        print("\tUsage: python3 gdlog_parser.py path_of_your_bin_file\n")
    elif len(sys.argv) == 2:
        bin_path = sys.argv[1]
    else:
        raise SystemExit(
            '\tUsage: python3 %s path_of_your_bin_file' % sys.argv[0])

    gdlog_parser = GDLOG_PARSER(bin_path)

    gdlog_parser.run()
