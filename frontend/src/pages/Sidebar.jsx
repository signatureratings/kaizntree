import { Link, Outlet } from "react-router-dom"

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
export function Sidebar() {
  const LowerSidebarItems = [
    {
      path: "/",
      icon: <HomeIcon />,
      text: "Home",
    },
    {
      path: "/",
      icon: <HomeIcon />,
      text: "Items",
    },
    {
      path: "/",
      icon: <HomeIcon />,
      text: "Stock",
    },
    {
      path: "/",
      icon: <HomeIcon />,
      text: "Build",
    },
  ]
  const TopSidebarItems = [
    {
      path: "/",
      icon: <HomeIcon />,
      text: "Home",
    },
    {
      path: "/",
      icon: <HomeIcon />,
      text: "Items",
    },
    {
      path: "/",
      icon: <HomeIcon />,
      text: "Stock",
    },
    {
      path: "/",
      icon: <HomeIcon />,
      text: "Build",
    },
    {
      path: "/",
      icon: <HomeIcon />,
      text: "Customers",
    },
    {
      path: "/",
      icon: <HomeIcon />,
      text: "Sales Orders",
    },
    {
      path: "/",
      icon: <HomeIcon />,
      text: "Suppliers",
    },
    {
      path: "/",
      icon: <HomeIcon />,
      text: "Manufacturers",
    },
    {
      path: "/",
      icon: <HomeIcon />,
      text: "Purchase Orders",
    },
    {
      path: "/",
      icon: <HomeIcon />,
      text: "Reports",
    },
  ]

  return (
    <div className="flex rounded-md border-3 border-gray-500 border-solid m-2">
      <div className="flex flex-col h-screen justify-between w-56 bg-slate-300">
        <div className="flex flex-col p-3">
          {TopSidebarItems.map((item) => {
            return (
              <Link className="flex items-center m-2" to={item.path}>
                <span>{item.icon}</span>
                <div className="ml-3 text-gray-600 tracking-wide">
                  {item.text}
                </div>
              </Link>
            )
          })}
        </div>
        <div className="flex flex-col mt-2 p-3">
          {LowerSidebarItems.map((item) => {
            return (
              <Link className="flex items-center m-2" to={item.path}>
                <span>{item.icon}</span>
                <div className="ml-3 text-gray-600 tracking-wide">
                  {item.text}
                </div>
              </Link>
            )
          })}
        </div>
      </div>
      <Outlet />
    </div>
  )
}
