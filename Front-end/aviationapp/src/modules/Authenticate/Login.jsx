import React from "react";
import { Field, FormikProvider, useFormik } from "formik";
import {
  Autocomplete,
  Box,
  Button,
  Checkbox,
  CircularProgress,
  FormControlLabel,
  Grid,
  IconButton,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import "./Login.scss";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { login } from "../../features/AppSlice";

function Login() {
  const navigate = useNavigate("/landing");
  const dispatch = useDispatch();
  const initialValues = {
    userName: "",
    password: "",
  };

  const formik = useFormik({
    initialValues: initialValues,
    onSubmit: (values) => {
      dispatch(login({ ...values, isLoggedIn: true }));
      navigate("/landing");
    },
  });

  return (
    <Grid className="loginContainer">
      <Grid
        sx={{
          backgroundColor: "#0000006e",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-evenly",
          gap: 2,
          height: "25rem",
          width: "25rem",
          padding: 5,
          borderRadius: "12px",
        }}
      >
        <Typography variant="h4" textAlign="center">
          Login
        </Typography>
        <FormikProvider value={formik}>
          <form
            onSubmit={formik.handleSubmit}
            style={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-evenly",
              gap: 2,
              height: "15rem",
            }}
          >
            <Field name="userName">
              {({ field, meta }) => (
                <>
                  <TextField
                    {...field}
                    type="text"
                    label="User Name"
                    variant="outlined"
                    required
                    sx={{
                      "& .MuiOutlinedInput-input": {
                        backgroundColor: "rgba(252, 252, 252, 0.42)",
                      },
                    }}
                  />
                </>
              )}
            </Field>
            <Field name="password">
              {({ field, meta }) => (
                <>
                  <TextField
                    {...field}
                    type="text"
                    label="Password"
                    variant="outlined"
                    required
                    sx={{ backgroundColor: "rgba(252, 252, 252, 0.42)" }}
                  />
                </>
              )}
            </Field>
            <Button variant="contained" type="submit">
              Login
            </Button>
          </form>
        </FormikProvider>
      </Grid>
    </Grid>
  );
}

export default Login;
