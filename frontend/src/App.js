import { createBrowserRouter, RouterProvider } from "react-router-dom"
import "./App.css"

import { HomePage } from "./pages/HomePage"
import { CreateAccount } from "./pages/CreateAccount"
import { Login } from "./pages/Login"
import { Dashboard } from "./pages/Dashboard"
import { Sidebar } from "./pages/Sidebar"

const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
    children: [
      {
        path: "register",
        element: <CreateAccount />,
      },
      {
        path: "login",
        element: <Login />,
      },
      {
        path: "dashboard",
        element: <Sidebar />,
        children: [
          {
            index: true,
            element: <Dashboard />,
          },
        ],
      },
    ],
  },
])

function App() {
  return <RouterProvider router={router}></RouterProvider>
}

export default App
