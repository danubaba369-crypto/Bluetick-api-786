"use client";

import { Skeleton } from "@/src/elements/ui/skeleton";
import { useGetIsDemoModeQuery } from "@/src/redux/api/authApi";
import Image from "next/image";

interface DynamicLogoProps {
  width?: number;
  height?: number;
  className?: string;
  skeletonClassName?: string;
}

const API_URL = process.env.NEXT_PUBLIC_STORAGE_URL ?? "";

const resolveUrl = (url?: string): string => {
  if (!url || url.length <= 0) return "/assets/logos/logo3.png";
  if (url.startsWith("http")) return url;
  const baseUrl = API_URL.endsWith("/") ? API_URL.slice(0, -1) : API_URL;
  const path = url.startsWith("/") ? url : `/${url}`;
  return `${baseUrl}${path}`;
};

export const DynamicLogo = ({
  width = 240,
  height = 62,
  className = "h-15 w-auto sm:h-18 object-contain mx-auto",
  skeletonClassName = "h-15 w-52 sm:h-18 mx-auto"
}: DynamicLogoProps) => {
  const { data: demoModeRes, isLoading } = useGetIsDemoModeQuery();

  if (isLoading) {
    return <Skeleton className={skeletonClassName} />;
  }

  const logoUrl = resolveUrl(demoModeRes?.logo_dark_url);

  return (
    <Image
      src={logoUrl}
      alt="App Logo"
      width={width}
      height={height}
      className={className}
      unoptimized
      priority
    />
  );
};
