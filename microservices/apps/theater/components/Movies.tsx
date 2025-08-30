"use client"

import { motion } from "framer-motion";
import { useMovie } from "@/graphql";
import { MovieInfoSortByEnum, OrderByEnum } from '@/graphql/schema';
import MovieCard from "@/components/MovieCard";
import Pagination from "@/components/pagination";
import { useSearchParams } from "next/navigation"
import { SumexusSettingsInterfaceProps } from "@/types/settings";


const Movies: React.FC<SumexusSettingsInterfaceProps> = ({ props }) => {
    const searchParams = useSearchParams();
    const currentPage = searchParams.get("page") || "1";
    const first = 30;
    const sortBy = [MovieInfoSortByEnum.PopularId];
    const orderBy = OrderByEnum.Asc;
    const { moviePopular, isSaving: isLoading } = useMovie({ first, sortBy, orderBy, pageNumber: parseInt(currentPage)});
    const movies = moviePopular?.result || [];
    const pageCount = moviePopular?.pageInfo?.page_info_count || 100;
    const lastPage = (Math.round(pageCount/first) + 1);
    
  
    return (
        <div>
            {movies && (
            <div className="relative pl-4 pb-24 lg:space-y-24">
              <div className="grid lg:grid-cols-5 sm:grid-cols-3 justify-items-center p-8 pt-28 gap-10" style={{rowGap: "24px"}}>
                {movies?.map((movie) => (
                  <MovieCard key={movie?.id} movie={movie!} category="movies" />
                ))}
              </div>
              <Pagination 
                category={"movies"}
                currentPage={parseInt(currentPage)}
                pageCount={lastPage}
              />
            </div>
          )}
        </div>
    );
};

export default Movies;
