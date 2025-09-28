const { ApolloServer } = require("@apollo/server");
const { startStandaloneServer } = require("@apollo/server/standalone");
const {
  ApolloGateway,
  RemoteGraphQLDataSource,
  IntrospectAndCompose,
} = require("@apollo/gateway");
require("dotenv").config();

// For more information on how to add information to http headers and github docs, use https://www.apollographql.com/docs/federation/gateway/ goto Customzing requests and expand the example
class AuthenticatedDataSource extends RemoteGraphQLDataSource {
  willSendRequest({ request, context }) {
    request.http.headers.set("Authorization", context.token);
    request.http.headers.set("service", context.serviceName);
    request.http.headers.set("user-ip", context.userIP);
  }
}

var publicSubgraphs = [];
var privateSubgraphs = [];
var env_var_list = process.env;

Object.keys(env_var_list).forEach(function (key) {
  if (key.match("APP_PORT_")) {
    var service_name = key.split("_")[2].toLowerCase();
    var port = env_var_list[key];
    var public_url = `http://${service_name}:${port}/graphql`;
    console.log("Adding Public: " + service_name + " -> " + public_url);
    publicSubgraphs.push({ name: service_name, url: public_url });
    var private_url = `http://${service_name}:${port}/internal/graphql`;
    console.log("Adding Private: " + service_name + " -> " + private_url);
    privateSubgraphs.push({ name: service_name, url: private_url });
  }
});

const publicGateway = new ApolloGateway({
  supergraphSdl: new IntrospectAndCompose({ subgraphs: publicSubgraphs }),
  buildService({ name, url }) {
    return new AuthenticatedDataSource({ url });
  },
});

const privateGateway = new ApolloGateway({
  supergraphSdl: new IntrospectAndCompose({ subgraphs: privateSubgraphs }),
  buildService({ name, url }) {
    return new AuthenticatedDataSource({ url });
  },
});

const publicServer = new ApolloServer({
  gateway: publicGateway,
  introspection: true,
});

const privateServer = new ApolloServer({
  gateway: privateGateway,
  introspection: true,
});

(async () => {
  const { url: publicUrl } = await startStandaloneServer(publicServer, {
    listen: { port: 4000 },
    context: async ({ req }) => {
      // Get the user token from the headers.
      const token = req.headers.authorization || "";
      const serviceName = req.headers["service"] || "";
      const userIP = req.headers["x-forwarded-for"] || req.socket.remoteAddress;

      // this will pass along the additional header info in the request to the context
      return { token, serviceName, userIP };
    },
  });
  console.log(`🚀 Public Server ready at ${publicUrl}`);

  const { url: privateUrl } = await startStandaloneServer(privateServer, {
    listen: { port: 4001 },
    context: async ({ req }) => {
      // Get the user token from the headers.
      const token = req.headers.authorization || "";
      const serviceName = req.headers["service"] || "";
      const userIP = req.headers["x-forwarded-for"] || req.socket.remoteAddress;

      // this will pass along the additional header info in the request to the context
      return { token, serviceName, userIP };
    },
  });
  console.log(`🚀 Private Server ready at ${privateUrl}`);
})();
