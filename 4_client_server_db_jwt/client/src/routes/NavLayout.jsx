import { Route, Outlet } from "react-router-dom";
import NavMenu from "../components/NavMenu";

export const NavLayout = () => {
  return (
    <Route
      element={
        <>
          <NavMenu />
          <Outlet />
        </>
      }
    />
  );
};
