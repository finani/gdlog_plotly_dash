# gdlog_tools_python
## Install dependencies
```sudo apt install git-lfs python3-pandas```

## Run gdlog_tools.py
```python3 gdlog_tools.py path_of_your_csv_file or path_of_your_bin_file```

## parser Output
```
/home/weebee/catkin_ws/src/gdlog_plot_python/gdLog_210323_172626.bin Parsing Start!

data_number: 109667
data_count: 0	logging_time: 0 m 0.00 s
data_count: 3000	logging_time: 1 m 0.00 s
data_count: 6000	logging_time: 2 m 0.00 s
data_count: 9000	logging_time: 3 m 0.00 s
data_count: 12000	logging_time: 4 m 0.00 s
data_count: 15000	logging_time: 5 m 0.00 s
data_count: 18000	logging_time: 6 m 0.00 s
data_count: 21000	logging_time: 7 m 0.00 s
data_count: 24000	logging_time: 8 m 0.00 s
data_count: 27000	logging_time: 9 m 0.00 s
data_count: 30000	logging_time: 10 m 0.00 s
data_count: 33000	logging_time: 11 m 0.00 s
data_count: 36000	logging_time: 12 m 0.00 s
data_count: 39000	logging_time: 13 m 0.00 s
data_count: 42000	logging_time: 14 m 0.00 s
data_count: 45000	logging_time: 15 m 0.00 s
data_count: 48000	logging_time: 16 m 0.00 s
data_count: 51000	logging_time: 17 m 0.00 s
data_count: 54000	logging_time: 18 m 0.00 s
data_count: 57000	logging_time: 19 m 0.00 s
data_count: 60000	logging_time: 20 m 0.00 s
data_count: 63000	logging_time: 21 m 0.00 s
data_count: 66000	logging_time: 22 m 0.00 s
data_count: 69000	logging_time: 23 m 0.00 s
data_count: 72000	logging_time: 24 m 0.00 s
data_count: 75000	logging_time: 25 m 0.00 s
data_count: 78000	logging_time: 26 m 0.00 s
data_count: 81000	logging_time: 27 m 0.00 s
data_count: 84000	logging_time: 28 m 0.00 s
data_count: 87000	logging_time: 29 m 0.00 s
data_count: 90000	logging_time: 30 m 0.00 s
data_count: 93000	logging_time: 31 m 0.00 s
data_count: 96000	logging_time: 32 m 0.00 s
data_count: 99000	logging_time: 33 m 0.00 s
data_count: 102000	logging_time: 34 m 0.00 s
data_count: 105000	logging_time: 35 m 0.00 s
data_count: 108000	logging_time: 36 m 0.00 s
total_data_count: 109667	total_logging_time: 36 m 33.34 s
Saved: /home/weebee/catkin_ws/src/gdlog_plot_python/gdLog_210323_172626.csv
```

## plotter Guide

```
Welcome to gdlog_plotter

[preset_name]

('a', ['rpy', 'velNed', 'posNed'])
('b', ['accBody', 'pqr'])
('c', ['vbxyz'])
('px4', ['fcMcMode', 'rpy', 'velNed', 'posNed'])


[data_name]

acHorWarnAC: 1		acHorWarnAngle: 1	acHorWarnRange: 1
acVerWarnAC: 1		acVerWarnAngle: 1	acVerWarnRange: 1
acWarnStat: 1		acXYZRel: 3		accBody: 3
acousticTemp: 1		

bladeTravelDistance: 1	

cmdLatVelIgain: 1	cmdLatVelMix: 1		ctrlDeviceStatus: 1
ctrlOp: 3		ctrlOutputType: 1	ctrlSetpointType: 1
ctrlSp: 3		ctrlStruct: 1		ctrlUser: 1

errLatLid: 1		errLatMix: 1		errLatMixCov00: 1
errLatMixCov11: 1	errLatMixRate: 1	errLatVis: 1

fcMcMode: 1		flightMode: 1		

gimbalRPY: 3		gimbalRPYCmd: 3		gpHealth: 1
gpsFix: 1		gpsFusedNSV: 1		gpsNSV: 1
guideModeLongPidErr: 1	guideModeLongPidIgain: 1	guideModeLongPidRate: 1

jobSeq: 1		jobType: 1		

lidarAngle: 1		lidarDist: 1		lidarRaw: 8

missionType: 1		

nSat: 1			

pad: 2			posCmdNed: 3		posCtrlINED: 3
posGPS: 3		posGp: 3		posGpsFused: 3
posNed: 3		posRTK: 3		pqr: 3

rcRPYT: 4		rosTime: 1		rosTimeDiff: 1
rpdCmd: 3		rpy: 3			rtkHealthFlag: 1

stdJobLongPidErr: 1	stdJobLongPidIgain: 1	stdJobLongPidRate: 1

tempQueryTime: 1	tempResponseTime: 1	trajCmdTNB: 3
trajTimeCur: 1		trajTimeMax: 1		trajUnitVectorTNB0: 3
trajUnitVectorTNB1: 3	trajUnitVectorTNB2: 3	

vbxyz: 3		velCmdLongLatHeave: 3	velCmdNav: 3
velCtrlIuvw: 3		velNed: 3		velNedGps: 3

windAngle: 1		windQueryTime: 1	windResponseTime: 1
windSpeed: 1		windStatus: 1		

yawSp: 1		yawSpType: 1		


[Command]

	[help] Open Guide

	[show] Plot preset
		[preset_name1] [preset_name2] ...

	[plot] Plot data from header
		[data_name1] [data_name2] ...

	[range] Set range   [cur] 0-109667, [max] 109667
		[start_number] [end_number]

	[save] Save plot (.png)
		[all] save all figures
		[png_file_name_to_save] save the recent figure

	[clear] Clear plots

	[q] Close gdlog_plotter


	Usage: [show, plot, range, save, clear, q] sub_command_data


plotter> 
```
