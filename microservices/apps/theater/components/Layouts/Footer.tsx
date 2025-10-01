"use client";

import Copyright from "@/components/Layouts/Copyright";
import { SumexusSettingsInterfaceProps } from "@/types/settings";

const Footer: React.FC<SumexusSettingsInterfaceProps> = ({ props }) => {
  return (
    <footer className="pt-20 bg-white z-20" id="contact">
      <Copyright props={props} />
    </footer>
  );
};

export default Footer;
