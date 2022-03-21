import React, { useState, useEffect } from "react";

import { useLocation, useNavigate } from "react-router-dom";

import { makeStyles } from "@material-ui/core";

import InputLabel from "@material-ui/core/InputLabel";
import Button from "@material-ui/core/Button";
import IconButton from "@material-ui/core/IconButton";
import OutlinedInput from "@material-ui/core/OutlinedInput";

import CircularProgress from "@material-ui/core/CircularProgress";
import InputAdornment from "@material-ui/core/InputAdornment";
import Visibility from "@material-ui/icons/Visibility";
import VisibilityOff from "@material-ui/icons/VisibilityOff";
import FormControl from "@material-ui/core/FormControl";
import { Alert, AlertTitle } from "@material-ui/lab";

import { useMutation } from "@apollo/client";
import { regexForPassword } from "../util/regex.js";
import { ACCOUNT_FORGOT_PASSWORD_CONFIRM_EMAIL_MUTATION, ACCOUNT_MODIFY_PASSWORD_MUTATION } from "../graphql/Queries";

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
    marginTop: "0rem",
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
    fontSize: "1rem",
    marginBottom: "1rem",
    [theme.breakpoints.only("sm")]: {
      fontSize: "1.1rem",
      color: "#9c9999",
      fontWeight: 450,
    },
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
    justifyContent: "flex-end",
    marginTop: "1rem",
  },
  formSubLinks: {
    color: "#A4A4A4",
    textDecoration: "none",
    "&:hover": {
      color: "black",
    },
  },

  buttonProgress: {
    color: "white",
  },

  Tooltip: {
    marginTop: "1rem",
  },

  cardHeaderError: {
    color: "#EE5B4F",
  },

  loginText: {
    textDecoration: "underline",
  },
}));

