import React from "react";
import { Grid, Typography, Box } from "@mui/material";
import bookingJson from "../../mocks/airport.json";
import { useSelector } from "react-redux";
import { data } from "../Landing/constants";
import dayjs from "dayjs";

function Booking() {
  const start = useSelector((state) => state.app.start);
  const destination = useSelector((state) => state.app.destination);
  console.log(start);
  return (
    <Grid
      sx={{
        width: "100vw",
        minHeight: "100vh",
        backgroundColor: "rgba(236,246,253,255)",
        p: "60px 20px 60px 20px",
      }}
    >
      <Grid sx={{ width: "100%" }}>
        <Grid
          sx={{
            width: "100%",
            p: 2,
            borderRadius: "20px",
            backgroundColor: "#000099",
            mt: 5,
            display: "flex",
            justifyContent: "center",
            color: "white ",
            gap: 2,
          }}
        >
          <Typography>{data[start] || "Pune"}</Typography>
          <Typography>-</Typography>
          <Typography>{data[destination] || "Mumbai"}</Typography>
        </Grid>
        <Grid mt={10} display="flex" flexDirection="column" gap={5}>
          {bookingJson.map((item, indexx) => (
            <Grid
              component="paper"
              sx={{
                padding: 3,
                borderRadius: "12px",

                backgroundColor: "white",
              }}
            >
              <Typography sx={{ mb: 2 }}>{item.flight_id}</Typography>
              <Box
                sx={{
                  display: "flex",
                  justifyContent: "space-between",
                  width: "100%",
                }}
              >
                <Box>
                  <Typography variant="body2">Departure</Typography>
                  <Typography sx={{ color: "#000099" }}>
                    {dayjs(item.departure_schedule).format("hh:mm A")}
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="body2">Duration</Typography>
                  <Typography sx={{ color: "#000099" }}>
                    {item.flight_duration}
                  </Typography>
                </Box>
                <Box>
                  <Box>
                    <Typography variant="body2">Arrival</Typography>
                    <Typography sx={{ color: "#000099" }}>
                      {dayjs(item.arrival_schedule).format("hh:mm A")}
                    </Typography>
                  </Box>
                </Box>
                <Box>
                  <Box>
                    <Typography variant="body2">Fare</Typography>
                    <Typography variant="h6" sx={{ color: "#000099" }}>
                      ₹{item.seats_available.economy}
                    </Typography>
                  </Box>
                </Box>
              </Box>
            </Grid>
          ))}
        </Grid>
      </Grid>
    </Grid>
  );
}

export default Booking;
