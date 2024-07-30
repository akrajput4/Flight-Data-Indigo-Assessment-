import React from "react";
import { Box, AppBar, Toolbar, Stack, Button, Typography } from "@mui/material";
import { TravelIcon } from "@/assets/Icons";
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";

function Header() {
  const selector = useSelector((state) => state.app.isLoggedIn);
  const navigate = useNavigate();
  const navigateToLogin = () => {
    navigate("/login");
  };
  return (
    <>
      <Box display="flex">
        <AppBar
          position="fixed"
          sx={{
            zIndex: 1202,
            boxShadow: "none",
            color: "black",
            backgroundColor: "white",
          }}
        >
          <Toolbar
            sx={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <Box display="flex" gap={1} alignItems="center">
              <TravelIcon height="24px" fill="black" />
              <Typography variant="h6" sx={{ fontFamily: "cursive" }}>
                aviation
              </Typography>
            </Box>
            <Box>
              {!selector && (
                <Button
                  variant="text"
                  sx={{ color: "black", textTransform: "none" }}
                  onClick={navigateToLogin}
                >
                  Login
                </Button>
              )}
            </Box>
          </Toolbar>
        </AppBar>
      </Box>
    </>
  );
}

export default Header;
