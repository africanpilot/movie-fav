"use client";

import Image from "next/image";
import { BsPlayFill } from "react-icons/bs";
import CircularRate from "@/components/CircularRate";
import { MovieInfo } from '@/graphql/schema';
import Link from "next/link";

type Props = {
  netflixOriginals: MovieInfo[];
};

function HomeBanner({ netflixOriginals }: Props) {
  const movie = netflixOriginals?.[Math.floor(Math.random() * netflixOriginals?.length)]

  return (
    <div className="flex flex-col space-y-2 py-16 md:space-y-4 lg:h-[65vh] lg:justify-end lg:pb-12 lg:pl-24">
      <div className="absolute top-0 left-0 h-[95vh] w-screen -z-10">
        <Image
          src={movie?.cover || movie?.full_cover || ""}
          alt={movie?.title || "home image"}
          fill
          style={{objectFit:"cover"}}
        />
        <div className="absolute w-full h-[95vh] bg-gradient-to-r from-black to-transparent bottom-0 z-20" />
        <div className="absolute w-full h-14 bg-gradient-to-t from-[#141414] to-transparent bottom-0 z-20" />
      </div>
      <div className="space-y-5 relative top-24">
        <h1 className="text-2xl md:text-4xl lg:text-7xl font-bold text-white">
          {movie?.title}
        </h1>
        {movie?.popular_id && (
          <div className="flex justify-start gap-8 items-center cursor-pointer">
            <CircularRate value={movie?.popular_id} />
            <p className="bg-red-600 rounded-full px-2.5 py-2.5 text-sm w-20 text-center text-white">
              Action
            </p>
            <p className="bg-red-600 rounded-full px-2.5 py-2.5 text-sm w-20 text-center text-white">
              Drama
            </p>
          </div>
        )}
        <p className="max-w-xs text-shadow-md text-xs md:max-w-lg md:text-lg lg:max-w-2xl line-clamp-5 text-white">
          {movie?.plot}
        </p>
        <Link 
          href={`${movie?.videos?.[0] || movie?.trailer_link || ""}`}
          target="_blank"
          >
        <button className="flex gap-3 bg-red-600 px-2.5 py-2.5 rounded-md items-center text-white">
          <BsPlayFill />
          WATCH NOW
        </button>
        </Link>
      </div>
    </div>
  );
}

export default HomeBanner;
