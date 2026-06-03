#include "oatpp/web/server/HttpConnectionHandler.hpp"
#include "oatpp/network/Server.hpp"
#include "oatpp/network/tcp/server/ConnectionProvider.hpp"

#include "opentelemetry/exporters/ostream/span_exporter_factory.h"
#include "opentelemetry/sdk/trace/exporter.h"
#include "opentelemetry/sdk/trace/processor.h"
#include "opentelemetry/sdk/trace/simple_processor_factory.h"
#include "opentelemetry/sdk/trace/tracer_provider_factory.h"
#include "opentelemetry/trace/provider.h"

#include <cstdlib>
#include <ctime>
#include <string>

using namespace std;
namespace trace_api = opentelemetry::trace;
namespace trace_sdk = opentelemetry::sdk::trace;
namespace trace_exporter = opentelemetry::exporter::trace;

namespace {
  void InitTracer() {
    auto exporter  = trace_exporter::OStreamSpanExporterFactory::Create();
    auto processor = trace_sdk::SimpleSpanProcessorFactory::Create(std::move(exporter));
    std::shared_ptr<opentelemetry::trace::TracerProvider> provider =
      trace_sdk::TracerProviderFactory::Create(std::move(processor));
    //set the global trace provider
    trace_api::Provider::SetTracerProvider(provider);
  }
  void CleanupTracer() {
    std::shared_ptr<opentelemetry::trace::TracerProvider> none;
    trace_api::Provider::SetTracerProvider(none);
  }

}

class Handler : public oatpp::web::server::HttpRequestHandler {
public:
  shared_ptr<OutgoingResponse> handle(const shared_ptr<IncomingRequest>& request) override {
    auto tracer = opentelemetry::trace::Provider::GetTracerProvider()->GetTracer("my-app-tracer");
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
  auto connectionProvider = oatpp::network::tcp::server::ConnectionProvider::createShared({"localhost", 8080, oatpp::network::Address::IP_4});
  oatpp::network::Server server(connectionProvider, connectionHandler);
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
