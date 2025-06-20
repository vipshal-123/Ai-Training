import React, { useEffect } from "react";
import { useDispatch } from "react-redux";
import { fetchUserData } from "../redux/slice/authSlice";

const UserProvider = ({ children }) => {
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(fetchUserData());
  }, [dispatch]);

  return <>{children}</>;
};

export default UserProvider;
