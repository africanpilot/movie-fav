import React, { useState, useEffect } from "react";
import { Container, Row } from "reactstrap";
import PageTitle from "../components/common/PageTitle";
import CollectionsCard from "../components/common/CollectionsCard";
import { useQuery } from "@apollo/client";
import { MOVIE_FAV_QUERY } from "../graphql/Queries";
import ServerError from "../util/ServerError.jsx";
import CircularProgress from "@material-ui/core/CircularProgress";

const TvShowsCollections = () => {
  const localCollections = JSON.parse(localStorage.getItem("tv-shows-collections"));
  console.log(localCollections);

  const [collections, setCollections] = useState(localCollections);
  const { data, loading, error } = useQuery(MOVIE_FAV_QUERY, {
    variables: { first: 18 },
    fetchPolicy: "network-only",
  });

  useEffect(() => {
    if (data ) {
      const {movieFav: { result },} = data;
      setCollections(result);
      localStorage.setItem("tv-shows-collections", JSON.stringify(result, null, 2));
    }
  }, [data]);

  if (error) {
    console.log(JSON.stringify(data, null, 2));
    return <ServerError />;
  }

  if (data?.movieFav.response.success === false) {
    return <div>You don't have an authority to do this</div>;
  }

  return (
    
    <Container fluid className="main-content-container px-4">
      <Row className="page-header py-4">
        <PageTitle title="Tv/Shows Collections" subtitle="My Tv/Shows Collections" className="text-sm-left mb-3" />    
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
          collections && collections.map((item, index) => {
          return (
              <CollectionsCard key={index} movie={item}/>
          );
        })

      )}
        
      </Row>       
    </Container>  
  );
};


export default TvShowsCollections;