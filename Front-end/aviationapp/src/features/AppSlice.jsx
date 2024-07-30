import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  userName: "",
  password: "",
  isLoggedIn: false,
  startDate: "",
  endDate: "",
  start: "",
  destination: "",
};

export const appSlice = createSlice({
  name: "app",
  initialState,
  reducers: {
    login: (state, action) => {
      state.userName = action.payload.userName;
      state.password = action.payload.password;
      state.isLoggedIn = action.payload.isLoggedIn;
    },
    pref: (state, action) => {
      (state.startDate = action.payload.startDate),
        (state.endDate = action.payload.endDate),
        (state.start = action.payload.start),
        (state.destination = action.payload.destination);
    },
  },
});

export const { login, pref } = appSlice.actions;
export default appSlice.reducer;
