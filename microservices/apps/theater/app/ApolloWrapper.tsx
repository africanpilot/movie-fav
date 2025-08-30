"use client";

import { HttpLink, from } from "@apollo/client";
import {
  ApolloNextAppProvider,
  ApolloClient,
  InMemoryCache,
} from "@apollo/experimental-nextjs-app-support";
import { setContext } from "@apollo/client/link/context";
import { onError } from "@apollo/client/link/error";

// have a function to create a client for you
function makeClient() {
  // configure error handlers
  const errorLink = onError(({ graphQLErrors, networkError }) => {
      if (networkError) {
          console.log("networkError!!", networkError);
          console.log(typeof networkError);
          console.log(JSON.stringify(networkError, null, 2));
      }
  })

  const gateway =
      process.env.NEXT_PUBLIC_APP_DEFAULT_ENV !== "prod"
      ? process.env.NEXT_PUBLIC_REACT_APP_GATEWAY_DEVELOPMENT
      : process.env.NEXT_PUBLIC_REACT_APP_GATEWAY_PRODUCTION

  const link = from([errorLink, new HttpLink({ 
    uri: gateway,
    fetchOptions: { cache: "no-store" },
  })]);

  const authLink = setContext((_, { headers }) => {
      // get the authentication token from local storage if it exists
      const appToken = localStorage.getItem("theater-app-token");
      const emailToken = localStorage.getItem("theater-email-token");
      const guestToken = localStorage.getItem("theater-guest-token");

      const token = appToken ? appToken
      : emailToken ? emailToken
      : guestToken;
      
      // return the headers to the context so httpLink can read them
      // console.log("token: ", token)
      return {
          headers: {
          ...headers,
          ["service"]: "theater",
          authorization: token ? `Bearer ${token}` : "",
          },
      }
  })

  // use the `ApolloClient` from "@apollo/experimental-nextjs-app-support"
  return new ApolloClient({
    // use the `InMemoryCache` from "@apollo/experimental-nextjs-app-support"
    link: authLink.concat(link),
    cache: new InMemoryCache(),
  });
}

// you need to create a component to wrap your app in
export function ApolloWrapper({ children }: React.PropsWithChildren) {
  return (
    <ApolloNextAppProvider makeClient={makeClient}>
      {children}
    </ApolloNextAppProvider>
  );
}
