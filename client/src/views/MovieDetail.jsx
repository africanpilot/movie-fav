import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router';
import './detail.scss';
import StarBorderIcon from '@mui/icons-material/StarBorder';
import EditIcon from '@material-ui/icons/Edit';
import { IconButton } from '@mui/material';
import DeleteIcon from '@material-ui/icons/Delete';
import AddBoxOutlinedIcon from '@material-ui/icons/AddBoxOutlined';

import { useQuery } from "@apollo/client";
import { MOVIE_SEARCH_DETAIL_QUERY } from "../graphql/Queries";
import ServerError from "../util/ServerError.jsx";

import EditMovieModal from "../components/common/EditMovieModal";
import UseModal from "../components/common/UseModal";

import styled from 'styled-components';
import { Modal } from '../components/Modal';
import { ModalAdd } from '../components/ModalAdd';
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
	const [showModalAdd, setShowModalAdd] = useState(false);
	const openModal = () => {setShowModal(prev => !prev);};
	const openModalAdd = () => {setShowModalAdd(prev => !prev);};

	// const localMovies = JSON.parse(localStorage.getItem("movies"));
	const { id } = useParams();

	const [movie, setMovie] = useState({});
	const [collection, setCollection] = useState({});
	const { data, loading, error } = useQuery(MOVIE_SEARCH_DETAIL_QUERY, {
		variables: { search_type: "search_imdb_id", search_value: id},
		fetchPolicy: "network-only",
	});
	
	useEffect(() => {
		if (data ) {
			const {movieSearch: { result },} = data;
			console.log("result data",result ? result[0]["movie_fav_info"]: {})
			setMovie(result ? result[0]: {});
			setCollection(result ? result[0]["movie_fav_info"]: {})
			localStorage.setItem(id, JSON.stringify(result ? result[0]: {}, null, 2));
		}
	}, [data,id]);

	if (error) {
		console.log(JSON.stringify(data, null, 2));
		return <ServerError />;
	}

	if (data?.movieSearch.response.success === false) {
		return <div>You don't have an authority to do this</div>;
	}

	return (
		
		<div >
			<div className="banner" style={{backgroundImage: `url(${movie.movie_imdb_info_cover})`}}></div>
				<div className="mb-3 movie-content container" >
					<div className="movie-content__poster">
							<div className="movie-content__poster__img" style={{backgroundImage: `url(${movie.movie_imdb_info_cover})`}}></div>
					</div>
					
					<div className="movie-content__info" >

					<Modal showModal={showModal} setShowModal={setShowModal} movieFav={collection} setCollection={setCollection}/>
					<ModalAdd showModal={showModalAdd} setShowModal={setShowModalAdd} movieFav={collection} setCollection={setCollection}/>

							<h1 className="title">
									{movie.movie_imdb_info_title || movie.movie_imdb_info_title}
							</h1>
							<div className="genres">
									{
											movie.movie_imdb_info_genres && movie.movie_imdb_info_genres.slice(0, 5).map((genre, i) => (
													<span key={i} className="genres__item">{genre}</span>
											))
									}
							</div>
							<p className="overview">{movie.movie_imdb_info_plot}</p>
							
							<div className="cast">
							
									<div className="section__header">
											<h2>Casts</h2>
									</div>
									<div className="casts">
										{
											movie.movie_imdb_info_cast && movie.movie_imdb_info_cast.map((cast , i) => (
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
										{ collection.movie_fav_info_id ?(
											<>
											<IconButton onClick={openModal}> 
												<EditIcon style={{color: "#0d6efd"}}/> 
											</IconButton>
											<IconButton> 
												<DeleteIcon /> 
											</IconButton>
										</>
										) : (
												<>
												<IconButton onClick={openModalAdd}> 
													<AddBoxOutlinedIcon/> 
												</IconButton>
												<IconButton> 
													<DeleteIcon /> 
												</IconButton>
												</>
										)}
									</div>
								}
							</div>
					</div>
			</div>
		</div>
	);
}

export default MovieDetail;