import React from "react";
import { StyledTitle, 
    StyledSubTitle, 
    Avatar, 
    StyledButton,
    ButtonGroup, 
} from "../components/layout/login/Styles";

import Logo from "../images/flag-us.png"

const Welcome = () => (
    <div>
        <div
            style={{
                position: "absolute",
                top: "5%",
                left: 0,
                backgroundColor: "transparent",
                width: "100%",
                padding: "15px",
                display: "flex",
                justifyContent: "flex-start",
            }}
        >
            <Avatar image={Logo}/>
        </div>

        <StyledTitle size={65}>
            Welcome to Movie Fav
        </StyledTitle>
        <StyledSubTitle size={27}>
            Track of your favorite shows
        </StyledSubTitle>
        
        <ButtonGroup>
            <StyledButton to="/login">
                Login
            </StyledButton>
            <StyledButton to="/signup">
                Sign up
            </StyledButton>
        </ButtonGroup> 
        
    </div>
);

export default Welcome;