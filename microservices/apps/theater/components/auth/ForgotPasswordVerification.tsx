"use client";

import React, { useState } from "react"
import { useAccount } from "@/graphql";
import Link from "next/link";
import { MapData } from "@/types/settings"
import { ErrorState } from "@/types/error"
import { useRouter } from "next/navigation"
import { regexForEmail } from "@/util/regex"


const ForgotPasswordVerification = () => {
  const [errorState, setErrorState] = useState<ErrorState>({} as ErrorState);
  const { forgotPassword } = useAccount();
  const email = localStorage.getItem("account-email") || "";
  const router = useRouter();

  const emailHelper = (email: string) => {
    if (!email.match(regexForEmail)) {
      setErrorState({ email: "Please enter valid email address" });
      return true;
    } else if (email.length < 1) {
      setErrorState({ email: "Please enter email address" });
      return true;
    } else {
      return false;
    }
  };

  const handleResend = () => { 
    if (!email){
      router.push('/portal/forgot-password');
    }

    if (!emailHelper(email)) {
      forgotPassword(email.trim())
      .then( (res) => {
        // get a success response on client side, but rejected by server side
        if (res?.response.success) {
          localStorage.setItem("account-email", email.trim());
          router.push('/portal/signin');
        } else {
          setErrorState({ serverError: res?.response.message });
        }
      })
      .catch((error) => {
        console.log("error", JSON.stringify(error, null, 2));
        setErrorState({
          serverError: "There is something wrong, please give us a minute to fix it!",
        });
      }); 
    }
  };

  return (
    <div className="pt-28 text-center xl:text-left">
        <div className="p-6 md:mx-auto">
            <svg viewBox="0 0 24 24" className="text-green-600 w-16 h-16 mx-auto my-6">
                <path fill="currentColor"
                    d="M12,0A12,12,0,1,0,24,12,12.014,12.014,0,0,0,12,0Zm6.927,8.2-6.845,9.289a1.011,1.011,0,0,1-1.43.188L5.764,13.769a1,1,0,1,1,1.25-1.562l4.076,3.261,6.227-8.451A1,1,0,1,1,18.927,8.2Z">
                </path>
            </svg>
            <div className="text-center">
                {Object.keys(errorState).length > 0 ? (
                    <div className="md:col-gap-4 mb-5 p-4 py-3 text-sm text-red-800 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400" role="alert">
                        <span className="font-medium">Failed to send email</span> {errorState.email || errorState.password || errorState.serverError}
                    </div>
                ) : null}
                <h3 className="md:text-2xl text-base text-gray-900 font-semibold text-center">{'Password reset email sent'}</h3>
                <p className="text-gray-600 my-2">{`We sent a password reset link to ${email}. Please use the link to reset your password.`}</p>
                <p className="text-gray-600">{`If you don't see it, you may need to check your spam folder.`}</p>
                <p className="text-gray-600 cursor-pointer">
                  {"Still can't find the email? "}
                  <b onClick={handleResend}> {"Resend Email"}</b>
                </p>
                                  
                <div className="py-10 text-center">
                <Link href={MapData.signinPage} target="_top" className="bg-green-400 hover:bg-green-300 text-gray-700 py-2 px-6 rounded-full transition duration-300 ease-in-out transform hover:scale-105 hover:shadow-lg">{`Login`}</Link>
                </div>
            </div>
        </div>
    </div>
  );
};

export default ForgotPasswordVerification;
