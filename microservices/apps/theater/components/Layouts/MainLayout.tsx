"use client";
import React from "react";
import { MapData } from "@/types/settings";
import HeaderMain from "@/components/Layouts/HeaderMain";
import Footer from "@/components/Layouts/Footer";
import ToastContainerBar from "@/components/ToastContainer";

export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      <ToastContainerBar />
      <HeaderMain props={MapData} />
      <main>{children}</main>
      <Footer props={MapData} />
    </>
  );
}
