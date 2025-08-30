'use client'

import React, { useEffect, useState } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { useMediaQuery } from 'react-responsive'
import { BiMenuAltRight, BiX } from 'react-icons/bi'
import { SumexusSettingsInterfaceProps } from '@/types/settings'


const HeaderMain: React.FC<SumexusSettingsInterfaceProps> = ({ props }) => {
  const [header, setHeader] = useState(false);
  const [nav, setNav] = useState(false);
  const [isDesktop, setIsDesktop] = useState(false);
  const returnLink = `/api/auth/login?returnTo=${encodeURIComponent('/portal')}`;
  
  const desktopMode = useMediaQuery({
    query: '(min-width: 1300px)',
  });

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 40) {
        setHeader(true);
      } else {
        setHeader(false);
      }
    };
    setIsDesktop(desktopMode)
    window.addEventListener('scroll', handleScroll);
    return () => {window.removeEventListener('scroll', handleScroll);};
  }, [desktopMode]);

  return (
    <header className="bg-white shadow-md py-2 fixed w-full max-w-[1920px] mx-auto z-20 transition-all duration-300">
      <div className='xl:container mx-auto flex flex-col xl:flex-row xl:items-center xl:justify-between'>
        <div 
        className={`flex justify-between items-center px-4 ${
          desktopMode ? 'w-1/2' : 'w-full'
        } bg-white gap-y-6 font-bold xl:font-medium xl:flex-row xl:w-max xl:gap-x-8 xl:h-max xl:bg-transparent xl:pb-0 transition-all duration-150 text-center xl:text-left uppercase text-sm xl:text-[15px] xl:normal-case`}
        >
          <Link href={props.homePage} className='cursor-pointer'>
            {/* <Image src={props.logo} width={150} height={100} alt='' priority={true}/> */}
            <p className="font-bold text-3xl">
              Theater<span className="text-red-500">App</span>
            </p>
          </Link>

          {/* nav */}
        <nav
          className={`${
            nav ? 'max-h-max py-8 px-2 xl:py-0 xl:px-0' : 'max-h-0 xl:max-h-max'
          } flex flex-col w-full bg-white gap-y-6 overflow-hidden font-bold xl:font-medium xl:flex-row xl:w-max xl:gap-x-8 xl:h-max xl:bg-transparent xl:pb-0 transition-all duration-150 text-center xl:text-left uppercase text-sm xl:text-[13px] xl:normal-case`}
        >
          <Link className={'cursor-pointer'} href={props.homePage} onClick={desktopMode ? () => {} : () => setNav(!nav)}>
            {'Home'}
          </Link>
          <Link className={'cursor-pointer'} href={props.moviesPage} onClick={desktopMode ? () => {} : () => setNav(!nav)}>
            {'Movies'}
          </Link>
          <Link className={'cursor-pointer'} href={props.showsPage} onClick={desktopMode ? () => {} : () => setNav(!nav)}>
            {'Shows'}
          </Link>
          <Link className={'cursor-pointer'} href={props.searchPage} onClick={desktopMode ? () => {} : () => setNav(!nav)}>
            {'Search'}
          </Link>
        </nav>
          
          {/* nav open menu */}
          <div
            onClick={() => setNav(!nav)}
            className='cursor-pointer xl:hidden'
          >
            {nav ? (
              <BiX className={`${header ? '' : ''} text-4xl`} />
            ) : (
              <BiMenuAltRight className={`${header ? '' : ''} text-4xl`} />
            )}
          </div>
        </div>
      </div>
    </header>
  );
}

export default HeaderMain;
