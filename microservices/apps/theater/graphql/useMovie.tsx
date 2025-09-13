import { 
    useMoviePopularQuery, MovieInfoPageInfoInput,
    useMovieDetailsQuery, MovieInfoFilterInput,
    useMovieUpdateMutation
} from "./schema";


export const useMovie = (pageInfo: MovieInfoPageInfoInput = {}, filterInput: MovieInfoFilterInput = {}) => {
    const [movieUpdate, { loading: isMovieUpdate }] = useMovieUpdateMutation();


    const handleMovieUpdate = async (movieInfoId: number) => {
      try {
        const { data } = await movieUpdate({ variables: { movieInfoId } });
        return data?.movieUpdate;
      } catch (error: any) {
        try { return JSON.parse(error.message) } catch (error: any) { throw error;};
      }
    };

    try {

        const { data , loading: isMoviePopular, error: isMovieError, refetch: moviePopularRefetch } = useMoviePopularQuery(
            { 
                variables: { pageInfo: pageInfo },
                fetchPolicy: 'cache-and-network',
                nextFetchPolicy: 'cache-first',
                // skip: skip
            }
        );

        const moviePopular = data?.movieInfo;


        const { data: movieDetails , loading: isMovieDetails, error: isMovieDetailsError, refetch: movieDetailsRefetch } = useMovieDetailsQuery(
            { 
                variables: { filterInput: filterInput },
                fetchPolicy: 'cache-and-network',
                nextFetchPolicy: 'cache-first',
                // skip: skip
            }
        );

        const movieDetailsData = movieDetails?.movieInfo?.result?.[0];
        const isSaving = (isMovieUpdate);

        return {
            moviePopular,
            isMoviePopular,
            isMovieError,
            moviePopularRefetch,
            movieDetailsData,
            isMovieDetails,
            isMovieDetailsError,
            movieDetailsRefetch,
            movieUpdate: handleMovieUpdate,
            isSaving
        };
      } catch (error) {
        throw error;
    }
};
