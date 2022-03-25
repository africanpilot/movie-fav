import React, { useRef, useEffect, useCallback, useState } from 'react';
import { useParams } from 'react-router';
import { useSpring, animated } from 'react-spring';
import styled from 'styled-components';
import { MdClose } from 'react-icons/md';
import { useLocation, useNavigate } from "react-router-dom";

import { makeStyles } from "@material-ui/core";

import InputLabel from "@material-ui/core/InputLabel";
import Button from "@material-ui/core/Button";
import IconButton from "@material-ui/core/IconButton";
import OutlinedInput from "@material-ui/core/OutlinedInput";
import FormControl from "@material-ui/core/FormControl";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";

import CircularProgress from "@material-ui/core/CircularProgress";

import { useMutation } from "@apollo/client";
import { MOVIE_CREATE_MUTATION } from "../graphql/Queries";

import { 
	StyledFormArea,
} from "../components/layout/login/Styles";

const Background = styled.div`
  width: 50%;
  height: 50%;
  position: relative;
  left: 25%;
  display: flex;
  justify-content: center;
  align-items: center;
`;

const ModalWrapper = styled.div`
  width: 800px;
  height: 600px;
  box-shadow: 0 5px 16px rgba(0, 0, 0, 0.2);
  background: #fff;
  color: #000;
  display: grid;
  position: relative;
  z-index: 10;
  border-radius: 10px;
`;

const ModalImg = styled.img`
  width: 100%;
  height: 100%;
  border-radius: 10px 0 0 10px;
  background: #000;
`;

const ModalContent = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  line-height: 1.8;
  color: #141414;

  p {
    margin-bottom: 1rem;
  }

  button {
    padding: 10px 24px;
    background: #141414;
    color: #fff;
    border: none;
  }
`;

const CloseModalButton = styled(MdClose)`
  cursor: pointer;
  position: absolute;
  top: 20px;
  right: 20px;
  width: 32px;
  height: 32px;
  padding: 0;
  z-index: 10;
