import Home from "@/components/Home";
import { MapData } from "@/types/settings";
import { Metadata } from "next";
import MainLayout from "@/components/Layouts/MainLayout";

export const metadata: Metadata = {
  title: "Sumexus | Sumexus NEMT Home Page",
  description:
    "Sumexus is a Premier local or long-distance Non-Emergency Medical Transport, NEMT",
};

const HomePage = () => {
  return (
    <MainLayout>
      <div className="h-full">
        <section id="home">
          <Home props={MapData} />
        </section>
      </div>
    </MainLayout>
  );
};

export default HomePage;
