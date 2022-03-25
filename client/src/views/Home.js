import React, { useState, useEffect } from "react";
import { Container, Row } from "reactstrap";
import PageTitle from "./../components/common/PageTitle";
import MovieCard from "../components/common/MovieCard";
import { useQuery } from "@apollo/client";
import { MOVIE_POPULAR_QUERY } from "../graphql/Queries";
import ServerError from "../util/ServerError.jsx";
import CircularProgress from "@material-ui/core/CircularProgress";


const Home = () => {
  // const movies = JSON.parse(localStorage.getItem("movies"));
  // const loading = false;

  const localMovies = JSON.parse(localStorage.getItem("movies"));
  console.log(localMovies);

  const [movies, setMovies] = useState(localMovies);
  const { data, loading, error } = useQuery(MOVIE_POPULAR_QUERY, {
    variables: { first: 18 },
    fetchPolicy: "network-only",
  });

  useEffect(() => {
    if (data ) {
      const {moviePopular: { result },} = data;
      setMovies(result);
      localStorage.setItem("movies", JSON.stringify(result, null, 2));
    }
  }, [data]);

  if (error) {
    console.log(JSON.stringify(data, null, 2));
    return <ServerError />;
  }

  if (data?.moviePopular.response.success === false) {
    return <div>You don't have an authority to do this</div>;
  }

  return (
    <Container fluid className="main-content-container px-4">
      <Row className="page-header py-4">
        <PageTitle title="Home" subtitle="Home Dashboard" className="text-sm-left mb-3" />    
      </Row>
      <Row>
      {loading ? ( 
        <CircularProgress 
          size={100}
          left={-20}
          top={50}
          status={'loading'}
          style={{marginLeft: '50%'}} 
        />
        ) : (
        movies && movies.map((item, index) => {
          return (
              <MovieCard key={index} movie={item}/>
          );
        })
      )}
      
      </Row>       
    </Container>
  );
}

export default Home;