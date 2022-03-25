import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import { regexForEmail, regexForPassword } from "../util/regex.js";

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
import { ACCOUNT_CREATE_MUTATION } from "../graphql/Queries";

import { 
	StyledFormArea,
	Avatar, 
	StyledTitle,
	colors,
	ExtraText,
	TextLink,
	CopyrightText,
	// StyledFormButton,
	// ButtonGroup,
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
    marginBottom: "0rem",
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
    marginLeft: "0.1rem",
    marginBottom: "0.5rem",
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
}));

const SignUp = () => {
  const classes = useStyles();
	const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [errorState, setErrorState] = useState({});
  const [password, setPassword] = useState("");
  const [passwordConfirmation, setPasswordConfirmation] = useState("");
  const [passwordVisible, setPasswordVisible] = useState(false);
	const [createUser, { loading }] = useMutation(ACCOUNT_CREATE_MUTATION);

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

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

  const emailHelper = (email) => {
    if (!email.match(regexForEmail)) {
      setErrorState({ email: "Please enter valid email address" });
      return true;
    } else if (email.length < 1) {
      setErrorState({ isError: true, email: "Please enter email address" });
      return true;
    } else {
      return false;
    }
  };

  const passwordHandler = (password) => {
    if (!password.match(regexForPassword)) {
      setErrorState({
        password:
          "Minimum of eight characters, at least 1 uppercase letter, 1 lowercase letter, 1 number and 1 special character are required.",
      });
      return true;
    } else if (password !== passwordConfirmation) {
      setErrorState({
        password: "Password do not match",
        passwordConfirmation: true,
      });
      return true;
    }
    return false;
  };

  const handleCreateButton = (e) => {
    e.preventDefault();
    setErrorState({});
    if (!!emailHelper(email) || !!passwordHandler(password)) {
    } else {
      createUser({
        variables: {
          login: email.trim(),
          password: password,
          reTypePassword: passwordConfirmation,
        },
      }) //mutation successfully went through
			.then( ({ data: { accountCreate: { response } }, }) => {
					// get a success response on clientside, but rejected by serverside
					if (!response.success) {
						setErrorState({ serverError: response.message });
					} else {
						// finally we went through all step!
						localStorage.setItem("account-email", email.trim());
						navigate('/email-verification');
					}
			})
			.catch((error) => {
				console.log("error", JSON.stringify(error, null, 2));
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
						Welcome, Signup
				</StyledTitle>

				{Object.keys(errorState).length > 0 ? (
					<Alert severity="error">
						<AlertTitle>
							{errorState.email || errorState.password || errorState.serverError}
						</AlertTitle>
					</Alert>
				) : null}

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
						style={{ width: "100%", margin: "2.1rem 0 1rem 0", height: 50 }}
					/>

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
						style={{ width: "100%", margin: "0.5rem 0 1rem 0", height: 50 }}
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
						disabled={loading}
						onClick={(e) => handleCreateButton(e)}
					>
						{loading ? (
							<CircularProgress size={24} className={classes.buttonProgress} />
						) : (
							"Create Account"
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

export default SignUp;