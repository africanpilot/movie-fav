import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    container: {
      padding: {
        DEFAULT: "15px",
      },
    },
    screens: {
      sm: "640px",
      md: "768px",
      lg: "960px",
      xl: "1200px",
      "2xsm": "375px",
    },
    extend: {
      colors: {
        primary: "#101828",
        secondary: "#667085",
        accent: {
          DEFAULT: "#ed1d24",
          hover: "#dd242a",
        },
        body: "#dedede",
        whiten: "#F1F5F9",
        bodydark: "#AEB7C0",
        bodydark1: "#DEE4EE",
        bodydark2: "#8A99AF",
        stroke: "#E2E8F0",
        strokedark: "#2E3A47",
        boxdark: "#24303F",
        "meta-4": "#313D4A",
        gray1: "#EFF4FB",
        black: "#1C2434",
        white: "#FFFFFF",
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
      animation: {
        "spin-slow": "spin 6s linear infinite",
      },
      fontFamily: {
        poppins: [`var(--font-poppins)`, "sans-serif"],
        sora: [`var(--font-sora)`, "sans-serif"],
        satoshi: ["Satoshi", "sans-serif"],
      },
      zIndex: {
        999999: "999999",
        99999: "99999",
        9999: "9999",
        999: "999",
        99: "99",
        9: "9",
        1: "1",
      },
      boxShadow: {
        7: "-5px 0 0 #313D4A, 5px 0 0 #313D4A",
        8: "1px 0 0 #313D4A, -1px 0 0 #313D4A, 0 1px 0 #313D4A, 0 -1px 0 #313D4A, 0 3px 13px rgb(0 0 0 / 8%)",
      },
      spacing: {
        7.5: "1.875rem",
      },
    },
  },
  container: {
    padding: {
      DEFAULT: "15px",
    },
  },
  plugins: [require("tailwind-scrollbar"), require("tailwind-scrollbar-hide")],
};
export default config;
