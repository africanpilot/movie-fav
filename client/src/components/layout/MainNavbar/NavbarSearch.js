import React from "react";
import {
  Form,
  InputGroup,
  // InputGroupAddon,
  InputGroupText,
  Input
} from "reactstrap";
import SearchIcon from '@material-ui/icons/Search';

const NavbarSearch = () => (
  <Form className="main-navbar__search w-100 d-none d-md-flex d-lg-flex">
    <InputGroup seamless className="ml-3">
      <InputGroupText>
        <SearchIcon/>
        <Input
          className="navbar-search"
          placeholder="Search for something..."
        />
      </InputGroupText>
    </InputGroup>
  </Form>
);

export default NavbarSearch;