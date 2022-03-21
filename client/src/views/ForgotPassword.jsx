import React, { useState } from "react";

import { makeStyles } from "@material-ui/core";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import { Alert, AlertTitle } from "@material-ui/lab";
import CircularProgress from "@material-ui/core/CircularProgress";
import { regexForEmail } from "../util/regex.js";

import { useMutation } from "@apollo/client";
import { ACCOUNT_FORGOT_PASSWORD_MUTATION } from "../graphql/Queries";

import { 
	StyledFormArea,
	Avatar, 
	StyledTitle,
	colors,
	ExtraText,
	TextLink,
	CopyrightText,
  StyledSubTitle,
} from "../components/layout/login/Styles";
import Logo from "../images/flag-us.png";


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
      fontSize: "1.9rem",
    },
  },

  cardHeaderDetail: {
    color: "#A4A4A4",
    marginBottom: "1rem",
    [theme.breakpoints.only("sm")]: {
      fontSize: "1.1rem",
      color: "#9c9999",
      fontWeight: 450,
    },
  },

  buttonProgress: {
    color: "white",
  },

  cardHeaderError: {
    color: "#FF7676",
  },
  resend: {
    color: theme.palette.primary.light,
    textDecoration: "underline",
    cursor: "pointer",
  },

  textfield: {
    height: "2.4rem",
    "& .MuiInputBase-formControl": {
      borderRadius: "8px",
      backgroundColor: "#F5F5F5",
      borderWidth: "1 !important",
    },
    "& .Mui-focused-": {
      backgroundColor: "green",
    },

    "& .MuiOutlinedInput-notchedOutline": {
      // border: 0,
    },
  },

  filled: {
    height: "2.4rem",
    "& .MuiInputBase-formControl": {
      backgroundColor: "white",
      // color: "black !important",
    },

    "& .MuiOutlinedInput-notchedOutline": {
      border: "1px solid lightgray",
    },
  },

  signupButton: {
    width: "100%",
    color: "white",
    fontSize: "1.1rem",
    marginTop: "2rem",
    backgroundColor: "#BE185D",//theme.backgrounds.main,
    height: "2.6rem",
    "&:hover": {
      color: "white",
      backgroundColor: "#97D2DD",
    },
    [theme.breakpoints.down("sm")]: {
      margin: "2rem 0 1rem 0",
    },
  },
  formLinks: {
    display: "flex",
    justifyContent: "space-between",
    marginTop: "1rem",
  },

  formSubLinks: {
    color: "#A4A4A4",
    textDecoration: "none",
    "&:hover": {
      color: "black",
    },
    resend: {
      textDecoration: "underline",
    },
  },
}));

const ForgotPassword = () => {
  const classes = useStyles();

  const [email, setEmail] = useState("");
  const [errorState, setErrorState] = useState({});
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(false);
  const [buttonDisabled, setButtonDisabled] = useState(false);
  const [forgotPasswordRequest] = useMutation(ACCOUNT_FORGOT_PASSWORD_MUTATION);
  const [inputFieldDisabled, setInputFieldDisabled] = useState(false);
  
  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const emailHelper = (email) => {
    if (!email.match(regexForEmail)) {
      setErrorState({ email: "Please enter valid email address" });
      return true;
    } else if (email.length < 1) {
      setErrorState({ isError: true, email: "Please enter email address" });
      return true;
    } else {
      setErrorState({});
      return false;
    }
  };

  const handleResetBtnClick = () => {
    setErrorState({});
    if (!!emailHelper(email)) {
      return;
    } else {
      setLoading(true);

      forgotPasswordRequest({
        variables: {
          login: email,
        },
      })
      .then(({ data: { accountForgotPassword: { response },},}) => {
        if (response.success === true) {
          setStatus(true);
          setLoading(false);
          setButtonDisabled(true);
          setInputFieldDisabled(true);
          console.log("request sent")
        }else{
          setErrorState({ server: response.message });
          setLoading(false);
        }
      })
      .catch((err) => {
				console.log("ERR", JSON.stringify(err, null, 2));
				setErrorState({
					serverError:
						"There is something wrong, please give us a minute to fix it!",
				});
			});
    }
  };

  return (
    <div>
      <StyledFormArea>
				<Avatar image={Logo}/>
				<StyledTitle color={colors.theme} size={30}>
          Forgot your password?
				</StyledTitle>
        <StyledSubTitle color={colors.theme}>
          We'll send you an email with a password reset link.
        </StyledSubTitle>

        {Object.keys(errorState).length > 0 ? (
          <Alert severity="error">
            <AlertTitle>Error!</AlertTitle>

            <strong>{errorState.email || errorState.server}</strong>
          </Alert>
        ) : null}
        {status ? (
          <Alert severity="success">
            <AlertTitle>Success</AlertTitle>A password reset message was sent to
            your email. If you did not receive the message, please check your spam
            folder or click{" "}
            <strong onClick={handleResetBtnClick} className={classes.resend}>
              RESEND
            </strong>
          </Alert>
        ) : 

        <form className={classes.root} noValidate autoComplete="off">
          <TextField
            size={"medium"}
            required
            className={
              email === ""
                ? `${classes.textfield}`
                : `${classes.textfield} ${classes.filled}`
            }
            error={!!errorState.email}
            variant="outlined"
            label="E-mail"
            name="email"
            type="email"
            value={email}
            disabled={inputFieldDisabled}
            onChange={handleEmailChange}
            InputLabelProps={{
              classes: {
                root: classes.cssLabel,
                focused: classes.cssFocused,
              },
            }}
            InputProps={{
              classes: {
                root: classes.cssOutlinedInput,
                focused: classes.cssFocused,
                notchedOutline: classes.notchedOutline,
              },
            }}
            style={{ width: "100%", margin: "1.5rem 0", height: 50 }}
          ></TextField>

          <Button
            className={classes.signupButton}
            onClick={handleResetBtnClick}
            disabled={buttonDisabled}
          >
            {loading ? (
              <CircularProgress size={24} className={classes.buttonProgress} />
            ) : (
              "Reset Password "
            )}
          </Button>
            <ExtraText>
              Already have an account?
							<TextLink to="/login"> Login</TextLink>
						</ExtraText>
						<ExtraText>
							New here?
							<TextLink to="/signup"> Signup</TextLink>
						</ExtraText>
        </form>

      }

      </StyledFormArea>
      <CopyrightText>
        All rights reserved &copy; 2022 Movie Fav, Inc
      </CopyrightText>
    </div>
  );
};

export default ForgotPassword;
