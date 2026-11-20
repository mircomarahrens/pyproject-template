#include "oatpp/web/server/HttpConnectionHandler.hpp"
#include "oatpp/network/Server.hpp"
#include "oatpp/network/tcp/server/ConnectionProvider.hpp"

#include "opentelemetry/exporters/otlp/otlp_http_exporter_factory.h"
#include "opentelemetry/exporters/otlp/otlp_http_exporter_options.h"
#include "opentelemetry/sdk/resource/resource.h"
#include "opentelemetry/sdk/trace/simple_processor_factory.h"
#include "opentelemetry/sdk/trace/tracer_provider_factory.h"
#include "opentelemetry/trace/provider.h"

#include <cstdlib>
#include <ctime>
#include <memory>
#include <string>

using namespace std;
namespace trace_api = opentelemetry::trace;
namespace trace_sdk = opentelemetry::sdk::trace;
namespace resource_sdk = opentelemetry::sdk::resource;
namespace otlp = opentelemetry::exporter::otlp;

namespace {
  void InitTracer() {
    otlp::OtlpHttpExporterOptions opts;
    const char* endpoint = std::getenv("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT");
    if (!endpoint) {
      endpoint = std::getenv("OTEL_EXPORTER_OTLP_ENDPOINT");
    }
    if (endpoint) {
      std::string url = endpoint;
      if (url.find("/v1/traces") == std::string::npos) {
        if (url.back() != '/') {
          url += "/";
        }
        url += "v1/traces";
      }
      opts.url = url;
    } else {
      opts.url = "http://collector:4318/v1/traces";
    }

    const char* service_name = std::getenv("OTEL_SERVICE_NAME");
    if (!service_name) {
      service_name = "dice-server";
    }

    auto resource = resource_sdk::Resource::Create({
      {"service.name", service_name}
    });

    auto exporter = otlp::OtlpHttpExporterFactory::Create(opts);
    auto processor = trace_sdk::SimpleSpanProcessorFactory::Create(std::move(exporter));
    std::shared_ptr<trace_api::TracerProvider> provider =
      trace_sdk::TracerProviderFactory::Create(std::move(processor), resource);
    // set the global trace provider
    trace_api::Provider::SetTracerProvider(provider);
  }

  void CleanupTracer() {
    std::shared_ptr<trace_api::TracerProvider> none;
    trace_api::Provider::SetTracerProvider(none);
  }
}

class Handler : public oatpp::web::server::HttpRequestHandler {
public:
  shared_ptr<OutgoingResponse> handle(const shared_ptr<IncomingRequest>& request) override {
    auto tracer = opentelemetry::trace::Provider::GetTracerProvider()->GetTracer("dice-server");
    auto span = tracer->StartSpan("RollDiceServer");
    int low = 1;
    int high = 7;
    int random = rand() % (high - low) + low;
    // Convert a std::string to oatpp::String
    const string response = to_string(random);
    span->End();
    return ResponseFactory::createResponse(Status::CODE_200, response.c_str());
  }
};

void run() {
  auto router = oatpp::web::server::HttpRouter::createShared();
  router->route("GET", "/rolldice", std::make_shared<Handler>());
  auto connectionHandler = oatpp::web::server::HttpConnectionHandler::createShared(router);
  auto connectionProvider = oatpp::network::tcp::server::ConnectionProvider::createShared({"0.0.0.0", 8080, oatpp::network::Address::IP_4});
  auto server = oatpp::network::Server(connectionProvider, connectionHandler);
  OATPP_LOGI("Dice Server", "Server running on port %s", static_cast<const char*>(connectionProvider->getProperty("port").getData()));
  server.run();
}

int main() {
  oatpp::base::Environment::init();
  InitTracer();
  srand((int)time(0));
  run();
  oatpp::base::Environment::destroy();
  CleanupTracer();
  return 0;
}
