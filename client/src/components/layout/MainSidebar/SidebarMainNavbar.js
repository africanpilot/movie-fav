import React from "react";
import PropTypes from "prop-types";
import { Navbar, NavbarBrand, Col} from "reactstrap";
import { Dispatcher, Constants } from "../../../flux";
import TheatersIcon from '@material-ui/icons/Theaters';


const SidebarMainNavbar = () => {
  
  const handleToggleSidebar = () => {
    Dispatcher.dispatch({
      actionType: Constants.TOGGLE_SIDEBAR
    });
  }

  return (
    <div className="main-navbar">
      <Navbar
        className="align-items-stretch bg-white flex-md-nowrap border-bottom p-0"
        type="light"
      >
        <NavbarBrand className="w-100 mr-0">
          <Col>
            <img
              id="main-logo"
              style={{ maxWidth: "150px",display: "block",
              marginLeft: "auto",
              marginRight: "auto",}}
              // src={require("../../../images/flag-us.png")}
              alt="Movie Fav"
            />
          </Col>
        </NavbarBrand>
        {/* eslint-disable-next-line */}
        <a
          className="toggle-sidebar d-sm-inline d-md-none d-lg-none"
          onClick={handleToggleSidebar}
        >
          <TheatersIcon/>
        </a>
      </Navbar>
    </div>
  );
};

SidebarMainNavbar.propTypes = {
  /**
   * Whether to hide the logo text, or not.
   */
  hideLogoText: PropTypes.bool
};

SidebarMainNavbar.defaultProps = {
  hideLogoText: false
};

export default SidebarMainNavbar;