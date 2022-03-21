import { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "./authContext";

export const RegisterRedirect = () => {
  const navigate = useNavigate();
  const { user } = useContext(AuthContext);
  
  useEffect(() => {
    if(user === null){
      navigate("/login");
    }
  }, [navigate,user]);
};