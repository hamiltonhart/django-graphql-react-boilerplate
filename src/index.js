import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import Auth from './components/Auth';

import { ApolloProvider, Query } from "react-apollo";
import ApolloClient, { gql } from "apollo-boost";

import * as serviceWorker from './serviceWorker';
// uri: "http://example.herokuapp.com/graphql/"

// !Apollo Client is available to the entire app
// ! fetchOptions: {credentials: 'include' - means to include operation.headers (just below in the request)}
const client = new ApolloClient({
  uri: "http://localhost:8000/graphql/",
  fetchOptions: {
    credentials: "include"
  },
  request: operation => {
    const token = localStorage.getItem('authToken') || "";
    operation.setContext({
      headers: {
        Authorization: `JWT ${token}`
      }
    })
  },
  clientState: {
    defaults: {
      // !The double bangs converts any value to a boolean
      isLoggedIn: !!localStorage.getItem("authToken")
    }
  }
});

// Does a query on the client (not the server) and the returned value (boolean) determines what the user sees, in this case home page or authorization page
const IS_LOGGED_IN_QUERY = gql`
  query {
    isLoggedIn @client
  }
`;


// ! Change the turnary below to include an authorization page, or whatever the user should see if they are not logged in.
const ApolloApp = () => (
  <ApolloProvider client={client}>
    <Query query={IS_LOGGED_IN_QUERY}>
      {({ data }) => (data.isLoggedIn ? <App /> : <Auth />)}
    </Query>
  </ApolloProvider>
)

ReactDOM.render(<ApolloApp />, document.getElementById("root"));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
