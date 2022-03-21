import React, { useContext } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { AuthContext } from "../util/authContext";

import { makeStyles } from "@material-ui/core";
import { useMutation } from "@apollo/client";
import { ACCOUNT_RESEND_CONFIRM_MUTATION } from "../graphql/Queries";

import CircularProgress from "@material-ui/core/CircularProgress";
import Button from "@material-ui/core/Button";

const useStyles = makeStyles((theme) => ({
  root: {
    backgroundColor: "",
    "& .MuiOutlinedInput-root.Mui-focused .MuiOutlinedInput-notchedOutline": {
      borderColor: `#BE185D !important`, //`${theme.backgroundColor} !important`,
    },
  },

  cardHeader: {
    marginBottom: "0.5rem",
  },

  cardHeaderTitle: {
    fontWeight: "bold",
    fontSize: "1.5rem",
    [theme.breakpoints.only("xs")]: {
      marginTop: "0.8rem",
      fontSize: "1.2rem",
    },
    [theme.breakpoints.only("sm")]: {
      fontSize: "1.5rem",
    },
    marginBottom: "1rem",
  },

  cardHeaderDetail: {
    color: "#A4A4A4",
    marginBottom: "1rem",

    [theme.breakpoints.only("sm")]: {
      fontSize: "1rem",
      color: "#9c9999",
      fontWeight: 450,
    },
  },

  emailAddress: {
    fontWeight: "500",
    textDecoration: "underline",
    color: "black",
  },

  firstParagraph: {},

  secondParagraph: {
    marginBottom: "1rem",
  },

  fifthParagraph: {
    marginTop: "1rem",
  },

  resend: {
    textDecoration: "underline",
    color: theme.palette.primary.light,
    fontWeight: "700",
    cursor: "pointer",
  },

  emailBtn: {
    color: "white",
    marginTop: "1rem",
  },

  NotInterestedIcon: {
    color: "#EE5B4F",
    fontSize: "5rem",
    marginRight: "1rem",
  },

  verificationResult: {
    marginTop: "1rem",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    marginBottom: "1rem",
  },
}));

const EmailVerification = (props) => {
  const classes = useStyles();
  const navigate = useNavigate();
  const location = useLocation();
  let { user } = useContext(AuthContext);

  const handleCheckEmail = () => {
    navigate("/login");
  };

  console.log("user", user);
  console.log("location", location);

  const [resendEmail, { loading: resendLoading }] = useMutation(ACCOUNT_RESEND_CONFIRM_MUTATION);

  let emailMarkup = localStorage.getItem("account-email");

  const handleResend = () => {
    console.log("user1", user);
    console.log("location1", location);
    resendEmail({
      variables: {
        login: user ? user.login.login : emailMarkup,
      },
    });
  };

  return (
    <>
      <div className={classes.cardHeader}>
        <div className={classes.cardHeaderTitle}>
          Please Verify Your Email Address
        </div>
        <div className={classes.cardHeaderDetail}>
          <div className={classes.firstParagraph}>
            Please take a moment and validate your email to confirm
          </div>

          <div className={classes.secondParagraph}>
            your account. We sent a verification email to{" "}
            <span className={classes.emailAddress}>
              {user ? user.login.login : emailMarkup}
            </span>
          </div>

          <div className={classes.fourthParagraph}>
            If you don't see it, you may need to check your spam folder.
          </div>
          <div className={classes.fifthParagraph}>
            Still can't find the email?{" "}
            <span className={classes.resend} onClick={handleResend}>
              Resend Email
            </span>
          </div>
          <Button
            fullWidth
            className={classes.emailBtn}
            variant="contained"
            color="primary"
            disableElevation
            onClick={handleCheckEmail}
            disabled={resendLoading}
          >
            {resendLoading ? (
              <CircularProgress size={24} className={classes.buttonProgress} />
            ) : (
              "Login"
            )}
          </Button>
        </div>
      </div>
    </>
  );
};

export default EmailVerification;
