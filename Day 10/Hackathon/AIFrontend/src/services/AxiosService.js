import AxiosService from "axios";
import { getAuthToken } from "../utils/storage";

AxiosService.interceptors.request.use(
  (config) => {
    let local = getAuthToken({ isSession: false });
    let transientToken = local;
    if (transientToken && !config.url.endsWith("refresh-token")) {
      config.headers.Authorization = "Bearer "+transientToken;
    } else {
      config.headers.Authorization = "";
    }
    config.headers.TIMESTAMP = new Date().toISOString();
    config.headers.TIMEZONE = Intl.DateTimeFormat().resolvedOptions().timeZone;
    return config;
  },
  (error) => {
    throw error;
  }
);

export default AxiosService;