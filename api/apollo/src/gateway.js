const { ApolloServer } = require('apollo-server');
const { ApolloGateway, RemoteGraphQLDataSource, IntrospectAndCompose } = require("@apollo/gateway");
require('dotenv').config()

// For more information on how to add information to http headers and github docs, use https://www.apollographql.com/docs/federation/gateway/ goto Customzing requests and expand the example
class AuthenticatedDataSource extends RemoteGraphQLDataSource {
  willSendRequest({ request, context }) {
    request.http.headers.set('Authorization', context.token);
    request.http.headers.set('service-name', context.serviceName);
    request.http.headers.set('user-ip', context.userIP);
  }
}

var url = '';
var subgraphsENV = []
var env_var_list = process.env 

Object.keys(env_var_list).forEach(function(key) {
  if (key.match("APP_PORT_")){
    var key_name = key.replace("APP_PORT_","").toLowerCase()
    var value = env_var_list[key]
    var service_name = process.env.MOVIE_FAV_ENV === 'local' ? "localhost" : key_name;
    url = 'http://' + service_name + ':' + value;
    console.log("Adding: " + key_name + ' -> ' + url);
    subgraphsENV.push({name: key_name, url: url});
  }
})

const gateway = new ApolloGateway({
  supergraphSdl: new IntrospectAndCompose({subgraphs: subgraphsENV}),
  buildService({ name, url }) {
    return new AuthenticatedDataSource({ url });
  },
});

const server = new ApolloServer({
  gateway,
  subscriptions: false,
  playground: true,
  introspection: true,
  cors: {
		origin: '*',			// <- allow request from all domains
		credentials: true, 	// <- enable CORS response for requests with credentials (cookies, http authentication)
  },
  context: ({ req }) => {
    // Get the user token from the headers.
    const token = req.headers.authorization || '';
    const serviceName = req.headers["service-name"]|| '';
    const userIP = req.header('x-forwarded-for') || req.connection.remoteAddress;

   // this will pass along the additional header info in the request to the context
   return { token, serviceName, userIP };
  }	
});


server.listen().then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
});