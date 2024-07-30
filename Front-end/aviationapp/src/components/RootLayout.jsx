import { Box, Stack } from "@mui/material";
import "./Layout.scss";
import { Outlet } from "react-router-dom";
import Header from "./Header";

const RootLayout = () => {
  return (
    <Box sx={{ width: "100%" }}>
      <Stack direction="row" justifyContent="start">
        <Header />
        <Box component="main" className="layoutContainer">
          <Outlet />
        </Box>
      </Stack>
    </Box>
  );
};

export default RootLayout;
