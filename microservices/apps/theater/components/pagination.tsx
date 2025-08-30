import Link from "next/link"

type Props = {
    category: string;
    currentPage: number;
    pageCount: number;
};

const Pagination = ({category, currentPage, pageCount}: Props) => {
    const url = `/${category}?page=`
    const nextPage = (currentPage + 1) > 0 ? (currentPage + 1) : 1;
    const prevPage = (currentPage - 1) > 0 ? (currentPage - 1) : 1;
    const pageRows = Array.from({length: pageCount}, (_, i) => i + 1)

    return (
        <div className="flex items-center justify-between border-t border-gray-200 px-4 py-3 sm:px-6">
            <div className="flex flex-1 justify-between sm:hidden">
                <Link href={`${url}${prevPage}`} className="relative inline-flex items-center rounded-md border border-gray-300 px-4 py-2 text-sm font-medium hover:bg-red-400">Previous</Link>
                <Link href={`${url}${nextPage}`} className="relative ml-3 inline-flex items-center rounded-md border border-gray-300 px-4 py-2 text-sm font-medium hover:bg-red-400">Next</Link>
            </div>
            <div className="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
                <div>
                <p className="text-sm">
                    Showing
                    <span className="font-medium">{` ${currentPage} `}</span>
                    of
                    <span className="font-medium">{` ${pageCount} `}</span>
                    results
                </p>
                </div>
                <div>
                <nav className="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
                    <Link href={`${url}${prevPage}`} className="relative inline-flex items-center rounded-l-md px-2 py-2 ring-1 ring-inset ring-gray-300 hover:bg-red-400 focus:z-20 focus:outline-offset-0">
                        <span className="sr-only">Previous</span>
                        <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path fillRule="evenodd" d="M12.79 5.23a.75.75 0 01-.02 1.06L8.832 10l3.938 3.71a.75.75 0 11-1.04 1.08l-4.5-4.25a.75.75 0 010-1.08l4.5-4.25a.75.75 0 011.06.02z" clipRule="evenodd" />
                        </svg>
                    </Link>

                    { 
                        pageRows?.map(i => {
                            return <Link key={i} href={`${url}${i}`} className={i == currentPage ?
                                'relative z-10 inline-flex items-center bg-red-600 px-4 py-2 text-sm font-semibold text-white focus:z-20 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-600' :
                                'relative inline-flex items-center px-4 py-2 text-sm font-semibold ring-1 ring-inset ring-gray-300 hover:bg-red-400 focus:z-20 focus:outline-offset-0'}>{i}</Link>
                        })
                    }
        
                    <Link href={`${url}${nextPage}`} className="relative inline-flex items-center rounded-r-md px-2 py-2 ring-1 ring-inset ring-gray-300 hover:bg-red-400 focus:z-20 focus:outline-offset-0">
                        <span className="sr-only">Next</span>
                        <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path fillRule="evenodd" d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z" clipRule="evenodd" />
                        </svg>
                    </Link>
                </nav>
                </div>
            </div>
        </div>
    )
}

export default Pagination
