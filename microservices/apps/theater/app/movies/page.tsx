import Movies from "@/components/Movies";
import { MapData } from "@/types/settings";
import MainLayout from "@/components/Layouts/MainLayout";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Sumexus | Sumexus NEMT about Page",
  description:
    "Sumexus is a Premier local or long-distance Non-Emergency Medical Transport",
};

const MoviesPage = () => {
  return (
    <MainLayout>
      <div>
        <section id="movies-home">
          <Movies props={MapData} />
        </section>
      </div>
    </MainLayout>
  );
};

export default MoviesPage;
