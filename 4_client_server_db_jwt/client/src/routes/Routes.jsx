import { RouterProvider, createBrowserRouter } from "react-router-dom";
import { useAuth } from "../providers/authProvider";
import { ProtectedRoute } from "./ProtectedRoute";
import { Navigate } from "react-router-dom";
import Authentication from "../components/Authentication";
import Dashboard from "../components/Dashboard";
import GameDetail from "../components/GameDetail";
import GameForm from "../components/GameForm";

const Routes = () => {
  const { token } = useAuth();

  const routesForAuthenticated = [
    {
      path: "/",
      element: <ProtectedRoute />,
      children: [
        {
          path: "/dashboard",
          element: <Dashboard />,
        },
        {
          path: "/games/:id",
          element: <GameDetail />,
        },
        {
          path: "/games/new",
          element: <GameForm />,
        },
      ],
    },
  ];

  const routesForUnauthenticated = [
    {
      path: "/",
      element: <Navigate to="/login" />,
    },
    {
      path: "/login",
      element: <Authentication />,
    },
  ];

  const router = createBrowserRouter([
    ...(!token ? routesForUnauthenticated : []),
    ...routesForAuthenticated,
  ]);

  return <RouterProvider router={router} />;
};

export default Routes;
