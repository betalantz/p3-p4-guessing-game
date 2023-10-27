import { RouterProvider, createBrowserRouter } from "react-router-dom";
import { useAuth } from "../providers/authProvider";
import Authentication from "../components/Authentication";
import Dashboard from "../components/Dashboard";
import GameDetail from "../components/GameDetail";
import GameForm from "../components/GameForm";
import TokenVerify from "./TokenVerify";

const Routes = () => {
  const { token, isTokenExpired } = useAuth();

  const allRoutes = [
    {
      path: "dashboard",
      element: <Dashboard />,
    },
    {
      path: "games/:id",
      element: <GameDetail />,
    },
    {
      path: "games/new",
      element: <GameForm />,
    },
    {
      path: "login",
      element: <Authentication />,
    },
  ]

  const publicRoutes = [
    {
      path: "/",
      element: <TokenVerify />,
      children: [
        ...allRoutes,
      ],
    },
  ];
  
  const router = createBrowserRouter([...publicRoutes]);

  return <RouterProvider router={router} />;
};

export default Routes;
