import React from "react";
// import { ReactComponent as NoConnection } from "../images/ServerError.svg";
import SettingsInputAntennaIcon from '@material-ui/icons/SettingsInputAntenna';
import { createStyles, makeStyles } from "@material-ui/core/styles";
import { Link } from "react-router-dom";
const useStyles = makeStyles((theme) =>
  createStyles({
    ServerError: {
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      alignItems: "center",
      marginTop: "5rem",
    },
    ServerErrorTop: {
      fontSize: "2rem",
      fontWeight: "700",
      color: "#BBBDBF",
      marginBottom: "1rem",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
    },

    ServerErrorMid: {},

    serverErrorIcon: {
      fontSize: "5rem",
      color: "#5E6369",
    },

    ServerErrorBottom: {
      color: "#A8AAAC",
      textAlign: "center",
    },
    hompageLink: {
      color: theme.palette.primary.light,
      textDecoration: "underline",
    },
  })
);

const ServerError = () => {
  const classes = useStyles();
  return (
    <div className={classes.ServerError}>
      <div className={classes.ServerErrorTop}>
        <div>We're sorry—</div> <div>we've run into an issue.</div>
      </div>
      <div className={classes.ServerErrorMid}>
        {/* <NoConnection /> */}
        <SettingsInputAntennaIcon/>
      </div>
      <div className={classes.ServerErrorBottom}>
        {/* <div>Sorry, we couldn't process your request.</div> */}
        <div>Please try again later.</div>
        <div>
          You can try other things on our{" "}
          <Link to={"/"} className={classes.hompageLink}>
            homepage
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ServerError;
