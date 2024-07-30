import { createBrowserRouter, Navigate } from "react-router-dom";
import { RootLayout } from "@/components";
import { Landing } from "@/modules/Landing";
import Layout from "./components/Layout";
import { Login } from "./modules/Authenticate";
import Booking from "./modules/Booking/Booking";

const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    children: [
      {
        index: true,
        element: <Navigate to="/landing" replace />,
      },
      {
        path: "/landing",
        element: (
          <Layout>
            <Landing />
          </Layout>
        ),
      },
      {
        path: "/login",
        element: (
          <Layout>
            <Login />
          </Layout>
        ),
      },
      {
        path: "/booking",
        element: (
          <Layout>
            <Booking />
          </Layout>
        ),
      },
    ],
  },
]);

export default router;
