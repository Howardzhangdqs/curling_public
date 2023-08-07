cmake_minimum_required(VERSION 3.27)
project(hello)

find_package(OpenCV REQUIRED)
include_directories(${OPENCV_INCLUDE_DIRS})

add_executable(hello main.cpp)

target_link_libraries(
    hello
    ${OPENCV_LIBS}
)