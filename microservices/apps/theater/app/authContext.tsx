'use client'
// https://www.youtube.com/watch?v=_DqPiZPKkgY&list=PLMhAeHCz8S3_pgb-j51QnCEhXNj5oyl8n

// https://www.youtube.com/watch?v=ewLrGMt7MQY&ab_channel=Classsed
import React, { createContext, useReducer, useEffect } from "react";

export const AuthContext = createContext({
  user: null,
  token: null,
  registerCompleted: null,
  login: (userData: any, token: string | null | undefined, role: string | null | undefined) => {},
  logout: () => {},
  verifyEmailToken: (token: string | null | undefined) => {},
});

const authReducer = (state: any, action: { type: any; payload: { user: any; token: string, role: string}; }) => {  
  switch (action.type) {
    case "LOGIN":
      var account_user = action.payload.user.length > 0 ? action.payload.user[0] : {}
      account_user.user_role = action.payload.role
      
      localStorage.setItem("user", JSON.stringify(account_user));
      localStorage.setItem("theater-app-token", action.payload.token);

      const user: any = typeof window !== "undefined" ? localStorage.getItem("user") : "{}"
      return {
        ...state,
        user: JSON.parse(user) || action.payload.user,
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
      localStorage.setItem("theater-email-token", action.payload.token.trim());
      return {
        ...state,
        token: action.payload.token,
      };
    default:
      return state;
  }
};

const AuthContextProvider: any = (props: typeof AuthContextProvider) => {
  const getUser: any = typeof window !== "undefined" ? localStorage.getItem("user") : "{}"

  const [state, dispatch] = useReducer(authReducer, {
    user: JSON.parse(getUser) || null,
    token: null,
  });

  const login = (userData: any, token: string, role: string) => {
    dispatch({
      type: "LOGIN",
      payload: {
        user: userData,
        token: token,
        role: role,
      },
    });
  };

  const logout = () => {
    dispatch({
      type: "LOGOUT",
      payload: {
        user: undefined,
        token: "",
        role: ""
      }
    });
  };

  const verifyEmailToken = (token: string) => {
    dispatch({
      type: "VERIFYEMAIL",
      payload: { 
        user: undefined,
        token: token, 
        role: ""
      },
    });
  };

  return (
    <AuthContext.Provider
      value={{
        user: state.user,
        token: state.token,
        login,
        logout,
        verifyEmailToken,
      }}
      {...props}
    />
  );
};

export default AuthContextProvider;
