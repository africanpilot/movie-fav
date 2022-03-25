import React from "react";
// import { Navigate } from "react-router-dom";

// Layout Types
import { DefaultLayout } from "./layouts";
import { StyledContainer } from "./components/layout/login/Styles";

// Route Views
import Home from "./views/Home";
import MovieCollections from "./views/MovieCollections";
import TvShowsCollections from "./views/TvShowsCollections";
import Welcome from "./views/Welcome";
import Login from "./views/Login";
import SignUp from "./views/SignUp";
import EmailVerification from "./views/EmailVerification";
import EmailConfirmation from "./views/EmailConfirmation";
import ForgotPassword from "./views/ForgotPassword";
import ChangePassword from "./views/ChangePassword";
import MovieDetail from "./views/MovieDetail";

const AllRoutes = [
    {
      path: "/",
      exact: true,
      layout: <StyledContainer/>,
      component: <StyledContainer><Welcome/></StyledContainer>, 
    },
    {
      path: "/welcome",
      layout: <StyledContainer/>,
      component: <StyledContainer><Welcome/></StyledContainer>, 
    },
    {
      path: "/login",
      layout: <StyledContainer/>,
      component: <StyledContainer><Login/></StyledContainer>, 
    },
    {
      path: "/signup",
      layout: <StyledContainer/>,
      component: <StyledContainer><SignUp/></StyledContainer>, 
    },
    {
      path: "/email-verification",
      layout: <StyledContainer/>,
      component: <StyledContainer><EmailVerification/></StyledContainer>, 
    },
    {
      path: "/email-confirmation/",
      layout: <StyledContainer/>,
      component: <StyledContainer><EmailConfirmation/></StyledContainer>, 
    },
    {
      path: "/forgot-password",
      layout: <StyledContainer/>,
      component: <StyledContainer><ForgotPassword/></StyledContainer>, 
    },
    {
      path: "/change-password",
      layout: <StyledContainer/>,
      component: <StyledContainer><ChangePassword/></StyledContainer>, 
    },
    {
      path: "/home",
      layout: <DefaultLayout/>,
      component: <DefaultLayout> <Home/> </DefaultLayout>,
    },
    {
      path: "/movie-collections",
      layout: <DefaultLayout/>,
      component: <DefaultLayout> <MovieCollections/> </DefaultLayout>, 
    },
    {
      path: "/tv-shows-collections",
      layout: <DefaultLayout/>,
      component: <DefaultLayout> <TvShowsCollections/> </DefaultLayout>, 
    },
    {
      path: "/movie/:id",
      layout: <DefaultLayout/>,
      component: <DefaultLayout><MovieDetail/></DefaultLayout>, 
    },
];

export default AllRoutes