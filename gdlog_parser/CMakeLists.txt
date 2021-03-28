cmake_minimum_required(VERSION 2.8.3)
project(gdLogParser)

set(CMAKE_CXX_STANDARD 14)

include_directories(
        ../../src/
)
add_executable(gdLogParser
        main.cpp
        )

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY $HOME/catkin_ws/devel/lib/niv_gnc)