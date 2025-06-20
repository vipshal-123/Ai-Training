export const removeAuthToken = ({ isSession = false }) => {
  if (isSession) {
    return sessionStorage.removeItem("transient_token");
  } else {
    return localStorage.removeItem("transient_token");
  }
};

export const setAuthToken = (token, isSession = false) => {
  if (isSession) {
    sessionStorage.setItem("transient_token", token);
    return;
  }
  localStorage.setItem("transient_token", token);
};

export const getAuthToken = ({ isSession = false }) => {
  if (isSession) {
    return sessionStorage.getItem("transient_token");
  } else {
    return localStorage.getItem("transient_token");
  }
};

export const setupAuthTokens = (token, isRemember = true) => {
  if (isRemember) {
    localStorage.setItem("transient_token", token);
  } else {
    sessionStorage.setItem("transient_token", token);
  }
};