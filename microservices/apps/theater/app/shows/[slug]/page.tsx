"use client";

import React from "react";
import DetailsBanner from "@/components/DetailsBanner";
import MainLayout from "@/components/Layouts/MainLayout";
import { useShows } from "@/graphql";
import { ShowsInfoSortByEnum, OrderByEnum } from "@/graphql/schema";
import Seasons from "@/components/Seasons";

export default function DetailsPage({ params }: { params: { slug: string } }) {
  const first = 20;
  const sortBy = [ShowsInfoSortByEnum.Id];
  const orderBy = OrderByEnum.Desc;
  const { showsDetailsData, isSaving: loading } = useShows(
    { first, sortBy, orderBy, pageNumber: 1 },
    { id: [parseInt(params.slug)] },
  );

  return (
    <MainLayout>
      <div>
        <section id={`shows-slug-${params.slug}`}>
          <DetailsBanner movieDetails={showsDetailsData!} />
        </section>
        <section id={`shows-seasons-slug-${params.slug}`}>
          <Seasons showsDetails={showsDetailsData!} />
        </section>
      </div>
    </MainLayout>
  );
}
