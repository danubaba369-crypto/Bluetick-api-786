"use client";

import { useCallback, useMemo } from "react";
import { useAppSelector } from "@/src/redux/hooks";
import { useGetUserSubscriptionQuery } from "@/src/redux/api/subscriptionApi";
import { MENUITEMS } from "@/src/data/SidebarList";

export const useFeatureAccess = () => {
  const { isAuthenticated } = useAppSelector((state) => state.auth);
  const { data: subscriptionRes, isLoading: subLoading } = useGetUserSubscriptionQuery(undefined, {
    skip: !isAuthenticated,
  });

  const enabledFeatures = useMemo(() => {
    if (!subscriptionRes?.success) return null;
    const sub = subscriptionRes.data;
    return {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      ...((sub?.plan_id as any)?.enabled_features || {}),
      ...(sub?.enabled_features || {}),
    };
  }, [subscriptionRes]);

  const isFeatureEnabled = useCallback(
    (featureKey?: string) => {
      if (!featureKey) return true;
      if (subLoading) return true;
      if (!enabledFeatures) return true;
      return enabledFeatures[featureKey] !== false;
    },
    [enabledFeatures, subLoading]
  );

  const isPathEnabled = useCallback(
    (path: string) => {
      const item = MENUITEMS.find((m) => m.path === path || path.startsWith(m.path + "/"));
      if (!item || !item.featureKey) return true;
      return isFeatureEnabled(item.featureKey);
    },
    [isFeatureEnabled]
  );

  return { isFeatureEnabled, isPathEnabled, enabledFeatures, isLoading: subLoading };
};
