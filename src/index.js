import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import Auth from "./components/Auth";

// import { ApolloProvider, Query } from "react-apollo";
import { ApolloProvider, useQuery } from "@apollo/react-hooks";
import ApolloClient, { gql } from "apollo-boost";
import { InMemoryCache } from "apollo-cache-inmemory";

import * as serviceWorker from "./serviceWorker";
// uri: "http://example.herokuapp.com/graphql/"

// !Apollo Client is available to the entire app
// ! fetchOptions: {credentials: 'include' - means to include operation.headers (just below in the request)}
const cache = new InMemoryCache();
const client = new ApolloClient({
  uri: "http://localhost:8000/graphql/",
  fetchOptions: {
    credentials: "include"
  },
  request: operation => {
    const token = localStorage.getItem("authToken") || "";
    operation.setContext({
      headers: {
        Authorization: `JWT ${token}`
      }
    });
  }
});

cache.writeDate({
  data: {
    isLoggedIn: !!localStorage.getItem("authToken")
  }
});

// ! Change the turnary below to include an authorization page, or whatever the user should see if they are not logged in.
const ApolloApp = () => {
  const { loading, error, data } = useQuery(gql`
    {
      isLoggedIn @client
    }
  `);

  return (
    <ApolloProvider client={client}>
      {console.log(data)}
      {data => (data.isLoggedIn ? <App /> : <Auth />)}
    </ApolloProvider>
  );
};

ReactDOM.render(<ApolloApp />, document.getElementById("root"));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();

// const client = new ApolloClient({
//   uri: "http://localhost:8000/graphql/",
//   fetchOptions: {
//     credentials: "include"
//   },
//   request: operation => {
//     const token = localStorage.getItem('authToken') || "";
//     operation.setContext({
//       headers: {
//         Authorization: `JWT ${token}`
//       }
//     })
//   },
//   clientState: {
//     defaults: {
//       // !The double bangs converts any value to a boolean
//       isLoggedIn: !!localStorage.getItem("authToken")
//     }
//   }
// });

// Does a query on the client (not the server) and the returned value (boolean) determines what the user sees, in this case home page or authorization page
// const IS_LOGGED_IN_QUERY = gql`
//   query {
//     isLoggedIn @client
//   }
// `;
