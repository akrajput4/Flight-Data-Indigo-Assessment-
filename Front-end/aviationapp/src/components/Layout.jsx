import React from "react";
import { Box } from "@mui/material";

function Layout({ children }) {
  return (
    <Box
      sx={{
        flexGrow: 1,

        mb: 4,
        width: "100%",
      }}
    >
      {children}
    </Box>
  );
}

export default Layout;
