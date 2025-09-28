"use client";

import { motion } from "framer-motion";
import { useShows } from "@/graphql";
import { ShowsInfoSortByEnum, OrderByEnum } from "@/graphql/schema";
import MovieCard from "@/components/MovieCard";
import Pagination from "@/components/pagination";
import { useSearchParams } from "next/navigation";
import { SumexusSettingsInterfaceProps } from "@/types/settings";

const Shows: React.FC<SumexusSettingsInterfaceProps> = ({ props }) => {
  const searchParams = useSearchParams();
  const currentPage = searchParams.get("page") || "1";
  const first = 30;
  const sortBy = [ShowsInfoSortByEnum.PopularId];
  const orderBy = OrderByEnum.Asc;
  const { showsPopular, isSaving: isLoading } = useShows({
    first,
    sortBy,
    orderBy,
    pageNumber: parseInt(currentPage),
  });
  const shows = showsPopular?.result || [];
  const pageCount = showsPopular?.pageInfo?.page_info_count || 100;
  const lastPage = Math.round(pageCount / first) + 1;

  return (
    <div>
      {shows && (
        <div className="relative pl-4 pb-24 lg:space-y-24">
          <div
            className="grid lg:grid-cols-5 sm:grid-cols-3 justify-items-center p-8 pt-28 gap-10"
            style={{ rowGap: "24px" }}
          >
            {shows?.map((show) => (
              <MovieCard key={show?.id} movie={show!} category="shows" />
            ))}
          </div>
          <Pagination
            category={"shows"}
            currentPage={parseInt(currentPage)}
            pageCount={lastPage}
          />
        </div>
      )}
    </div>
  );
};

export default Shows;
