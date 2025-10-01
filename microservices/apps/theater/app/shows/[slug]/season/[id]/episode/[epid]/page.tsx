"use client";

import React from "react";
import DetailsBanner from "@/components/DetailsBanner";
import MainLayout from "@/components/Layouts/MainLayout";
import { useShows } from "@/graphql";
import { ShowsInfoSortByEnum, OrderByEnum } from "@/graphql/schema";

export default function EpisodeDetailsPage({
  params,
}: {
  params: { slug: string; id: string; epid: string };
}) {
  const first = 20;
  const sortBy = [ShowsInfoSortByEnum.Id];
  const orderBy = OrderByEnum.Desc;
  const { showsDetailsData, isSaving: loading } = useShows(
    { first, sortBy, orderBy, pageNumber: 1 },
    { id: [parseInt(params.slug)] },
  );
  const season = showsDetailsData?.shows_season?.filter(
    (x) => x?.season == parseInt(params.id),
  )?.[0];
  const episode = season?.shows_episode?.filter(
    (x) => x?.episode == parseInt(params.epid),
  )?.[0];

  return (
    <MainLayout>
      {episode && (
        <div>
          <section id={`episode-slug-${params.slug}`}>
            <DetailsBanner movieDetails={episode!} />
          </section>
        </div>
      )}
    </MainLayout>
  );
}
