"use client";

import ComingSoonTemplate from "@/src/components/product/ComingSoonTemplate";
import { useAppSelector } from "@/src/redux/hooks";
import { Instagram } from "lucide-react";
import { useTranslation } from "react-i18next";

const MultiChannelPage = () => {
  const { t } = useTranslation();
  const setting = useAppSelector((state) => state.setting);

  return <ComingSoonTemplate featureName="Social Commerce" title="Sell more by connecting Instagram and Facebook to your WhatsApp" description={`Manage all your social media sales and customer queries in one simple dashboard. Engage with customers on Instagram and Messenger without leaving ${setting.app_name || t("app_name")}.`} icon={<Instagram className="w-12 h-12" />} />;
};

export default MultiChannelPage;
