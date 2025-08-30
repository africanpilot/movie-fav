"use client";

import { useMovie, useShows } from "@/graphql"
import { MovieInfo, MovieInfoSortByEnum, OrderByEnum, ShowsInfo, ShowsInfoSortByEnum } from '@/graphql/schema'
import HomeBanner from "@/components/HomeBanner"
import Row from "@/components/Row"
import { SumexusSettingsInterfaceProps } from '@/types/settings'
import { FcSearch } from "react-icons/fc";


const Home: React.FC<SumexusSettingsInterfaceProps> = ({ props }) => {
  const orderBy = OrderByEnum.Asc;
  const { moviePopular, isSaving: movieLoading } = useMovie({first: 8, sortBy: [MovieInfoSortByEnum.PopularId], orderBy});
  const { showsPopular, isSaving: showsLoading } = useShows({first: 8, sortBy: [ShowsInfoSortByEnum.PopularId], orderBy});
  const isLoading = movieLoading || showsLoading
  
  return (
    <div>
      {isLoading ? (
          <div className="h-[300px] flex justify-center items-center">
            <FcSearch className="text-9xl animate-bounce" />
          </div>
        ) : (
        <div className="relative pl-4 pb-24 lg:space-y-24">
          <HomeBanner netflixOriginals={moviePopular?.result as MovieInfo[]} />
          <div className="md:space-y-24 pt-10">
            <Row movies={moviePopular?.result as MovieInfo[]} title="Trending Movies" isMain={true} category={"movies"}/>
            <Row movies={showsPopular?.result as ShowsInfo[]} title="Trending Shows" isMain={true} category={"shows"}/>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;
