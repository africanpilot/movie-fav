import React from "react";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";
import {
  DropdownToggle,
  DropdownMenu,
  DropdownItem,
  UncontrolledDropdown
} from "reactstrap";

import PersonIcon from '@material-ui/icons/Person';
import ExitToAppIcon from '@material-ui/icons/ExitToApp';

const UserActions = ({accountName}) => {

  return (
    <UncontrolledDropdown inNavbar nav>
      <DropdownToggle caret nav>
        <img
          className="user-avatar rounded-circle mr-2"
          src={require("./../../../../images/avatars/me.jpg")}
          alt="User Avatar"
        />{" "}
        <span className="d-none d-md-inline-block">{accountName}</span>
      </DropdownToggle>
      <DropdownMenu end>
        <DropdownItem>
          <PersonIcon/> Profile
        </DropdownItem>
        <DropdownItem tag={Link} to="/" className="text-danger">
          <ExitToAppIcon/> Logout
        </DropdownItem>
      </DropdownMenu>
    </UncontrolledDropdown>
  );
};

UserActions.propTypes = {
  accountName: PropTypes.string
};

UserActions.defaultProps = {
  accountName: "Guest"
};

export default UserActions;
