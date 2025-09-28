import type { Metadata } from "next";
import { Sora } from "next/font/google";
import "@/css/globals.css";
import GuestLogin from "@/components/auth/GuestLogin";
import { ApolloWrapper } from "./ApolloWrapper";

// font settings
const sora = Sora({
  subsets: ["latin"],
  variable: "--font-sora",
  weight: ["100", "200", "300", "400", "500", "600", "700", "800"],
});

export const metadata: Metadata = {
  title: "Theater",
  description: "Theater | Movie and Shows",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  typeof window !== "undefined"
    ? localStorage.removeItem("theater-email-token")
    : null;

  return (
    <html lang="en">
      <body
        suppressHydrationWarning={true}
        className={`page bg-[#f6fcff] text-black/60 bg-cover bg-no-repeat ${sora.variable} font-sora relative`}
      >
        <link rel="icon" href="/favicon.ico" sizes="any" />
        <ApolloWrapper>
          <GuestLogin />
          <div>{children}</div>
        </ApolloWrapper>
      </body>
    </html>
  );
}
