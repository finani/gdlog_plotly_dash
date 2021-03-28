#include <model/types.h>
#include <stdio.h>
#include <unistd.h>
#include <cstdint>
#include <cstring>
#include <ctime>
#include <iostream>
#include <nlab/math.hpp>
#include <vector>
#include "dirent.h"

#define GetCurrentDir getcwd

using std::string;
using std::vector;
using nlab::lib::Vector3;
using nlab::lib::Vector3f;
using nlab::lib::Quaternionf;
using nlab::lib::Eulerf;
using nlab::lib::Dcmf;

void parseLog(string binDir, string txtDir, nlab::FcLogData &fcLogging_) {
  FILE *logFpBin_;
  FILE *logFpTxt_;

  logFpBin_ = fopen(binDir.c_str(), "rb");
  logFpTxt_ = fopen(txtDir.c_str(), "wt");

  if (logFpBin_ == NULL) {
    perror("error .bin fopen");
    return;
  }
  if (logFpTxt_ == NULL) {
    perror("error .csv fopen");
    return;
  }

  fprintf(logFpTxt_,
          "rosTime, flightMode, ctrlDeviceStatus, "
          "fcMcMode, nSat, gpsFix, jobSeq, "
          "velNedGps_0, velNedGps_1, velNedGps_2, "
          "posNed_0, posNed_1, posNed_2, "
          "velNed_0, velNed_1, velNed_2, "
          "rpy_0, rpy_1, rpy_2, "
          "yawSpType, "  // 20
          "ctrlUser, ctrlStruct, ctrlSetpointType, ctrlOutputType, "
          "ctrlSp_0, ctrlSp_1, ctrlSp_2, "
          "ctrlOp_0, ctrlOp_1, ctrlOp_2, yawSp, "
          "rcRoll, rcPitch, rcYaw, rcThrottle, "  // 20+15
          "GpsNSV, RtkHealthFlag, GpsFusedNSV, GpHealth, "
          "posGPS_0, posGPS_1, posGPS_2, "
          "posRTK_0, posRTK_1, posRTK_2, "
          "posGpsFused_0, posGpsFused_1, posGpsFused_2, "
          "posGp_0, posGp_1, posGp_2, "
          "errLatMix, errLatVis, errLatLid, cmdLatVelIgain, cmdLatVelMix, "
          "errLatMixRate, errLatMixCov00, errLatMixCov11, "  // 20+15+24
          "vbx, vby, vbz, "
          "AcWarnStat, AcHorWarnAC, AcVerWarnAC, "
          "AcXRel, AcYRel, AcZRel, "
          "AcHorWarnRange, AcHorWarnAngle, AcVerWarnRange, AcVerWarnAngle, "
          "LidarDist, LidarAngle, LidarRaw_0, LidarRaw_1, LidarRaw_2, LidarRaw_3, LidarRaw_4, LidarRaw_5, LidarRaw_6, "
          "LidarRaw_7,  "  // 20+15+24+15+8
          "LongVelCmd, LatVelCmd, HeaveVelCmd, "
          "velCtrlI_u, velCtrlI_v, velCtrlI_d, "
          "posCtrlI_N, posCtrlI_E, posCtrlI_D, "
          "gimbalRollCmd, gimbalPitchCmd, gimbalYawCmd, gimbalRoll, gimbalPitch, gimbalYaw, "  // 20+15+24+15+8+15
          "windStatus, windSpeed, windAngle, windQueryTime, windResponseTime, "
          "acousticTemp, tempQueryTime, tempResponseTime, "
          "accBody_0, accBody_1, accBody_2, "
          "trajUnitVectorT_0, trajUnitVectorT_1, trajUnitVectorT_2, "
          "trajUnitVectorN_0, trajUnitVectorN_1, trajUnitVectorN_2, "
          "trajUnitVectorB_0, trajUnitVectorB_1, trajUnitVectorB_2, "
          "trajCmd_T, trajCmd_N, trajCmd_B, "
          "StdJobLongPidErr, StdJobLongPidRate, StdJobLongPidIgain, "
          "GuideModeLongPidErr, GuideModeLongPidRate, GuideModeLongPidIgain, "  // 20+15+24+15+8+15+11+18
          "pqr_0, pqr_1, pqr_2, "
          "rpdCmd_0, rpdCmd_1, rpdCmd_2, "
          "velCmdNav_0, velCmdNav_1, velCmdNav_2, "
          "posCmdNed_0, posCmdNed_1, posCmdNed_2, "
          "missionType, jobType, "
          "bladeTravelDistance, "
          "trajTimeCur, trajTimeMax\n");  // 20+15+24+15+8+15+11+18+17

  while (fread(&fcLogging_, sizeof(nlab::FcLogData), 1, logFpBin_) == 1) {
    if (fprintf(logFpTxt_,
                "%.8lf, %d, %d, "
                "%d, %d, %d, %d, "
                "%.5f, %.5f, %.5f, "
                "%.5f, %.5f, %.5f, "
                "%.5f, %.5f, %.5f, "
                "%.5f, %.5f, %.5f, "
                "%d, "  // 20
                "%d, %d, %d, %d, "
                "%.5f, %.5f, %.5f, "
                "%.5f, %.5f, %.5f, %.5f, "
                "%.2f, %.2f, %.2f, %.2f, "  // 20+15
                "%d, %d, %d, %d, "
                "%.15f, %.15f, %.5f, "
                "%.15f, %.15f, %.5f, "
                "%.15f, %.15f, %.5f, "
                "%.15f, %.15f, %.5f, "
                "%.4f, %.4f, %.4f, %.4f, %.4f, "
                "%.4f, %.4f, %.4f, "  // 20+15+24
                "%.5f, %.5f, %.5f, "
                "%d, %d, %d, "
                "%.5f, %.5f, %.5f, "
                "%.5f, %.5f, %.5f, %.5f, "
                "%.5f, %.5f, %.5f, %.5f, %.5f, %.5f, %.5f, %.5f, %.5f, %.5f,"  // 20+15+24+15+8
                "%.5f, %.5f, %.5f, "
                "%.5f, %.5f, %.5f, "
                "%.5f, %.5f, %.5f, "
                "%.5f, %.5f, %.5f,%.5f, %.5f, %.5f, "  // 20+15+24+15+8+15
                "%d, %.1f, %d, %.3lf, %.3lf, %.1f, %.3lf, %.3lf, "
                "%.5f, %.5f, %.5f, "  // 20+15+24+15+8+15+11
                "%.5f, %.5f, %.5f, %.5f, %.5f, %.5f, "
                "%.5f, %.5f, %.5f, %.5f, %.5f, %.5f, "
                "%.5f, %.5f, %.5f, %.5f, %.5f, %.5f, "  // 20+15+24+15+8+15+11+18
                "%.5f, %.5f, %.5f, "
                "%.5f, %.5f, %.5f, "
                "%.5f, %.5f, %.5f, "
                "%.5f, %.5f, %.5f, "
                "%d, %d, "
                "%.4f, "
                "%.4f, %.4f \n",  // 20+15+24+15+8+15+11+18+17

                fcLogging_.rosTime,
                fcLogging_.flightMode, fcLogging_.ctrlDeviceStatus, fcLogging_.fcMcMode, fcLogging_.nSat,
                fcLogging_.gpsFix, fcLogging_.jobSeq, fcLogging_.velNedGps_0, fcLogging_.velNedGps_1,
                fcLogging_.velNedGps_2, fcLogging_.posNed_0, fcLogging_.posNed_1, fcLogging_.posNed_2,
                fcLogging_.velNed_0, fcLogging_.velNed_1, fcLogging_.velNed_2, fcLogging_.attEulerDeg_0,
                fcLogging_.attEulerDeg_1, fcLogging_.attEulerDeg_2,
                fcLogging_.yCmdType,  // 20

                fcLogging_.ctrlUser, fcLogging_.ctrlStruct, fcLogging_.ctrlSetpointType, fcLogging_.ctrlOutputType,
                fcLogging_.ctrlSetpoint_0, fcLogging_.ctrlSetpoint_1, fcLogging_.ctrlSetpoint_2,
                fcLogging_.ctrlOutput_0, fcLogging_.ctrlOutput_1, fcLogging_.ctrlOutput_2, fcLogging_.yCmdDeg,
                fcLogging_.rcRoll, fcLogging_.rcPitch, fcLogging_.rcYaw, fcLogging_.rcThrottle,  // 20+15

                fcLogging_.posGpsNSV, fcLogging_.posRtkHealthFlag, fcLogging_.posGpsFusedNSV, fcLogging_.posGpHealth,
                fcLogging_.posGPS_0, fcLogging_.posGPS_1, fcLogging_.posGPS_2, fcLogging_.posRTK_0, fcLogging_.posRTK_1,
                fcLogging_.posRTK_2, fcLogging_.posGpsFused_0, fcLogging_.posGpsFused_1, fcLogging_.posGpsFused_2,
                fcLogging_.posGP_0, fcLogging_.posGP_1, fcLogging_.posGP_2, fcLogging_.errLatMix, fcLogging_.errLatVis,
                fcLogging_.errLatLid, fcLogging_.cmdLatVelIgain, fcLogging_.cmdLatVelMix, fcLogging_.errLatMixRate,
                fcLogging_.errLatMixCov00, fcLogging_.errLatMixCov11,  // 20+15+24

                fcLogging_.velBody_0, fcLogging_.velBody_1, fcLogging_.velBody_2, fcLogging_.AcWarnStat,
                fcLogging_.AcHorWarnAC, fcLogging_.AcVerWarnAC, fcLogging_.AcXRel, fcLogging_.AcYRel, fcLogging_.AcZRel,
                fcLogging_.AcHorWarnRange, fcLogging_.AcHorWarnAngleDeg, fcLogging_.AcVerWarnRange,
                fcLogging_.AcVerWarnAngleDeg, fcLogging_.LidarDist, fcLogging_.LidarAngleDeg,  // 20+15+24+15
                fcLogging_.LidarRaw_0, fcLogging_.LidarRaw_1, fcLogging_.LidarRaw_2, fcLogging_.LidarRaw_3,
                fcLogging_.LidarRaw_4, fcLogging_.LidarRaw_5, fcLogging_.LidarRaw_6, fcLogging_.LidarRaw_7,
                // 20+15+24+15+8

                fcLogging_.longVelCmd, fcLogging_.latVelCmd, fcLogging_.heaveVelCmd, fcLogging_.velCtrlI_u,
                fcLogging_.velCtrlI_v, fcLogging_.velCtrlI_d, fcLogging_.posCtrlI_0, fcLogging_.posCtrlI_1,
                fcLogging_.posCtrlI_2, fcLogging_.gimbalRPYCmdDeg_0, fcLogging_.gimbalRPYCmdDeg_1, fcLogging_.gimbalRPYCmdDeg_2, fcLogging_.gimbalRPYDeg_0, fcLogging_.gimbalRPYDeg_1,
                fcLogging_.gimbalRPYDeg_2,  // 20+15+24+15+8+15

                fcLogging_.windStatus, fcLogging_.windSpeed, fcLogging_.windAngle, fcLogging_.windQueryTime,
                fcLogging_.windResponseTime, fcLogging_.acousticTemp, fcLogging_.tempQueryTime,
                fcLogging_.tempResponseTime, fcLogging_.accBody_0, fcLogging_.accBody_1, fcLogging_.accBody_2,
                fcLogging_.trajUnitVectorT_0, fcLogging_.trajUnitVectorT_1, fcLogging_.trajUnitVectorT_2,
                fcLogging_.trajUnitVectorN_0, fcLogging_.trajUnitVectorN_1, fcLogging_.trajUnitVectorN_2,
                fcLogging_.trajUnitVectorB_0, fcLogging_.trajUnitVectorB_1, fcLogging_.trajUnitVectorB_2,
                fcLogging_.trajCmd_T, fcLogging_.trajCmd_N, fcLogging_.trajCmd_B, fcLogging_.StdJobLongPidErr,
                fcLogging_.StdJobLongPidRate, fcLogging_.StdJobLongPidIgain, fcLogging_.GuideModeLongPidErr,
                fcLogging_.GuideModeLongPidRate, fcLogging_.GuideModeLongPidIgain,  // 20+15+24+15+8+12+11+18
                fcLogging_.pqr_0, fcLogging_.pqr_1, fcLogging_.pqr_2, fcLogging_.rpdCmd_0, fcLogging_.rpdCmd_1,
                fcLogging_.rpdCmd_2, fcLogging_.velCmdNav_0, fcLogging_.velCmdNav_1, fcLogging_.velCmdNav_2,
                fcLogging_.posCmdNed_0, fcLogging_.posCmdNed_1, fcLogging_.posCmdNed_2, fcLogging_.missionType,
                fcLogging_.jobType, fcLogging_.bladeTravelDistance, fcLogging_.trajTimeCur,
                fcLogging_.trajTimeMax) < 0)  // 20+15+24+15+8+15+11+18+17
    {
      break;
    }
  }
  fclose(logFpBin_);
  fclose(logFpTxt_);
}

