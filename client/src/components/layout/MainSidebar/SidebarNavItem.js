import React from "react";
import PropTypes from "prop-types";
import { NavLink as RouteNavLink } from "react-router-dom";
import { NavItem, NavLink } from "reactstrap";

const SidebarNavItem = ({ item }) => (
  <NavItem>
    <NavLink tag={RouteNavLink} to={item.to}>
      <div> {item.htmlBefore} 
            {item.title && <span>{item.title}</span>}
            {item.htmlAfter}
      </div>
    </NavLink>
  </NavItem>
);

SidebarNavItem.propTypes = {
  /**
   * The item object.
   */
  item: PropTypes.object
};

export default SidebarNavItem;
