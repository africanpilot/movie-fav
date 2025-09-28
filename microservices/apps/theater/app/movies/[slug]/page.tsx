"use client";

import React from "react";
import DetailsBanner from "@/components/DetailsBanner";
import MainLayout from "@/components/Layouts/MainLayout";
import { useMovie } from "@/graphql";
import { MovieInfoSortByEnum, OrderByEnum } from "@/graphql/schema";

export default function DetailsPage({ params }: { params: { slug: string } }) {
  const first = 20;
  const sortBy = [MovieInfoSortByEnum.Id];
  const orderBy = OrderByEnum.Desc;
  const { movieDetailsData, isSaving: loading } = useMovie(
    { first, sortBy, orderBy, pageNumber: 1 },
    { id: [parseInt(params.slug)] },
  );

  return (
    <MainLayout>
      <div>
        <section id={`movies-slug-${params.slug}`}>
          <DetailsBanner movieDetails={movieDetailsData!} />
        </section>
      </div>
    </MainLayout>
  );
}