`;

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

export const ModalAdd = ({ movieFav, showModal, setShowModal, setCollection }) => {
  const classes = useStyles();
  const location = useLocation();
  const navigate = useNavigate();
  const [episode, setEpisode] = useState("");
  const [movieStatus, setMovieStatus] = useState("");
  const [rating, setRating] = useState("");
  const [buttonDisabled, setButtonDisabled] = useState(false);
  const [seconds] = useState(3);
  const [errorState, setErrorState] = useState({});
  const modalRef = useRef();
  const { id } = useParams();

  const [movieCreate, { loading }] = useMutation(MOVIE_CREATE_MUTATION);

  const animation = useSpring({
    config: {
      duration: 250
    },
    opacity: showModal ? 1 : 0,
    transform: showModal ? `translateY(0%)` : `translateY(-100%)`
  });

  const closeModal = e => {
    if (modalRef.current === e.target) {
      setShowModal(false);
    }
  };

  const keyPress = useCallback(
    e => {
      if (e.key === 'Escape' && showModal) {
        setShowModal(false);
        console.log('I pressed');
      }
    },
    [setShowModal, showModal]
  );

  const handleEpisodeChange = (e) => {
    setEpisode(e.target.value);
  };

  const handleMovieStatusChange = (e) => {
    setMovieStatus(e.target.value);
  };

  const handleRatingChange = (e) => {
    setRating(e.target.value);
  };

  const handleSubmitEditBtn = (e) => {
    e.preventDefault();
    setErrorState({});

    movieCreate({
      variables: {
        movie_fav_info_imdb_id: id,
        movie_fav_info_episode_current: episode ? episode.toString() : "1",
        movie_fav_info_status: movieStatus ? movieStatus : "unmarked",
        movie_fav_info_rating_user: parseFloat(rating),
      },
    })
    .then(({ data: {movieCreate: { response, result },},}) => {
      if (response.success === true) {
        setButtonDisabled(true);
        setShowModal(false);
        // update local data for item
        setCollection(result ? result[0]: movieFav);

        // setTimeout(() => {
        // }, seconds * 1000);
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

  useEffect(
    () => {
      document.addEventListener('keydown', keyPress);
      return () => document.removeEventListener('keydown', keyPress);
    },
    [keyPress]
  );

  return (
    <>
      {showModal ? (
        <Background onClick={closeModal} ref={modalRef}>
          <animated.div style={animation}>
            <ModalWrapper showModal={showModal}>
              {/* <ModalImg src={require('./modal.jpg')} alt='.' /> */}
              <StyledFormArea>
              <form className={classes.root} noValidate autoComplete="off">
                <div>
                <FormControl
                  className={
                    episode === ""
                      ? `${classes.textfield}`
                      : `${classes.textfield} ${classes.filled}`
                  }
                  variant="outlined"
                  style={{ width: "50%", margin: "0.5rem 0 1rem 0", height: 50 }}
                >
                  <InputLabel
                    htmlFor="outlined-adornment-password"
                    error={!!errorState.episode}
                  >
                    episode
                  </InputLabel>
                  <OutlinedInput
                    id="outlined-adornment-password"
                    type={"number"}
                    inputProps={{ min: "1", max: "100000", step: "1" }}
                    value={episode || movieFav.movie_fav_info_episode_current || 1}
                    onChange={handleEpisodeChange}
                    error={!!errorState.episode}
                    labelWidth={70}
                  />
                </FormControl>
                </div>
                
                <div>
                <FormControl
                  className={
                    movieStatus === ""
                      ? `${classes.textfield}`
                      : `${classes.textfield} ${classes.filled}`
                  }
                  variant="outlined"
                  style={{ width: "50%", margin: "0.5rem 0 1rem 0", height: 50 }}
                >
                  <InputLabel
                    htmlFor="outlined-adornment-password"
                    error={!!errorState.movieStatus}
                  >
                    status
                  </InputLabel>
                  <Select
                      required
                      id="outlined-adornment-password"
                      name="printerType"
                      value={movieStatus || movieFav.movie_fav_info_status || "unmarked"}
                      onChange={handleMovieStatusChange}
                      error={!!errorState.movieStatus}
                      labelWidth={70}
                      label="unmarked"
                      style={{textAlign: "left"}}
                    >
                      <MenuItem value={"unmarked"}>unmarked</MenuItem>
                      <MenuItem value={"completed"}>completed</MenuItem>
                      <MenuItem value={"on_hold"}>on hold</MenuItem>
                      <MenuItem value={"dropped"}>dropped</MenuItem>
                      <MenuItem value={"plan_to_watch"}>plan to watch</MenuItem>
                    </Select>
                </FormControl>
                </div>
                
                <div>
                <FormControl
                  className={
                    rating === ""
                      ? `${classes.textfield}`
                      : `${classes.textfield} ${classes.filled}`
                  }
                  variant="outlined"
                  style={{ width: "50%", margin: "0.5rem 0 1rem 0", height: 50 }}
                >
                  <InputLabel
                    htmlFor="outlined-adornment-password"
                    error={!!errorState.rating}
                  >
                  rating
                  </InputLabel>
                  <OutlinedInput
                    id="outlined-adornment-password"
                    type={"number"}
                    inputProps={{ min: "0", max: "10", step: "0.1" }}
                    value={rating || movieFav.movie_fav_info_rating_user || 10}
                    onChange={handleRatingChange}
                    error={!!errorState.rating}
                    labelWidth={70}
                  />
                </FormControl>
                </div>

                  <Button
                    className={classes.signupButton}
                    disabled={loading || buttonDisabled}
                    onClick={(e) => handleSubmitEditBtn(e)}
                    style={{ width: "50%", margin: "0.5rem 0 1rem 0", height: 50 }}
                  >
                    {loading ? (
                      <CircularProgress size={24} className={classes.buttonProgress} />
                    ) : (
                      "Submit"
                    )}
                  </Button>

              </form>



              </StyledFormArea>
              <CloseModalButton
                aria-label='Close modal'
                onClick={() => setShowModal(prev => !prev)}
              />
            </ModalWrapper>
          </animated.div>
        </Background>
      ) : null}
    </>
  );
};
