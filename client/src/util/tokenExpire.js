import React,  { useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import jwt_decode from "jwt-decode";

const TokenExpire = ({ history }) => {
  const navigate = useNavigate();
  const location = useLocation();
  
  console.log("checking token");
  console.log("location: ", location.pathname);

  useEffect(() => {
    // allowed to access while getting a token
    const allowedLocations = [
      "/login", 
      "/forgot-password", 
      "/email-verification", 
      "/signup",
      "/welcome"
    ]

    if (localStorage.getItem("app-token")) {
      console.log("Found token");
      const jwt_Token_decoded = jwt_decode(localStorage.getItem("app-token"));
  
      if (jwt_Token_decoded.exp * 1000 <= Date.now()) {
        localStorage.clear();
        navigate('/login');
      }
    }else{
      console.log("checking location");
      if(!allowedLocations.includes(location.pathname)){
        console.log("not allowed redirect");
        navigate('/login');
      }
    }

  }, [navigate, location]);
  
  return <></>;
};

export default TokenExpire;