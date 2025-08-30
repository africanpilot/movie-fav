"use client";

import Image from "next/image";
import uiConfigs from "@/config/ui.configs";
import { Box, Chip, Divider, Stack, Typography } from "@mui/material";
import { BsPlayFill } from "react-icons/bs";
import CastSlide from "@/components/CastSlide";
import CircularRate from "@/components/CircularRate";
import Container from "@/components/Container";
import { MovieInfo, PersonInfo, DownloadTypeEnum, ShowsInfo, ShowsEpisode } from "@/graphql/schema";
import { useMovie } from "@/graphql";
import Link from "next/link";
import { toast } from "react-toastify";


type Props = {
  movieDetails: MovieInfo | ShowsInfo | ShowsEpisode | any;
};

function DetailsBanner({ movieDetails }: Props) {
  const { movieDownload, isSaving } = useMovie();

    const handleDownload = (e: { preventDefault: () => void; }, download_type: DownloadTypeEnum) => {
        movieDownload(
          [{imdb_id: (movieDetails?.imdb_id!), download_type: download_type}]
        ).then((res) => {
          window.open(process.env.NEXT_PUBLIC_TRANSMISSION, "_blank")
        })
        .catch((err) => {
			console.log("ERR", JSON.stringify(err, null, 2));
			toast.error("There is something wrong, please give us a minute to fix it!");
		});
    };

  return (
    <>
      <Box
        sx={{
          zIndex: "-1",
          position: "relative",
          paddingTop: { xs: "60%", sm: "40%", md: "35%" },
          backgroundPosition: "top",
          backgroundSize: "cover",
          backgroundImage: `url(${movieDetails?.cover || movieDetails?.full_cover})`,
          backgroundAttachment: "fixed",
          "&::before": {
            content: '""',
            position: "absolute",
            left: 0,
            bottom: 0,
            width: "100%",
            height: "100%",
            pointerEvents: "none",
            ...uiConfigs.style.gradientBgImage.dark,
          },
        }}
      />
      <Box
        sx={{
          color: "primary.contrastText",
          ...uiConfigs.style.mainContent,
        }}
      >
        <Box
          sx={{
            marginTop: { xs: "-10rem", md: "-15rem", lg: "-20rem" },
          }}
        >
          <Box
            sx={{
              display: "flex",
              flexDirection: { md: "row", xs: "column" },
            }}
          >
            <Box
              sx={{
                width: { xs: "70%", sm: "50%", md: "40%" },
                margin: { xs: "0 auto 2rem", md: "0 2rem 0 0" },
              }}
            >
              <Box
                sx={{
                  paddingTop: "140%",
                  ...uiConfigs.style.backgroundImage(movieDetails?.cover || movieDetails?.full_cover!),
                }}
              />
            </Box>
            <Box
              sx={{
                width: { xs: "100%", md: "60%" },
                color: "#fff",
              }}
            >
              <Stack spacing={5}>
                <Typography
                  variant="h4"
                  fontSize={{ xs: "2rem", md: "2rem", lg: "4rem" }}
                  fontWeight="700"
                  sx={{ ...uiConfigs.style.typoLines(2, "left") }}
                  color="#fff"
                >
                  {movieDetails?.title}
                </Typography>
                <Stack direction="row" spacing={1} alignItems="center" className="flex-wrap">
                  <CircularRate
                    value={movieDetails?.popular_id || 1}
                    isPoster={false}
                  />
                  <Divider orientation="vertical" />
                  {movieDetails?.genres?.map((genre: any, index: any) => (
                    <Chip
                      label={genre}
                      variant="filled"
                      color="error"
                      key={index}
                    />
                  ))}
                </Stack>
                <p className="text-white">{movieDetails?.plot}</p>
                <Stack direction="row" spacing={1} className="pt-6">
                  <Link
                    className="flex gap-3 bg-red-600 px-2.5 py-2.5 rounded-md items-center"
                    href={`${movieDetails?.videos?.[0] || ""}`}
                    target="_blank"
                  >
                    <BsPlayFill />
                    Watch Trailer
                  </Link>
                  {movieDetails?.download_1080p_url && (
                    <button
                      className="flex gap-3 bg-gray-400 px-2.5 py-2.5 rounded-md items-center"
                      onClick={(e: { preventDefault: () => void; }) => handleDownload(e, DownloadTypeEnum.Download_1080p)}
                    >
                      <BsPlayFill />
                      {DownloadTypeEnum.Download_1080p.replace("DOWNLOAD_","")}
                    </button>
                  )}
                  {movieDetails?.download_720p_url && (
                    <button
                      className="flex gap-3 bg-gray-400 px-2.5 py-2.5 rounded-md items-center"
                      onClick={(e: { preventDefault: () => void; }) => handleDownload(e, DownloadTypeEnum.Download_720p)}
                    >
                      <BsPlayFill />
                      {DownloadTypeEnum.Download_720p.replace("DOWNLOAD_","")}
                    </button>
                  )}
                  {movieDetails?.download_480p_url && (
                    <button
                      className="flex gap-3 bg-gray-400 px-2.5 py-2.5 rounded-md items-center"
                      onClick={(e: { preventDefault: () => void; }) => handleDownload(e, DownloadTypeEnum.Download_480p)}
                    >
                      <BsPlayFill />
                      {DownloadTypeEnum.Download_480p.replace("DOWNLOAD_","")}
                    </button>
                  )}
                </Stack>
                {movieDetails?.casts && (
                  <Container header="cast">
                    <CastSlide casts={movieDetails?.casts as PersonInfo[]} />
                  </Container>
                )}
              </Stack>
            </Box>
          </Box>
        </Box>
      </Box>
    </>
  );
}

export default DetailsBanner;
