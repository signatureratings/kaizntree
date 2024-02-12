import { useLoaderData, Link } from "react-router-dom"

export const HomeIcon = () => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="w-8 h-8"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25"
      />
    </svg>
  )
}

const DashboardLoader = async () => {
  try {
    const response = await fetch("/api/v1/items/")
    return response.items
  } catch (error) {
    console.log(error)
  }
}

export function Dashboard() {
  const items = useLoaderData()
  return (
    <div className="flex flex-col mx-4 mt-4 flex-grow">
      {/* Top dashboard */}
      <div className="flex justify-between">
        <div className="flex flex-col">
          <div className=" font-bold text-3xl">Item Dashboard</div>
          <div className="mt-2 text-gray-600 tracking-wider">All items</div>
        </div>
        <div className="flex flex-col w-2/3">
          <div className="flex justify-between items-center border-b-2 border-gray-300 border-solid pb-2">
            <span className="ml-4">
              <HomeIcon />
            </span>
            <div className="mr-20 text-gray-600 tracking-wider">
              Total Categories
            </div>
            <div className="mr-20 text-gray-600 tracking-wider">4</div>
          </div>
          <div className="flex justify-between items-center pt-2">
            <span className="ml-4">
              <HomeIcon />
            </span>
            <div className="mr-20 text-gray-600 tracking-wider">
              Total Items
            </div>
            <div className="mr-20 text-gray-600 tracking-wider">21</div>
          </div>
        </div>
      </div>

      {/* New Item Category */}
      <Link className=" bg-green-600 my-5 ml-3 rounded-md p-2 tracking-widest w-56 text-white">
        NEW ITEM CATEGORY
      </Link>
      {/* Lower Dashboard */}
      <div className="container mx-auto p-2">
        <div className="flex m-2 items-center justify-between">
          <div className="flex items-center">
            <Link className=" bg-green-600 m-3 rounded-md p-2 tracking-widest w-28 text-white">
              NEW ITEM
            </Link>
            <div className="flex items-center border-2 rounded-md h-10 bg-slate-300 p-3">
              <div className="text-gray-400 tracking-wider">OPTIONS</div>
              <span>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  class="w-4 h-4"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="m19.5 8.25-7.5 7.5-7.5-7.5"
                  />
                </svg>
              </span>
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center border-solid border-b-2 justify-between pb-2 mr-5">
              <input
                type="text"
                name="search"
                placeholder="Search"
                className="w-96"
              ></input>
              <span>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  class="w-6 h-6"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"
                  />
                </svg>
              </span>
            </div>

            <div className="flex items-center justify-between mb-6 ">
              <span className="p-2 bg-slate-600 px-6 rounded-md">
                <HomeIcon />
              </span>
              <div className="flex items-end bg-gray-700 text-white rounded-full">
                <span className="border-2 rounded-full">
                  <HomeIcon />
                </span>
                <span className="">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    class="w-4 h-4"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="m19.5 8.25-7.5 7.5-7.5-7.5"
                    />
                  </svg>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
