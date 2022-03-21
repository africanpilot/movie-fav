import React from "react";
import { Dispatcher, Constants } from "../../../flux";

const NavbarToggle = () => {

  const handleClick = () => {
    Dispatcher.dispatch({
      actionType: Constants.TOGGLE_SIDEBAR
    });
  }

  return (
    <nav className="nav">
      {/* eslint-disable-next-line jsx-a11y/anchor-is-valid */}
      <a href="#" onClick={handleClick} className="nav-link nav-link-icon toggle-sidebar d-sm-inline d-md-inline d-lg-none text-center">
        <i className="material-icons">&#xE5D2;</i>
      </a>
    </nav>
  )
};

export default NavbarToggle;
