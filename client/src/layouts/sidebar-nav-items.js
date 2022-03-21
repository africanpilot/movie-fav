import HomeIcon from '@material-ui/icons/Home';
import TheatersIcon from '@material-ui/icons/Theaters';

const SideItemsData = () => [
  {
    title: "Home",
    to: "/home",
    htmlBefore: <HomeIcon/>,
    htmlAfter: ""
  },
  {
    title: "Movie Collections",
    to: "/movie-collections",
    htmlBefore: <TheatersIcon/>,
  },
  {
    title: "Tv/shows Collections",
    to: "/tv-shows-collections",
    htmlBefore: <TheatersIcon/>,
  },
];

export default SideItemsData;
