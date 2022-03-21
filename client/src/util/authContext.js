// https://www.youtube.com/watch?v=_DqPiZPKkgY&list=PLMhAeHCz8S3_pgb-j51QnCEhXNj5oyl8n

// https://www.youtube.com/watch?v=ewLrGMt7MQY&ab_channel=Classsed
import React, { createContext, useReducer } from "react";

export const AuthContext = createContext({
  user: null,
  token: null,
  registerCompleted: null,
  login: (userData) => {},
  logout: () => {},
});

const authReducer = (state, action) => {
  switch (action.type) {
    case "LOGIN":
      localStorage.setItem("user", JSON.stringify(action.payload.user));
      localStorage.setItem("app-token", action.payload.token);

      return {
        ...state,
        user: JSON.parse(localStorage.getItem("user")) || action.payload.user,
        token: action.payload.token,
      };
    case "LOGOUT":
      localStorage.clear();
      return {
        ...state,
        user: null,
        token: null,
        registerCompleted: null,
      };
    case "VERIFYEMAIL":
      localStorage.setItem("app-token", action.payload);
      return {
        ...state,
        token: action.payload,
      };
    default:
      return state;
  }
};

const AuthContextProvider = (props) => {
  const [state, dispatch] = useReducer(authReducer, {
    user: JSON.parse(localStorage.getItem("user")) || null,
    token: null,
  });

  const login = (userData, token) => {
    dispatch({
      type: "LOGIN",
      payload: {
        user: userData,
        token: token,
      },
    });
  };

  const logout = (props) => {
    dispatch({ type: "LOGOUT" });
  };

  const verifyEmailToken = (token) => {
    dispatch({
      type: "VERIFYEMAIL",
      payload: token,
    });
  };

  return (
    <AuthContext.Provider
      value={{
        user: state.user,
        login,
        logout,
        token: state.token,
        verifyEmailToken,
      }}
      {...props}
    />
  );
};

export default AuthContextProvider;
