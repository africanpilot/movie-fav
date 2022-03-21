import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router';
import './detail.scss';
import StarBorderIcon from '@mui/icons-material/StarBorder';
import EditIcon from '@material-ui/icons/Edit';
import { IconButton } from '@mui/material';
import DeleteIcon from '@material-ui/icons/Delete';

import { useMutation } from "@apollo/client";
import { MOVIE_MODIFY_MUTATION } from "../graphql/Queries";

import EditMovieModal from "../components/common/EditMovieModal";
import UseModal from "../components/common/UseModal";

import styled from 'styled-components';
import { Modal } from '../components/Modal';
import { GlobalStyle } from './globalStyles';

const Container = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
`;

const Button = styled.button`
  min-width: 100px;
  padding: 16px 32px;
  border-radius: 4px;
  border: none;
  background: #141414;
  color: #fff;
  font-size: 24px;
  cursor: pointer;
`;

const MovieDetail = () => {

	const [showModal, setShowModal] = useState(false);
	const openModal = () => {setShowModal(prev => !prev);};

	const localMovies = JSON.parse(localStorage.getItem("movies"));
	const { id } = useParams();
	// const [item, setItem] = useState(null);
	var item = {};
	localMovies.filter(function(idx) {
			if(idx["movie_imdb_info_imdb_id"] === id){
					item = idx ;
			}
			return idx;
	});

	// get the account movie fav info
	const localMovieCollection = JSON.parse(localStorage.getItem("movie-collections"));
	const localTvShowCollection = JSON.parse(localStorage.getItem("tv-shows-collections"));
	var collection = {};
	localMovieCollection.filter(function(idx) {
			if(idx["movie_fav_info_imdb_id"] === id){
				collection = idx ;
			}
			return idx;
	});
	
	console.log("collection: ", collection);

	// query data if not available

	// modify movie fav
	// const [movieModify, { loading }] = useMutation(MOVIE_MODIFY_MUTATION);

	const handleEditClickBtn = (e) => {

	}



	return (
		
		<div >
				<div className="banner" style={{backgroundImage: `url(${item.movie_imdb_info_cover})`}}></div>
					<div className="mb-3 movie-content container" >
						<div className="movie-content__poster">
								<div className="movie-content__poster__img" style={{backgroundImage: `url(${item.movie_imdb_info_cover})`}}></div>
						</div>
						
						<div className="movie-content__info" >
						<Modal showModal={showModal} setShowModal={setShowModal} movieFav={collection}/>	
								<h1 className="title">
										{item.movie_imdb_info_title || item.movie_imdb_info_title}
								</h1>
								<div className="genres">
										{
												item.movie_imdb_info_genres && item.movie_imdb_info_genres.slice(0, 5).map((genre, i) => (
														<span key={i} className="genres__item">{genre}</span>
												))
										}
								</div>
								<p className="overview">{item.movie_imdb_info_plot}</p>
								
								<div className="cast">
								
										<div className="section__header">
												<h2>Casts</h2>
										</div>
										<div className="casts">
											{
												item.movie_imdb_info_cast && item.movie_imdb_info_cast.map((cast , i) => (
													<div key={i} className="casts__item">
														<div className="casts__item__img" style={{backgroundImage: `url(${cast.image})`}}></div>
														<span key={i} className="casts__item__name">{cast.name}</span>
													</div>
												))
											
											}
											
										</div>
										
								</div>
							
								<div className="tracking">
									{
										<div className="tracking">
											<span className="tracking__item">{collection.movie_fav_info_status || "unmarked"}</span>
											<span className="tracking__item">{collection.movie_fav_info_rating_user || "N/A"}</span>
											<span className="tracking__item">{"9.2"}</span>
											<span className="tracking__item">{"S01 | E"}{collection.movie_fav_info_episode_current || "01"}</span>
											<IconButton onClick={openModal}> 
												<EditIcon style={{color: "#0d6efd"}}/> 
											</IconButton>
											<IconButton> 
												<DeleteIcon /> 
											</IconButton>
											
										</div>
									}
								</div>
								
						</div>
				</div>
				
	
		</div>
	);
}

export default MovieDetail;