import React from "react";
import { Nav} from "reactstrap";
import UserActions from "./UserActions";
// import TwitterIcon from '@material-ui/icons/Twitter';

const NavbarNav = () => {

  return (
    <Nav navbar className="border-left flex-row">
      <UserActions />
      {/* <TwitterIcon style={{color: "#0074d9"}}/> */}
    </Nav>
  );
};

export default NavbarNav;
