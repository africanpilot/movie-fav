import Shows from "@/components/Shows"
import { MapData } from "@/types/settings"
import MainLayout from "@/components/Layouts/MainLayout"
import { Metadata } from "next"

export const metadata: Metadata = {
  title: "Sumexus | Sumexus NEMT about Page",
  description: "Sumexus is a Premier local or long-distance Non-Emergency Medical Transport",
};

const ShowsPage = () => {
  return (
    <MainLayout>
      <div>
        <section id="movies-home"><Shows props={MapData}/></section>
      </div>
    </MainLayout>
  );
};

export default ShowsPage;
