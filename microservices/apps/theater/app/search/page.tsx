import React from "react";
import MainLayout from "@/components/Layouts/MainLayout";
import { Metadata } from "next";
import SearchComponent from "@/components/SearchComponent";

export const metadata: Metadata = {
  title: "Sumexus | Sumexus NEMT about Page",
  description:
    "Sumexus is a Premier local or long-distance Non-Emergency Medical Transport",
};

type Props = {};

function searchPage({}: Props) {
  return (
    <MainLayout>
      <div>
        <section id="search-home">
          <SearchComponent />
        </section>
      </div>
    </MainLayout>
  );
}

export default searchPage;
