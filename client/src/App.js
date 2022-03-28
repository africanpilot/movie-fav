import React, { useState, useContext } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import AllRoutes from "./routes";
// import withTracker from "./withTracker";

import "bootstrap/dist/css/bootstrap.min.css";
import "./layouts/shards-dashboards.1.1.0.min.css";

import {
  ApolloClient,
  InMemoryCache,
  ApolloProvider,
  HttpLink,
  from,
} from "@apollo/client";
import { onError } from "@apollo/client/link/error";
import { setContext } from "@apollo/client/link/context";
import AuthContextProvider, { AuthContext } from "./util/authContext";


import TokenExpire from "./util/tokenExpire";
// "https://48p1r2roz4.sse.codesandbox.io",

//this will remove all the console when its production.
if (process.env.APP_DEFAULT_ENV === "prod") console.log = () => {};

// when there is error, we can handle this with graphql, many of them has console inside of the request, but you can always use this, or in chrome developer tool
const errorLink = onError(({ graphqlErrors, networkError }) => {
  if (graphqlErrors) {
    graphqlErrors.map(({ message, location, path }) => {
      console.log(`Graphql Error ${(message, location, path)}`);
    });
  }

  if (networkError) {
    console.log("networkError!!", networkError);
    console.log(typeof networkError);
    console.log(JSON.stringify(networkError, null, 2));
  }
});

// const gateway =
//   process.env.NODE_ENV !== "production"
//     ? process.env.REACT_APP_GATEWAY_DEVELOPMENT
//     : process.env.REACT_APP_GATEWAY_PRODUCTION;

const gateway =
    process.env.APP_DEFAULT_ENV !== "prod"
      ? process.env.REACT_APP_GATEWAY_DEVELOPMENT
      : process.env.REACT_APP_GATEWAY_PRODUCTION;

const link = from([errorLink, new HttpLink({ uri: gateway })]);

const authLink = setContext((_, { headers }) => {
  // get the authentication token from local storage if it exists
  const token = localStorage.getItem("app-token");

  // return the headers to the context so httpLink can read them
  return {
    headers: {
      ...headers,
      ["service-name"]: "moviefav-service",
      authorization: token ? `Bearer ${token}` : "",
    },
  };
});

const client = new ApolloClient({
  link: authLink.concat(link),
  cache: new InMemoryCache(),
});

const App = () => {
  const { user } = useContext(AuthContext);
  const [loginUser, setLoginUser] = useState(user);
  const [darkMode, setDarkMode] = useState(false);

  return (
    <ApolloProvider client={client}>
      <AuthContextProvider>
        <Router basename={process.env.REACT_APP_BASENAME || ""}>
          <TokenExpire />
          <div>
            <Routes>
            {AllRoutes.map((route, index) => {
              return (
                <Route
                  key={index}
                  path={route.path}
                  exact={route.exact}
                  element={route.component}
                  // element={withTracker(props => {
                  //   return (
                  //     <route.layout {...props}>
                  //       <route.component {...props} />
                  //     </route.layout>
                  //   );
                  // })}
                />
              );
            })}
            </Routes>
          </div>
        </Router>
      </AuthContextProvider>
    </ApolloProvider>
  );
};

export default App;