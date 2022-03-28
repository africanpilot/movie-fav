import React, { useEffect, useContext, useState } from "react";
import { AuthContext } from "../util/authContext";
import { useLocation, useNavigate } from "react-router-dom";
import { createStyles, makeStyles } from "@material-ui/core/styles";
import MailOutlineIcon from "@material-ui/icons/MailOutline";
import SmsFailedIcon from "@material-ui/icons/SmsFailed";
import { useMutation } from "@apollo/client";
import { ACCOUNT_CONFIRM_EMAIL_MUTATION } from "../graphql/Queries";
import CircularProgress from "@material-ui/core/CircularProgress";
import ServerError from "../util/ServerError";

const useStyles = makeStyles((theme) =>
  createStyles({
    EmailConfirmation: {
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      flexDirection: "column",
      minHeight: "100vh",
    },
    loadingContainer: {
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      alignItems: "center",
    },
    checkingText: {
      marginTop: "3rem",
      fontSize: "1.5rem",
      fontWeight: "700",
      color: "gray",
    },
    emailIconContainer: {},
    emailIcon: { fontSize: "8rem", color: theme.palette.primary.light },
    emailTitle: {
      fontSize: "2rem",
      fontWeight: "600",
      color: "gray",
    },
    emailDescription: {
      marginTop: "1rem",
      fontSize: "1rem",
      color: "gray",
    },
  })
);

const EmailConfirmation = () => {
  const location = useLocation();
  const [seconds] = useState(5);
  const navigate = useNavigate();

  const urlParams = new URLSearchParams(location.search);
  const token = urlParams.get("ur_token");
  const { verifyEmailToken } = useContext(AuthContext);
  const classes = useStyles();

  const [
    verifyEmailMutation,
    { loading: mutationLoading, data: verifyEmailData, error: mutationError },
  ] = useMutation(ACCOUNT_CONFIRM_EMAIL_MUTATION);

  useEffect(() => {
    localStorage.clear();
    verifyEmailToken(token);
    verifyEmailMutation()
      .then((res) => {
        console.log("Email verification Success")
        setTimeout(() => {
          navigate("/login");
        }, seconds * 1000);
      })
      .catch((error) => console.log(error));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  if (mutationLoading) {
    return (
      <div className={classes.EmailConfirmation}>
        <div className={classes.loadingContainer}>
          <div>
            <CircularProgress size={100} />
          </div>
          <div className={classes.checkingText}>Checking your status </div>
        </div>
      </div>
    );
  }

  if (mutationError) {
    return <ServerError />;
  }

  if (verifyEmailData) {
    const {
      accountConfirmEmail: { response },
    } = verifyEmailData;
    console.log("verifyEmailData", response);

    if (response.success === false) {
      return (
        <div className={classes.EmailConfirmation}>
          <>
            <div className={classes.emailIconContainer}>
              <SmsFailedIcon className={classes.emailIcon} />
            </div>
            <div className={classes.emailTitle}>Error</div>
            <div className={classes.emailDescription}>
              Your email address could not be verified.
            </div>
          </>
        </div>
      );
    }
  }

  return (
    <div className={classes.EmailConfirmation}>
      <>
        <div className={classes.emailIconContainer}>
          <MailOutlineIcon className={classes.emailIcon} />
        </div>
        <div className={classes.emailTitle}>Thank you</div>
        <div className={classes.emailDescription}>
          Your email has been verified. Redirecting to login 5 sec...
        </div>
      </>
    </div>
  );
};

export default EmailConfirmation;
