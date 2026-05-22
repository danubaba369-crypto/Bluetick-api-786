"use client";

import { Skeleton } from "@/src/elements/ui/skeleton";
import { useGetIsDemoModeQuery } from "@/src/redux/api/authApi";
import { DynamicLogoProps } from "@/src/types/auth";
import Image from "next/image";

const API_URL = process.env.NEXT_PUBLIC_STORAGE_URL ?? "";

const resolveUrl = (url?: string, onDark?: boolean): string => {
  if (!url || url.length <= 0) return onDark ? "/assets/logos/logo1.png" : "/assets/logos/logo3.png";
  return url.startsWith("http") ? url : `${API_URL}${url}`;
};

export const DynamicLogo = ({
  width = 240,
  height = 62,
  className = "h-15 w-auto sm:h-18 object-contain",
  skeletonClassName = "h-15 w-48 animate-pulse bg-transparent",
  onDark = false
}: {
  width?: number;
  height?: number;
  className?: string;
  skeletonClassName?: string;
  onDark?: boolean;
}) => {
  const { data: demoModeRes, isLoading } = useGetIsDemoModeQuery();

  if (isLoading) {
    return <Skeleton className={skeletonClassName} />;
  }

  const logoUrl = resolveUrl(onDark ? demoModeRes?.logo_light_url : demoModeRes?.logo_dark_url, onDark);

  return <Image src={logoUrl} alt="App Logo" width={width} height={height} className={className} unoptimized priority />;
};
