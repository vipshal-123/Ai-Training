import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { userData } from "../../services/auth.service"

export const fetchUserData = createAsyncThunk(
  "auth/fetchUserData",
  async () => {
    try {
      const response = await userData();
      if (response.success) {
        return { isAuth: true, ...response.data };
      } else {
        return { isAuth: false, id: "", type: "" };
      }
    } catch (error) {
        console.log('error: ', error);
      return { isAuth: false, id: "", type: "" };
    }
  }
);

const initialState = {
  isAuth: false,
  _id: "",
  email: "",
  name: ""
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setupAuth: (state, { payload }) => {
      state.isAuth = payload.isAuth;
      state._id = payload._id;
      state.email = payload.email;
      state.name = payload.name;
    },
    revokeAuth: (state) => {
      state.isAuth = false;
      state._id = "";
      state.email = "";
      state.name = "";
    },
  },
  extraReducers: (builder) => {
    builder.addCase(fetchUserData.fulfilled, (state, action) => {
      state.isAuth = !!action?.payload?.isAuth;
      state._id = action?.payload?._id;
      state.email = action?.payload?.email;
      state.name = action?.payload?.name;
    });
  },
});

export const { setupAuth, revokeAuth } = authSlice.actions;
export default authSlice.reducer;