char *GetFileExtension(char *file_name) {
  int file_name_len = strlen(file_name);
  file_name += file_name_len;

  char *file_ext;
  for (int i = 0; i < file_name_len; i++) {
    if (*file_name == '.') {
      file_ext = file_name + 1;
      break;
    }
    file_name--;
  }
  return file_ext;
}

std::string GetCurrentWorkingDir() {
  char buff[FILENAME_MAX];
  GetCurrentDir(buff, FILENAME_MAX);
  std::string current_working_dir(buff);
  return current_working_dir;
}

int main(int argc, char *argv[]) {
  printf("argc = %d\n", argc);
  for (int i = 0; i < argc; i++) printf("argv[%d] = %s\n", i, argv[i]);

  struct dirent *ent;
  DIR *dir;
  nlab::FcLogData fcLogging_;

  if (argc == 1) {
    string current_dir = GetCurrentWorkingDir();

    system(("mkdir -p " + current_dir + "/gdLogCsv").c_str());

    if ((dir = opendir(current_dir.c_str())) != NULL) {
      while ((ent = readdir(dir)) != NULL) {
        char *ptr = GetFileExtension(ent->d_name);
        if (ptr && strcmp(ptr, "bin") == 0) {
          printf("%s\n", ent->d_name);
          string binFileName = ent->d_name;
          auto binDir = current_dir + "/" + binFileName;
          auto txtFileName = binFileName.substr(0, binFileName.find_last_of('.')) + ".csv";
          printf("%s\n", txtFileName.c_str());
          auto txtDir = current_dir + "/gdLogCsv/" + txtFileName;

          parseLog(binDir, txtDir, fcLogging_);
        }
      }
      closedir(dir);
    } else {
      perror("error reading dir");
      return EXIT_FAILURE;
    }

    return 0;
  } else {
    DIR *logFolderDir;
    struct dirent *logFolderEnt;

    string logTimePath;
    string logPath = argv[1];

    if ((dir = opendir(logPath.c_str())) != NULL) {
      while ((logFolderEnt = readdir(dir)) != NULL) {
        logTimePath = logPath + logFolderEnt->d_name;
        if ((logFolderDir = opendir(logTimePath.c_str())) != NULL) {
          while ((ent = readdir(logFolderDir)) != NULL) {
            if (strstr(ent->d_name, ".bin")) {
              if (strstr(ent->d_name, "gdLog")) {
                string binFileName = ent->d_name;

                auto binDir = logTimePath + "/" + binFileName;
                printf("Binary File Name: %s\n", binFileName.c_str());
                //                printf("Binary File DIR: %s\n", binDir.c_str());

                auto txtFileName = binFileName.substr(0, binFileName.find_last_of('.')) + ".csv";
                auto txtDir = logTimePath + "/" + txtFileName;
                printf("Txt File Name: %s\n", txtFileName.c_str());
                //                printf("Txt File DIR: %s\n", txtDir.c_str());

                parseLog(binDir, txtDir, fcLogging_);
              }
            }
          }
          closedir(logFolderDir);
        }
      }
      closedir(dir);
    } else {
      perror("error reading dir");
      return EXIT_FAILURE;
    }
    return 0;
  }
}
