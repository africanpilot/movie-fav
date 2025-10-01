"use client";

import React, { useEffect, useState } from "react";
import { useAccount } from "@gql/index";
import { useRouter } from "next/navigation";
import { ErrorState } from "@/types/error";

const GuestLogin = () => {
  const router = useRouter();
  const { accountGuestLogin, isSaving } = useAccount();
  const [errorState, setErrorState] = useState<ErrorState>({} as ErrorState);

  useEffect(() => {
    if (!localStorage.getItem("theater-guest-token")) {
      accountGuestLogin()
        .then((res) => {
          if (!res?.response.success) {
            setErrorState({ serverError: res?.response.message });
          } else {
            setErrorState({ message: res?.response.message });
            localStorage.setItem(
              "theater-guest-token",
              res?.result?.authenticationToken,
            );
            router.refresh();
          }
        })
        .catch((error) => {
          console.log("error", JSON.stringify(error, null, 2));
          setErrorState({
            serverError:
              "There is something wrong, please give us a minute to fix it!",
          });
        });
    }
  });

  if (isSaving) return <p>Loading...</p>;

  return null;
};

export default GuestLogin;
