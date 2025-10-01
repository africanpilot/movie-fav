"use client";

import React from "react";
import MainLayout from "@/components/Layouts/MainLayout";
import { useShows } from "@/graphql";
import { ShowsInfoSortByEnum, OrderByEnum } from "@/graphql/schema";
import EpisodeCard from "@/components/EpisodeCard";

export default function SeasonDetailsPage({
  params,
}: {
  params: { slug: string; id: string };
}) {
  const first = 20;
  const sortBy = [ShowsInfoSortByEnum.Id];
  const orderBy = OrderByEnum.Desc;
  const { showsDetailsData, isSaving: loading } = useShows(
    { first, sortBy, orderBy, pageNumber: 1 },
    { id: [parseInt(params.slug)] },
  );
  const episodes = showsDetailsData?.shows_season?.filter(
    (x) => x?.season == parseInt(params.id),
  )?.[0]?.shows_episode;

  return (
    <MainLayout>
      <div className="relative pl-4 pb-24 lg:space-y-24">
        <div
          className="grid lg:grid-cols-5 sm:grid-cols-3 justify-items-center p-8 pt-28 gap-10"
          style={{ rowGap: "24px" }}
        >
          {episodes?.map((episode) => (
            <EpisodeCard key={episode?.id} episode={episode!} />
          ))}
        </div>
      </div>
    </MainLayout>
  );
}
