export type SumexusSettings = {
  name: string;
  email: string;
  phoneSingle: string;
  phoneArea: string;
  address: string;
  googleMapsAddress: string;

  // Images
  logo: string;
  aboutBanner: string;
  bannerHome: string;
  aboutUsImage: string;
  servicesHeroImage: string;
  hoursOfServiceImage: string;
  hoursOfService2Image: string;
  hospiceImage: string;
  medTransportService: string;
  doctorsApt: string;
  transportation: string;
  aboutMeImage: string;
  traversaImage: string;
  encoreShadow: string;
  oxygenTank: string;

  // Routes
  homePage: string;
  moviesPage: string;
  showsPage: string;
  searchPage: string;
  confidentialityPage: string;
  contactPage: string;
  faqPage: string;
  requestTransportPage: string;
  aboutMissionVisionValuesSection: string;
  servicesFeatureSection: string;
  contactSuccessPage: string;
  signinPage: string;
  clientPortalPage: string;
};

export interface SumexusSettingsInterfaceProps {
  props: SumexusSettings;
}

export const MapData = {
  name: "MovieFav",
  email: "info@theater.com",
  phoneSingle: "817-997-4733",
  phoneArea: "(817) 997-4733",
  address: "2442 S Collins St Ste 108 PMB 1133 Arlington, TX 76014",
  googleMapsAddress: "https://maps.app.goo.gl/dGUGuvWn1PjGGQev8",

  // Images
  logo: "/PNG-01.png",
  aboutBanner: "/about-banner.jpeg",
  bannerHome: "/nemt-banner.webp",
  aboutUsImage: "/JPEG-02.jpg",
  servicesHeroImage: "/Logo Mock-Up 2.jpg",
  hoursOfServiceImage: "/hoursofservice.jpeg",
  hoursOfService2Image: "/hoursofservice2.jpg",
  hospiceImage: "/hospice.jpg",
  medTransportService: "/medtransportservice.jpg",
  doctorsApt: "/doctorapt2.jpg",
  transportation: "/transportation.jpg",
  aboutMeImage: "/aboutme2.jpg",
  traversaImage: "/Traversa_Shadow.png",
  encoreShadow: "/encoreShadow.png",
  oxygenTank: "/oxygenTank.jpeg",

  // Routes
  homePage: "/",
  moviesPage: "/movies",
  showsPage: "/shows",
  searchPage: "/search",
  confidentialityPage: "/confidentiality",
  contactPage: "/contact",
  faqPage: "/faq",
  requestTransportPage: "/request-transport",
  aboutMissionVisionValuesSection: "/about#mission-vision-values-about",
  servicesFeatureSection: "/services#features",
  contactSuccessPage: "/contact-success",
  signinPage: "/portal/signin",
  clientPortalPage: "/portal",
};