const ChangePassword = () => {
  const classes = useStyles();
  const location = useLocation();
  const navigate = useNavigate();

  const [errorState, setErrorState] = useState({});
  const [password, setPassword] = useState("");
  const [passwordConfirmation, setPasswordConfirmation] = useState("");
  const [passwordVisible, setPasswordVisible] = useState(false);
  const [wrongApproach, setWrongApproach] = useState(false);
  const [seconds] = useState(3);
  const [status, setStatus] = useState(false);
  const [buttonDisabled, setButtonDisabled] = useState(false);

  const urlParams = new URLSearchParams(location.search);
  const token = urlParams.get("ur_token");

  localStorage.setItem("app-token", token);

  const [forgetPasswordValidation] = useMutation(ACCOUNT_FORGOT_PASSWORD_CONFIRM_EMAIL_MUTATION);
  const [userPasswordChange, { loading }] = useMutation(ACCOUNT_MODIFY_PASSWORD_MUTATION);

  useEffect(() => {
    forgetPasswordValidation()
      .then(({data: { accountForgotPasswordConfirmEmail: { response },},}) => {
        if (response.success === false) {
          setWrongApproach(true);
          setTimeout(() => {
            navigate("/login");
          }, seconds * 1000);
        }
      })
      .catch((err) => {
        console.log("ERR", JSON.stringify(err, null, 2));
        setErrorState({
          serverError:
            "There is something wrong, please give us a minute to fix it!",
        });
      });
  }, [token,seconds, navigate, forgetPasswordValidation]);

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handlePasswordConfirmationChange = (e) => {
    setPasswordConfirmation(e.target.value);
  };

  const handleClickShowPassword = () => {
    setPasswordVisible(!passwordVisible);
  };

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  const passwordHandler = (password) => {
    if (!password.match(regexForPassword)) {
      setErrorState({
        password:
          "Minimum eight characters, at least 1 uppercase letter, 1 lowercase letter, 1 number and 1 special character are required.",
      });
      return true;
    } else if (password !== passwordConfirmation) {
      setErrorState({
        password: "Passwords do not match",
        passwordConfirmation: true,
      });
      return true;
    }
    return false;
  };

  const handlePasswordChangeBtn = (e) => {
    e.preventDefault();
    setErrorState({});
    if (passwordHandler(password)) {
      //   return;
    } else {
      userPasswordChange({
        variables: {
          password: password,
          passwordRetype: passwordConfirmation,
        },
      })
      .then(({ data: {accountModify: { response },},}) => {
        if (response.success === true) {
          setStatus(true);
          setButtonDisabled(true);
          setTimeout(() => {
            navigate("/login");
          }, seconds * 1000);
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

  const handleLoginBtn = () => {
    navigate("/login");
  };

  return (
    <div>
      <StyledFormArea>
				<Avatar image={Logo}/>
				<StyledTitle color={colors.theme} size={30}>
          Change Your Password
				</StyledTitle>
        <StyledSubTitle color={colors.theme}>
          Enter your new account password below.
        </StyledSubTitle>

      {wrongApproach ? (
        <Alert severity="error">
          <AlertTitle>Wrong Approach</AlertTitle>

          <strong>Please check your email with valid token.</strong>
          <br />
          <strong>
            For security reason, you will be redirected in {seconds} seconds
          </strong>
        </Alert>
      ) : null}

      {Object.keys(errorState).length > 0 ? (
        <Alert severity="error">
          <AlertTitle>
            {errorState.password || errorState.serverError}
          </AlertTitle>
        </Alert>
      ) : null}

      {status ? (
        <Alert severity="success">
          <AlertTitle>Success</AlertTitle>
          Please{" "}
          <strong onClick={handleLoginBtn} className={classes.loginText}>
            Log In
          </strong>{" "}
          with your new password!
          <br />
          Or We can redirect you in {seconds} seconds!
        </Alert>
      ) : null}
      <br />

      <form className={classes.root} noValidate autoComplete="off">
        <FormControl
          className={
            password === ""
              ? `${classes.textfield}`
              : `${classes.textfield} ${classes.filled}`
          }
          variant="outlined"
          style={{ width: "100%", margin: "0.5rem 0 1rem 0", height: 50 }}
        >
          <InputLabel
            required
            htmlFor="outlined-adornment-password"
            error={!!errorState.password}
          >
            Password
          </InputLabel>
          <OutlinedInput
            id="outlined-adornment-password"
            type={passwordVisible ? "text" : "password"}
            value={password}
            onChange={handlePasswordChange}
            error={!!errorState.password}
            endAdornment={
              <InputAdornment position="end">
                <IconButton
                  aria-label="toggle password visibility"
                  onClick={handleClickShowPassword}
                  onMouseDown={handleMouseDownPassword}
                  edge="end"
                >
                  {passwordVisible ? <Visibility /> : <VisibilityOff />}
                </IconButton>
              </InputAdornment>
            }
            labelWidth={70}
          />
        </FormControl>

        <FormControl
          className={
            password === ""
              ? `${classes.textfield}`
              : `${classes.textfield} ${classes.filled}`
          }
          variant="outlined"
          fullWidth
          style={{ width: "100%", margin: "0.5rem 0 0rem 0", height: 50 }}
        >
          <InputLabel
            htmlFor="outlined-adornment-password-confirmation"
            error={!!errorState.passwordConfirmation}
            required
          >
            Password Confirmation
          </InputLabel>
          <OutlinedInput
            id="outlined-adornment-password-confirmation"
            type={passwordVisible ? "text" : "password"}
            value={passwordConfirmation}
            onChange={handlePasswordConfirmationChange}
            error={!!errorState.passwordConfirmation}
            endAdornment={
              <InputAdornment position="end">
                <IconButton
                  aria-label="toggle password visibility"
                  onClick={handleClickShowPassword}
                  onMouseDown={handleMouseDownPassword}
                  edge="end"
                >
                  {passwordVisible ? <Visibility /> : <VisibilityOff />}
                </IconButton>
              </InputAdornment>
            }
            labelWidth={170}
          />
        </FormControl>

        <Button
          className={classes.signupButton}
          disabled={loading || buttonDisabled}
          onClick={(e) => handlePasswordChangeBtn(e)}
        >
          {loading ? (
            <CircularProgress size={24} className={classes.buttonProgress} />
          ) : (
            "Change Password"
          )}
        </Button>

        <ExtraText>
          Already have an account?
          <TextLink to="/login"> Login</TextLink>
        </ExtraText>

      </form>
      </StyledFormArea>
      <CopyrightText>
        All rights reserved &copy; 2022 Movie Fav, Inc
      </CopyrightText>
    </div>
  );
};

export default ChangePassword;
