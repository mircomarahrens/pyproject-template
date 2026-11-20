# C++ Roll-Dice Microservice (`dice-server`)

This C++ microservice provides a high-performance HTTP service implementing the same OpenTelemetry tracing concepts as the Python FastAPI application, allowing for direct architectural, throughput, and memory footprint comparisons.

## Architecture

- **Web Framework**: [Oat++](https://oatpp.io/) (high-performance C++ web server).
- **Observability**: [OpenTelemetry C++ SDK](https://github.com/open-telemetry/opentelemetry-cpp) with in-code manual span lifecycle management (`InitTracer`, `StartSpan`, `End`, `CleanupTracer`).
- **Endpoint**: `GET /rolldice` on port `8080`, returning an integer (1–6) simulating a random dice roll while producing trace spans.

## Prerequisites

- CMake 3.25+
- C++20 compliant compiler (GCC 11+, Clang 13+, MSVC 2019+)
- Internet connection during initial build (CMake `FetchContent` downloads and builds Oat++ and OpenTelemetry C++ SDK automatically).

## Building Locally

From the `cpp/` directory:

```bash
cmake -S roll-dice -B out -DCMAKE_BUILD_TYPE=Release
cmake --build out -- -j$(nproc)
```

## Running the Service

```bash
./out/dice-server
```

In another terminal, test the endpoint:

```bash
curl http://localhost:8080/rolldice
```

The server responds with the rolled number (e.g., `5`) and outputs the generated OpenTelemetry trace span details to standard output.
