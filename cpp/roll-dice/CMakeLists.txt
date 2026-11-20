cmake_minimum_required(VERSION 3.25)
project(RollDiceServer CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)

# 1. Fetch Oat++ (disable test suite)
set(OATPP_BUILD_TESTS OFF CACHE BOOL "" FORCE)

FetchContent_Declare(
    oatpp
    GIT_REPOSITORY https://github.com/oatpp/oatpp.git
    GIT_TAG        1.3.0-latest
    GIT_SHALLOW    TRUE
)

# 2. Fetch OpenTelemetry C++ SDK (disable test suites)
set(BUILD_TESTING OFF CACHE BOOL "" FORCE)
set(WITH_EXAMPLES OFF CACHE BOOL "" FORCE)
set(WITH_BENCHMARK OFF CACHE BOOL "" FORCE)
set(WITH_STL ON CACHE BOOL "" FORCE)
set(WITH_OTLP_HTTP ON CACHE BOOL "" FORCE)
set(WITH_OTLP_GRPC OFF CACHE BOOL "" FORCE)

FetchContent_Declare(
    opentelemetry-cpp
    GIT_REPOSITORY https://github.com/open-telemetry/opentelemetry-cpp.git
    GIT_TAG        v1.30.0
    GIT_SHALLOW    TRUE
)

FetchContent_MakeAvailable(oatpp opentelemetry-cpp)

# 3. Target
add_executable(dice-server main.cpp)

target_link_libraries(dice-server PRIVATE
    oatpp
    opentelemetry_trace
    opentelemetry_exporter_otlp_http
    opentelemetry_resources
)
