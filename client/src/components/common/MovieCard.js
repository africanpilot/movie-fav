/* eslint jsx-a11y/anchor-is-valid: 0 */
import React, { useState } from "react";
import { Link, useNavigate } from 'react-router-dom';
import PropTypes from "prop-types";
import {Col, Card} from "reactstrap";
import './movie-card.scss';
import Button from '../button/Button';
import AddBoxOutlinedIcon from '@material-ui/icons/AddBoxOutlined';
import { IconButton } from '@mui/material';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';

import { useMutation } from "@apollo/client";
import { MOVIE_CREATE_QUICK_ADD_MUTATION } from "../../graphql/Queries";


const truncate = (str) => {
  return str.length > 20 ? str.substring(0, 20) + "..." : str;
}

const MovieCard = ({ movie }) => {
  const DEFAULT_PLACEHOLDER_IMAGE = "https://m.media-amazon.com/images/M/MV5BMTczNTI2ODUwOF5BMl5BanBnXkFtZTcwMTU0NTIzMw@@._V1_SX300.jpg";
  const poster = movie.Poster === "N/A" ? DEFAULT_PLACEHOLDER_IMAGE : movie.movie_imdb_info_cover;
  const link = '/movie/' + movie.movie_imdb_info_imdb_id;
  const [seconds] = useState(3);
  const navigate = useNavigate();
  const [errorState, setErrorState] = useState({});

  const [movieQuickAdd, { loading }] = useMutation(MOVIE_CREATE_QUICK_ADD_MUTATION);

  const handleQuickAddChangeBtn = (e) => {
    e.preventDefault();
    setErrorState({});
    movieQuickAdd({
      variables: {
        imdbId: movie.movie_imdb_info_imdb_id,
      },
    })
    .then(({ data: {movieCreate: { response },},}) => {
      if (response.success === true) {
        setTimeout(() => {
          // navigate("/home");
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
  };

  return (
    
    <Col lg="2" md="6" sm="6" className="mb-4">
      <Link to={link}>
        <div className="movie-card" style={{backgroundImage: `url(${poster})`}}>
            <Button>
                <i className="bx bx-play"></i>
            </Button>
        </div>
        
      </Link>
      <p>{truncate(movie.movie_imdb_info_title) || truncate(movie.movie_imdb_info_title)} 
        
      {movie.movie_imdb_info_user_added ? ( 
          <IconButton> 
            <CheckCircleOutlineIcon style={{color: "green"}}/> 
          </IconButton>
         ) : (
          <IconButton onClick={(e) => handleQuickAddChangeBtn(e)}> 
            <AddBoxOutlinedIcon/> 
          </IconButton>
      )}
      </p>
      
    </Col>
  );
};


export default MovieCard;

MovieCard.propTypes = {
  movie: PropTypes.object,
};

MovieCard.defaultProps = {
  movie: {},
}