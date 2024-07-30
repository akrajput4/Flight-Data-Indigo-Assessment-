import React from "react";
import {
  Container,
  Typography,
  Grid,
  Button,
  TextField,
  Autocomplete,
} from "@mui/material";
import { useFormik } from "formik";
import * as Yup from "yup";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import { LocalizationProvider } from "@mui/x-date-pickers";
import { airport } from "./constants";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { pref } from "../../features/AppSlice";

function Landing() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const formik = useFormik({
    initialValues: {
      start: "",
      destination: "",
      startDate: new Date(),
      endDate: new Date(),
    },

    onSubmit: (values) => {
      const { startDate, endDate, start, destination } = values;
      dispatch(pref({ startDate, endDate, start, destination }));
      navigate("/booking");
    },
  });

  return (
    <Container sx={{ paddingTop: 20 }}>
      <Typography
        variant="h4"
        sx={{ fontFamily: "fantasy", color: "#000099" }}
        gutterBottom
      >
        Hi there, where would you like to go today?
      </Typography>
      <Grid
        component="form"
        onSubmit={formik.handleSubmit}
        spacing={2}
        sx={{
          display: "flex",
          padding: "3.5rem 3rem 3.5rem 3rem",
          borderRadius: "12px",
          backgroundColor: "#ffffffde",
          justifyContent: "center",
          alignItems: "center",
          gap: 2,
          boxShadow: "rgba(149, 157, 165, 0.2) 0px 8px 24px",
        }}
      >
        <Autocomplete
          name="start"
          label="Start"
          options={airport}
          sx={{ width: "15rem" }}
          renderInput={(params) => <TextField {...params} label="Departure" />}
          onChange={(e) => formik.setFieldValue("start", e.target.value)}
        />
        <Autocomplete
          name="destination"
          options={airport}
          renderInput={(params) => <TextField {...params} label="Arrival" />}
          onChange={(e) => formik.setFieldValue("destination", e.target.value)}
          label="Destination"
          sx={{ width: "15rem" }}
        />
        <LocalizationProvider dateAdapter={AdapterDateFns}>
          <DatePicker
            label="Start Date"
            disablePast
            value={formik.values.startDate}
            onChange={(value) => formik.setFieldValue("startDate", value)}
            renderInput={(params) => <TextField name="startDate" />}
            sx={{
              "& .MuiOutlinedInput-root": {
                width: "10rem",
              },
            }}
          />

          <DatePicker
            label="End Date"
            disablePast
            value={formik.values.endDate}
            onChange={(value) => formik.setFieldValue("endDate", value)}
            renderInput={(params) => <TextField name="endDate" />}
            sx={{
              "& .MuiOutlinedInput-root": {
                width: "10rem",
              },
            }}
          />

          <Button
            type="submit"
            variant="outlined"
            sx={{ textTransform: "none", width: "10rem", height: "3rem" }}
          >
            Search
          </Button>
        </LocalizationProvider>
      </Grid>
    </Container>
  );
}

export default Landing;
