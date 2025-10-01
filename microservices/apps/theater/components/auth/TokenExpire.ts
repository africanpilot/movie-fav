"use client";

import React, { useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import jwt_decode from "jwt-decode";
import { useAccount } from "@gql/index";
import { ErrorState } from "@/types/error";

const TokenExpire = () => {
  const router = useRouter();
  const [errorState, setErrorState] = useState<ErrorState>({} as ErrorState);
  // const { accountAuthZeroLogin, isSaving } = useAccount();
  const pathname = usePathname();
  const returnLink = `/api/auth/login?returnTo=${encodeURIComponent("/portal")}`;

  useEffect(() => {
    const token = localStorage.getItem("theater-app-token");

    // allowed to access while getting a token
    const allowedLocations = [
      "/portal/signin",
      "/portal/signup",
      "/portal/email-verification",
      "/portal/forgot-password",
      "/portal/forgot-password-verification",
      "/portal/email-confirmation",
      "/portal/change-password",
    ];

    if (token) {
      try {
        const jwt_Token_decoded: { exp: number } = jwt_decode(token);
        if (jwt_Token_decoded.exp * 1000 <= Date.now()) {
          localStorage.clear();
          router.push("/portal/signin");
        }

        if (pathname === "/portal/signin") {
          router.push("/portal");
        }
      } catch (error: any) {
        localStorage.clear();
        router.push("/portal/signin");
      }
    } else {
      if (!allowedLocations.includes(pathname)) {
        router.push("/portal/signin");
      }

      // // query backend for a token
      // accountAuthZeroLogin()
      // .then((res) => {
      // 	if (!res?.response.success) {
      // 		setErrorState({ serverError: res?.response.message });
      // 	} else {
      // 		setErrorState({ message: res?.response.message });
      // 		localStorage.setItem("theater-app-token", res?.result?.authenticationToken);
      // 		router.refresh();
      // 	}
      // })
      // .catch((error) => {
      // 	console.log("error", JSON.stringify(error, null, 2));
      // 	router.push(returnLink);
      // });
    }
  });

  return null;
};

export default TokenExpire;
