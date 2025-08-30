'use client'

import { motion } from "framer-motion";
import { useRouter } from "next/navigation";
import { ShowsInfo } from "@/graphql/schema";
import Container from "@/components/Container";

type Props = {
  showsDetails: ShowsInfo;
};

function Seasons({ showsDetails }: Props) {
  const router = useRouter();
  const navigatePage = (sessionId: number, sessionNumber: number) => {
    router.push(`/shows/${sessionId}/season/${sessionNumber}`);
  };

  return (
    <div className="px-4 pb-8">
      <Container header="Seasons">
        <div className="flex items-center scrollbar-hide space-x-0.5 overflow-x-scroll md:space-x-2.5 md:p-2 overflow-y-hidden">
          {showsDetails?.shows_season?.map((season) => (
            <motion.div
              initial={{ opacity: 0, scale: 0.5 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{
                duration: 0.8,
                delay: 0.5,
                ease: [0, 0.71, 0.2, 1.01],
              }}
              key={season?.id}
              className="relative h-28 min-w-[180px] cursor-pointer transition-transform duration-200 ease-out md:h-[400px] md:min-w-[200px] items-center"
              onClick={() =>
                navigatePage((showsDetails?.id || 1), (season?.season || 1))
              }
            >
              <p
                className={`text-lg py-2.5 text-gray-400 ${
                  !showsDetails?.cover && "animate-pulse"
                }`}
              >
                {season?.season}
              </p>
              {showsDetails?.cover ? (
                <img
                  src={`${showsDetails?.cover}`}
                  alt={`${showsDetails?.title} ${season?.season}`}
                  className="rounded-sm object-cover md:rounded w-[180px]"
                />
              ) : (
                <img
                  src="https://i0.wp.com/authormarystone.com/wp-content/uploads/2019/01/comingsoon.jpg?resize=576%2C864"
                  alt="img/no"
                  className="rounded-sm object-cover md:rounded w-[180px] animate-pulse"
                />
              )}

              <p
                className={`text-sm font-medium text-gray-400 text-start ${
                  !showsDetails?.cover && "animate-pulse"
                }`}
              >
                Season Number:{" "}
                <span className="">
                  {season?.season || "Not Yet"}
                </span>
              </p>
              <p
                className={`text-sm font-medium text-gray-400 text-start ${
                  !showsDetails?.cover && "animate-pulse"
                }`}
              >
                Episode Count:{" "}
                <span className="">
                  {season?.total_episodes || "Not Yet"}
                </span>
              </p>
              <p
                className={`text-sm font-medium text-gray-400 text-start ${
                  !showsDetails?.cover && "animate-pulse"
                }`}
              >
                Air Date:{" "}
                <span className="">
                  {season?.release_date || "Not Yet"}
                </span>
              </p>
            </motion.div>
          ))}
        </div>
      </Container>
    </div>
  );
}

export default Seasons;
