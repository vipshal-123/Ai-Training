import axios, { handleResponse } from "./Axios";

export const login = async (data) => {
  try {
    const response = await axios({
      url: "/auth/user/google-signin",
      method: "POST",
      data,
    });

    return handleResponse(response, "success");
  } catch (error) {
    return handleResponse(error, "error");
  }
};

export const userData = async() => {
  try {
    const response = await axios({
      url: "/v1/user/user-info",
      method: "GET"
    });

    return handleResponse(response, "success");
  } catch (error) {
    return handleResponse(error, "error");
  }
}

export const uploadFile = async(formData) => {
  try {
    const response = await axios({
      url: "/v1/user/file-upload",
      method: "POST",
      data: formData
    });

    return handleResponse(response, "success");
  } catch (error) {
    return handleResponse(error, "error");
  }
}

export const details = async() => {
  try {
    const response = await axios({
      url: "/v1/user/details",
      method: "GET",
    });

    return handleResponse(response, "success");
  } catch (error) {
    return handleResponse(error, "error");
  }
}