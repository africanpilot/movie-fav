/* eslint jsx-a11y/anchor-is-valid: 0 */
import React, { useState } from "react";
import { Link, useNavigate } from 'react-router-dom';
import PropTypes from "prop-types";
import {Col, Card} from "reactstrap";
import './movie-card.scss';
import Button from '../button/Button';
import { IconButton } from '@mui/material';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import StarIcon from '@mui/icons-material/Star';

// import { useMutation } from "@apollo/client";
// import { MOVIE_CREATE_QUICK_ADD_MUTATION } from "../../graphql/Queries";


const truncate = (str) => {
  return str.length > 20 ? str.substring(0, 20) + "..." : str;
}

const CollectionsCard = ({ movie }) => {
  const DEFAULT_PLACEHOLDER_IMAGE = "https://m.media-amazon.com/images/M/MV5BMTczNTI2ODUwOF5BMl5BanBnXkFtZTcwMTU0NTIzMw@@._V1_SX300.jpg";
  const poster = movie.Poster === "N/A" ? DEFAULT_PLACEHOLDER_IMAGE : movie.movie_search_info.movie_imdb_info_cover;
  const link = '/movie/' + movie.movie_fav_info_imdb_id;

  return (
    
    <Col lg="2" md="6" sm="6" className="mb-4">
      <Link to={link}>
        <div className="movie-card" style={{backgroundImage: `url(${poster})`}}>
            <Button>
                <i className="bx bx-play"></i>
            </Button>
        </div>
        
      </Link>
      <span>{truncate(movie.movie_search_info.movie_imdb_info_title) || truncate(movie.movie_search_info.movie_imdb_info_title)} </span>
      <div className="tracking">
          {
            <div className="tracking">
              <span className="tracking__item">{"S01 | E"}{movie.movie_fav_info_episode_current || "01"}</span>
              <IconButton> 
                <CheckCircleOutlineIcon style={{color: "grey"}}/> 
              </IconButton>
              <span className="tracking__item">{movie.movie_fav_info_rating_user || "NA"}</span>
              <IconButton> 
                <StarIcon style={{color: "gold"}}/> 
              </IconButton>
            </div>
          }
        </div>

    </Col>
  );
};


export default CollectionsCard;

CollectionsCard.propTypes = {
  movie: PropTypes.object,
};

CollectionsCard.defaultProps = {
  movie: {},
}