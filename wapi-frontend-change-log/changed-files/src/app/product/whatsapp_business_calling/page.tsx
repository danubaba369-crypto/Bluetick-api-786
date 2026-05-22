"use client";

import ComingSoonTemplate from "@/src/components/product/ComingSoonTemplate";
import { useAppSelector } from "@/src/redux/hooks";
import { PhoneCall } from "lucide-react";
import { useTranslation } from "react-i18next";

const VoiceCallingPage = () => {
  const { t } = useTranslation();
  const setting = useAppSelector((state) => state.setting);

  return <ComingSoonTemplate featureName="Voice Channel" title={`Make and receive official WhatsApp voice calls directly in ${setting.app_name || t("app_name")}`} description="No more switching to personal phones for calls. Resolve complex customer issues faster with clear, official voice calling integrated directly into your team's workflow." icon={<PhoneCall className="w-12 h-12" />} />;
};

export default VoiceCallingPage;
