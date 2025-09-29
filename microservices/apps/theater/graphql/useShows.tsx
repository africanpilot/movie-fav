import {
  useShowsPopularQuery,
  ShowsInfoPageInfoInput,
  useShowsDetailsQuery,
  ShowsInfoFilterInput,
  useShowsEpisodeDetailsQuery,
} from "./schema";

export const useShows = (
  pageInfo: ShowsInfoPageInfoInput = {},
  filterInput: ShowsInfoFilterInput = {},
) => {
  try {
    const {
      data,
      loading: isShowsPopular,
      error: isShowsError,
      refetch: showsPopularRefetch,
    } = useShowsPopularQuery({
      variables: { pageInfo: pageInfo },
      fetchPolicy: "cache-and-network",
      nextFetchPolicy: "cache-first",
      // skip: skip
    });

    const showsPopular = data?.showsInfo;

    const {
      data: showsDetails,
      loading: isShowsDetails,
      error: isShowsDetailsError,
      refetch: showsDetailsRefetch,
    } = useShowsDetailsQuery({
      variables: { filterInput: filterInput },
      fetchPolicy: "cache-and-network",
      nextFetchPolicy: "cache-first",
      // skip: skip
    });

    const showsDetailsData = showsDetails?.showsInfo?.result?.[0];

    const {
      data: showsEpisodeDetails,
      loading: isShowsEpisodeDetails,
      error: isShowsEpisodeDetailsError,
      refetch: showsEpisodeDetailsRefetch,
    } = useShowsEpisodeDetailsQuery({
      variables: { filterInput: filterInput },
      fetchPolicy: "cache-and-network",
      nextFetchPolicy: "cache-first",
      // skip: skip
    });

    const showsEpisodeDetailsData =
      showsEpisodeDetails?.showsEpisode?.result?.[0];
    const isSaving = false;

    return {
      showsPopular,
      isShowsPopular,
      isShowsError,
      showsPopularRefetch,
      showsDetailsData,
      isShowsDetails,
      isShowsDetailsError,
      showsDetailsRefetch,
      showsEpisodeDetailsData,
      isShowsEpisodeDetails,
      isShowsEpisodeDetailsError,
      showsEpisodeDetailsRefetch,
      isSaving,
    };
  } catch (error) {
    throw error;
  }
};
