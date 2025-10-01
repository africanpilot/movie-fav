import {
  useMoviePopularQuery,
  MovieInfoPageInfoInput,
  useMovieDetailsQuery,
  MovieInfoFilterInput,
} from "./schema";

export const useMovie = (
  pageInfo: MovieInfoPageInfoInput = {},
  filterInput: MovieInfoFilterInput = {},
) => {
  try {
    const {
      data,
      loading: isMoviePopular,
      error: isMovieError,
      refetch: moviePopularRefetch,
    } = useMoviePopularQuery({
      variables: { pageInfo: pageInfo },
      fetchPolicy: "cache-and-network",
      nextFetchPolicy: "cache-first",
      // skip: skip
    });

    const moviePopular = data?.movieInfo;

    const {
      data: movieDetails,
      loading: isMovieDetails,
      error: isMovieDetailsError,
      refetch: movieDetailsRefetch,
    } = useMovieDetailsQuery({
      variables: { filterInput: filterInput },
      fetchPolicy: "cache-and-network",
      nextFetchPolicy: "cache-first",
      // skip: skip
    });

    const movieDetailsData = movieDetails?.movieInfo?.result?.[0];
    const isSaving = false;

    return {
      moviePopular,
      isMoviePopular,
      isMovieError,
      moviePopularRefetch,
      movieDetailsData,
      isMovieDetails,
      isMovieDetailsError,
      movieDetailsRefetch,
      isSaving,
    };
  } catch (error) {
    throw error;
  }
};
