"use client";

import { Skeleton } from "@/src/elements/ui/skeleton";
import { useGetIsDemoModeQuery } from "@/src/redux/api/authApi";

interface DynamicLogoProps {
  className?: string;
  skeletonClassName?: string;
}

export const DynamicLogo = ({
  className = "text-center my-2",
  skeletonClassName = "h-10 w-48 mx-auto"
}: DynamicLogoProps) => {
  const { isLoading } = useGetIsDemoModeQuery();

  if (isLoading) {
    return <Skeleton className={skeletonClassName} />;
  }

  return (
    <div className={`flex flex-col items-center justify-center ${className}`}>
      <span className="text-3xl sm:text-4xl font-black tracking-widest text-transparent bg-clip-text bg-gradient-to-r from-emerald-600 to-teal-500 dark:from-emerald-400 dark:to-teal-300 drop-shadow-sm uppercase">
        BLUE TICK API
      </span>
    </div>
  );
};
