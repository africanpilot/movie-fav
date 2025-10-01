"use client";

import React, { useState } from "react";
import { useAccount } from "@/graphql";
import Link from "next/link";
import Image from "next/image";
import { MapData } from "@/types/settings";
import { ErrorState } from "@/types/error";
import { useRouter } from "next/navigation";
import { regexForEmail } from "@/util/regex";

const ForgotPassword = () => {
  const [errorState, setErrorState] = useState<ErrorState>({} as ErrorState);
  const { forgotPassword, isSaving } = useAccount();
  const router = useRouter();
  const [email, setEmail] = useState<string>("");

  const handleEmailChange = (e: {
    target: { value: React.SetStateAction<string> };
  }) => {
    setEmail(e.target.value);
  };

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

  const handleForgotPassword = (e: { preventDefault: () => void }) => {
    e.preventDefault();
    setErrorState({});
    if (!emailHelper(email)) {
      forgotPassword(email.trim())
        .then((res) => {
          // get a success response on client side, but rejected by server side
          if (res?.response.success) {
            localStorage.setItem("account-email", email.trim());
            router.push("/portal/forgot-password-verification");
          } else {
            setErrorState({ serverError: res?.response.message });
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
  };

  return (
    <div className="py-20 rounded-sm">
      <div className="flex flex-wrap items-center">
        <div className="w-full xl:block xl:w-1/2">
          <div className="px-26 py-17.5 text-center">
            <Link className="mb-5.5 inline-block" href="/">
              <Image
                className="hidden dark:block"
                src={MapData.logo}
                alt="Logo"
                width={176}
                height={32}
              />
              <Image
                className="dark:hidden"
                src={MapData.logo}
                alt="Logo"
                width={176}
                height={32}
              />
            </Link>

            <p className="2xl:px-20">
              {`Sumexus is a premier local or long-distance Non-Emergency Medical Transport`}
            </p>
          </div>
        </div>

        <div className="w-full border-stroke dark:border-strokedark xl:w-1/2 xl:border-l-2">
          <div className="w-full p-4 sm:p-12.5 xl:p-17.5 ">
            <h2 className="mb-9 text-2xl font-bold text-black dark:text-white sm:text-title-xl2 text-center">
              Sign In to Sumexus
            </h2>
            {Object.keys(errorState).length > 0 ? (
              <div
                className="md:col-gap-4 mb-5 p-4 py-3 text-sm text-red-800 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400"
                role="alert"
              >
                <span className="font-medium">{`Sign in failed!`}</span>{" "}
                {errorState.email ||
                  errorState.password ||
                  errorState.serverError}
              </div>
            ) : null}

            <form onSubmit={handleForgotPassword}>
              <div className="mb-4">
                <label className="mb-2.5 block font-medium text-black dark:text-white">
                  Email
                </label>
                <div className="relative">
                  <input
                    type="email"
                    placeholder="Enter your email"
                    name="email"
                    required
                    value={email}
                    onChange={handleEmailChange}
                    className="w-full rounded-lg border border-stroke bg-transparent py-4 pl-6 pr-10 text-black outline-none focus:border-primary focus-visible:shadow-none dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
                  />

                  <span className="absolute right-4 top-4">
                    <svg
                      className="fill-current"
                      width="22"
                      height="22"
                      viewBox="0 0 22 22"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <g opacity="0.5">
                        <path
                          d="M19.2516 3.30005H2.75156C1.58281 3.30005 0.585938 4.26255 0.585938 5.46567V16.6032C0.585938 17.7719 1.54844 18.7688 2.75156 18.7688H19.2516C20.4203 18.7688 21.4172 17.8063 21.4172 16.6032V5.4313C21.4172 4.26255 20.4203 3.30005 19.2516 3.30005ZM19.2516 4.84692C19.2859 4.84692 19.3203 4.84692 19.3547 4.84692L11.0016 10.2094L2.64844 4.84692C2.68281 4.84692 2.71719 4.84692 2.75156 4.84692H19.2516ZM19.2516 17.1532H2.75156C2.40781 17.1532 2.13281 16.8782 2.13281 16.5344V6.35942L10.1766 11.5157C10.4172 11.6875 10.6922 11.7563 10.9672 11.7563C11.2422 11.7563 11.5172 11.6875 11.7578 11.5157L19.8016 6.35942V16.5688C19.8703 16.9125 19.5953 17.1532 19.2516 17.1532Z"
                          fill=""
                        />
                      </g>
                    </svg>
                  </span>
                </div>
              </div>

              <div className="mb-5">
                <input
                  type="submit"
                  value="Submit"
                  className="w-full cursor-pointer bg-green-400 hover:bg-green-300 font-bold text-gray-900 py-2 px-6 rounded-full transition duration-300 ease-in-out transform hover:scale-105 hover:shadow-lg"
                />
              </div>

              <div className="mt-6 text-center">
                <p>
                  {`Don't have any account?`}{" "}
                  <Link href="/portal/signup" className="text-primary">
                    Sign Up
                  </Link>
                </p>
                <p>
                  {`Already have an account?`}{" "}
                  <Link href="/portal/signin" className="text-primary">
                    Sign in
                  </Link>
                </p>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword;
