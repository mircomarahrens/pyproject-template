#include "oatpp/web/server/HttpConnectionHandler.hpp"
#include "oatpp/network/Server.hpp"
#include "oatpp/network/tcp/server/ConnectionProvider.hpp"

#include "opentelemetry/exporters/otlp/otlp_http_exporter_factory.h"
#include "opentelemetry/sdk/resource/resource.h"
#include "opentelemetry/sdk/trace/batch_span_processor_factory.h"
#include "opentelemetry/sdk/trace/batch_span_processor_options.h"
#include "opentelemetry/sdk/trace/tracer_provider_factory.h"
#include "opentelemetry/trace/provider.h"

#include <cstdlib>
#include <memory>
#include <random>
#include <string>

namespace trace_api = opentelemetry::trace;
namespace trace_sdk = opentelemetry::sdk::trace;
namespace resource_sdk = opentelemetry::sdk::resource;
namespace otlp = opentelemetry::exporter::otlp;

namespace {
  void InitTracer() {
    const char* service_name = std::getenv("OTEL_SERVICE_NAME");
    auto resource = resource_sdk::Resource::Create({
      {"service.name", service_name ? service_name : "dice-server"}
    });

    auto exporter = otlp::OtlpHttpExporterFactory::Create();
    auto processor = trace_sdk::BatchSpanProcessorFactory::Create(
      std::move(exporter), trace_sdk::BatchSpanProcessorOptions{});
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
  opentelemetry::nostd::shared_ptr<trace_api::Tracer> tracer_ =
      trace_api::Provider::GetTracerProvider()->GetTracer("dice-server");

public:
  std::shared_ptr<OutgoingResponse> handle(const std::shared_ptr<IncomingRequest>& /*request*/) override {
    auto span = tracer_->StartSpan("RollDiceServer");
    auto scope = tracer_->WithActiveSpan(span);

    thread_local std::mt19937 rng{std::random_device{}()};
    std::uniform_int_distribution<int> dist(1, 6);
    // Convert a std::string to oatpp::String
    const std::string response = std::to_string(dist(rng));

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
  run();
  oatpp::base::Environment::destroy();
  CleanupTracer();
  return 0;
}
