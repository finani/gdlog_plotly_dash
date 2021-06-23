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
    def __init__(self):
        self.fcLogVersion = 0
        self.csv_header_list = []
        self.bin_data_length = 616
        self.bin_data_type = 'd6B12fB4B3d4f4fHBHB12d8f3f3B7f10f3f6f6fBfB2df2d3f12f6f3f9f2B3f4B'
        self.logging_hz = 50

        self.csv_header_list = [
            'rosTime', 'flightMode', 'ctrlDeviceStatus',
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

    def run(self, bin_file_path):
        print("")
        print("")
        print("    Parsing Start!")
        print(bin_file_path)
        print("")
        with open(bin_file_path, 'rb') as f_bin:
            chunk = f_bin.read()
            if chr(chunk[0]) == 'n':
                self.fcLogVersion = chunk[1]
                print(self.fcLogVersion)
                FcLogHeaderSize = chunk[3] << 8 | chunk[2]
                FcLogTypeListSize = chunk[5] << 8 | chunk[4]
                FcLogDataSize = chunk[7] << 8 | chunk[6]
                FcLogHeader = chunk[8:8+FcLogHeaderSize].decode('ascii')
                FcLogTypeList = chunk[8+FcLogHeaderSize:8+FcLogHeaderSize+FcLogTypeListSize].decode('ascii')

                self.csv_header_list = FcLogHeader.split(",")
                self.bin_data_type = '='+FcLogTypeList # Byte order: native, Size: standard
                self.bin_data_length = FcLogDataSize

                chunk = chunk[8+FcLogHeaderSize+FcLogTypeListSize:]
            chunk = chunk[0:len(chunk)//self.bin_data_length*self.bin_data_length]
            print("data_number: " + str(len(chunk)//self.bin_data_length))
            data_count = 0
            with open(bin_file_path.split('.')[0] + '.csv', 'w', encoding='utf-8') as f_csv:
                wr = csv.writer(f_csv)
                wr.writerow(self.csv_header_list)
                for unpacked_chunk in struct.iter_unpack(self.bin_data_type, chunk):
                    wr.writerow(list(unpacked_chunk))
                    if data_count % 3000 == 0:
                        print("data_count: " + str(data_count) + "\tlogging_time: " + "%d"%(data_count/self.logging_hz//60) + " m " + "%2.2f"%(data_count/self.logging_hz%60) + " s")
                    data_count += 1
                print("")
                print("total_data_count: " + str(data_count) + "\ttotal_logging_time: " + "%d"%(data_count/self.logging_hz//60) + " m " + "%2.2f"%(data_count/self.logging_hz%60) + " s")
                print("Saved: " + f_csv.name)


if __name__ == '__main__':
    if len(sys.argv) == 1:  # for test run
        bin_path = "gdLog_210601_102129.bin"
        print("Test run gdlog_parser.py using \'gdLog_210601_102129.bin\'\n")
        print("\tUsage: python3 gdlog_parser.py ~/log 210601\n")
    elif len(sys.argv) == 2: # for all subfolder
        dir_path = sys.argv[1]
        dir_path_included = '_'
    elif len(sys.argv) == 3:
        dir_path = sys.argv[1]
        dir_path_included = sys.argv[2]
    else:
        raise SystemExit(
            '\tUsage: python3 gdlog_parser.py ~/log 210601\n')

    gdlog_parser = GDLOG_PARSER()

    file_paths = []
    for root, dirs, filenames in os.walk(dir_path):
        for filename in filenames:
            if dir_path_included in root.split('/')[-1][0:7] and 'gdLog' in filename and 'bin' in filename:
                gdlog_parser.run(root + '/' + filename)
                file_paths.append(root + '/' + filename.split('.')[0] + '.csv')

    print("")
    print("    All Done!")
    for file_path in file_paths:
        print(file_path)
    print("")
