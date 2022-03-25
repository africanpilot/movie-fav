import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../util/authContext";

import { regexForEmail } from "../util/regex.js";

import { makeStyles } from "@material-ui/core";
import InputLabel from "@material-ui/core/InputLabel";
import TextField from "@material-ui/core/TextField";
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
import { ACCOUNT_AUTHENTICATION_LOGIN_MUTATION, ACCOUNT_RESEND_CONFIRM_MUTATION } from "../graphql/Queries";

import { 
	StyledFormArea,
	Avatar, 
	StyledTitle,
	colors,
	ExtraText,
	TextLink,
	CopyrightText,
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
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: "bold",
    fontSize: "2rem",
    marginBottom: "0.5rem",
    [theme.breakpoints.only("xs")]: {
      marginTop: "0.8rem",
      fontSize: "2rem",
    },
    [theme.breakpoints.only("sm")]: {
      fontSize: "2rem",
    },
  },

  cardHeaderDetail: {
    color: "#A4A4A4",
    textAlign: "center",
    marginBottom: "0.8rem",
    fontSize: "1rem",
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

  loginBtn: {
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

  buttonProgress: {
    color: "white",
  },
  formLinks: {
    display: "flex",
    justifyContent: "space-between",
    marginTop: "1rem",
  },
  formSubLinks: {
    color: "#66B0BD",
    textDecoration: "underline",
    "&:hover": {
      color: "#54929D",
      textDecoration: "underline",
    },
  },

  cardHeaderError: {
    color: "#EE5B4F",
  },
}));

const Login = () => {
  const classes = useStyles();
  const navigate = useNavigate();

  const { login } = useContext(AuthContext);
  const [email, setEmail] = useState("");
  const [errorState, setErrorState] = useState({});
  const [password, setPassword] = useState("");
  const [passwordVisible, setPasswordVisible] = useState(false);


	const [signInUser, { loading: signInLoading }] = useMutation(ACCOUNT_AUTHENTICATION_LOGIN_MUTATION);
  const [resendEmail, { loading: resendLoading }] = useMutation(ACCOUNT_RESEND_CONFIRM_MUTATION);

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleClickShowPassword = () => {
    setPasswordVisible(!passwordVisible);
  };

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  const emailHelper = (email) => {
    if (!email.match(regexForEmail)) {
      setErrorState({ email: "Please enter valid email address" });
      return true;
    } else if (email.length < 1) {
      setErrorState({ email: "Please enter email address" });
      return true;
    } else {
      return false;
    }
  };

  const passwordHandler = (password) => {
    if (password.length === 0) {
      setErrorState({
        password: "Please enter password",
      });
      return true;
    }
    return false;
  };

  const handleSignInBtn = (e) => {
    e.preventDefault();
    setErrorState({});
    if (!emailHelper(email) && !passwordHandler(password)) {
      signInUser({
        variables: {
          login: email.trim(),
          password: password,
        },
      })
			.then(({ data: { accountAuthenticationLogin: { result, response } },}) => {

				// if user email is not verified resend it.
				console.log("response message", response.message);
				if (response.message === "http_401_unauthorized: Email unverified") {
					resendEmail({ variables: { login: email},})
						.then(({ data: { accountResendConfirm: { response },},}) => {
							localStorage.setItem("email", email);
							navigate("/email-verification");
						})
						.catch((err) => {
							console.log("ERR", JSON.stringify(err, null, 2));
							setErrorState({
								serverError:
									"There is something wrong, please give us a minute to fix it!",
							});
						});
					return;
				}

				// finally success
				if (response.success === true) {
					const { accountInfo, authenticationToken } = result;
					login(accountInfo, authenticationToken);
					navigate("/home");
				}
				else {
					return setErrorState({
						serverError: response.message,
					});
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
						Welcome, Login
				</StyledTitle>

				{Object.keys(errorState).length > 0 ? (
					<Alert severity="error">
						<AlertTitle>
							{errorState.email || errorState.password || errorState.serverError}
						</AlertTitle>
					</Alert>
				) : null}

				<form
					className={classes.root}
					noValidate
					autoComplete="off"
					onSubmit={handleSignInBtn}
				>
					<TextField
						size={"medium"}
						required
						className={
							email === ""
								? `${classes.textfield}`
								: `${classes.textfield} ${classes.filled}`
						}
						error={!!setErrorState.email}
						variant="outlined"
						label="E-mail"
						name="email"
						type="email"
						value={email}
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

					<FormControl
						className={
							password === ""
								? `${classes.textfield}`
								: `${classes.textfield} ${classes.filled}`
						}
						variant="outlined"
						style={{ width: "100%", margin: "0.5rem 0", height: 50 }}
						required
					>
						<InputLabel htmlFor="outlined-adornment-password">
							Password
						</InputLabel>
						<OutlinedInput
							id="outlined-adornment-password"
							type={passwordVisible ? "text" : "password"}
							value={password}
							onChange={handlePasswordChange}
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

					<Button
						className={classes.loginBtn}
						disabled={signInLoading || resendLoading}
						onClick={handleSignInBtn}
					>
						{signInLoading || resendLoading ? (
							<CircularProgress size={24} className={classes.buttonProgress} />
						) : (
							"Sign in"
						)}
					</Button>
					<ExtraText>
								Forgot password?
								<TextLink to="/forgot-password"> Reset Password</TextLink>
						</ExtraText>
						<ExtraText>
							New here?
							<TextLink to="/signup"> Signup</TextLink>
						</ExtraText>
					
				</form>
			</StyledFormArea>
		<CopyrightText>
			All rights reserved &copy; 2022 Movie Fav, Inc
		</CopyrightText>  
    </div>
  );
};

export default Login;