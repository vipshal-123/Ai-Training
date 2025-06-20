import isEmpty from "is-empty";
import axios from "./AxiosService";
import config from "../config/index.js";
import paramsEncoder from "../utils/paramsEncoder.js";

axios.defaults.baseURL = config.API_URL;
axios.defaults.paramsSerializer = paramsEncoder;
axios.defaults.headers.common["TIMEZONE"] =
  Intl.DateTimeFormat().resolvedOptions().timeZone;

export const handleResponse = (response, type) => {
  
  try {
    if (type === "success") {
      return response.data;
    } else if (type === "error") {
      if (isEmpty(response.response) || isEmpty(response.response.data)) {
        return { success: false, message: "Unknown error occurred" };
      }

      return response.response.data;
    }
  } catch (error) {
    console.log('error: ', error);
    return { success: false, message: "Unknown error occurred" };
  }
};

export default axios;