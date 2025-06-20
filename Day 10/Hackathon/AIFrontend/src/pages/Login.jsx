import { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";
import config from "../config";
import isEmpty from "is-empty";
import { setAuthToken } from "../utils/storage";
import { useDispatch } from "react-redux";
import { fetchUserData, setupAuth } from "../redux/slice/authSlice";
import { login } from "../services/auth.service";

function Login() {
  const navigate = useNavigate();
  const [responseToken, setResponseToken] = useState(null);
  const dispatch = useDispatch();

  const handleLogin = useCallback(async () => {
    try {
      const { success, message, token, userId } = await login({
        id_token: responseToken,
      });
      if (success) {
        setAuthToken(token?.refreshToken || "", false);
        dispatch(setupAuth({ isAuth: true, _id: userId }));
        dispatch(fetchUserData());
        navigate("/home");
      } else {
        console.log("Error", message);
      }
    } catch (error) {
      console.error("error: ", error);
    }
  }, [dispatch, navigate, responseToken]);

  useEffect(() => {
    if (!isEmpty(responseToken)) {
      handleLogin();
    }
  }, [responseToken, handleLogin]);

  return (
    <GoogleOAuthProvider clientId={config.GOOGLE_OAUTH_ID}>
      <div className="relative flex h-full w-full">
        <div className="h-screen w-1/2 bg-black">
          <div className="mx-auto flex h-full w-2/3 flex-col justify-center text-white xl:w-1/2">
            <div>
              <p className="text-2xl">App|</p>
              <p>please login to continue|</p>
            </div>
            <div className="my-6">
              <GoogleLogin
                onSuccess={(token) => setResponseToken(token.credential)}
                onError={() => console.log("Login failed")}
              />
            </div>
            <div>
              <fieldset className="border-t border-solid border-gray-600">
                <legend className="mx-auto px-2 text-center text-sm">
                  login via our secure system
                </legend>
              </fieldset>
            </div>
          </div>
        </div>
        <div className="h-screen w-1/2 bg-blue-600">
          <img
            src="https://images.pexels.com/photos/2523959/pexels-photo-2523959.jpeg"
            className="h-full w-full"
          />
        </div>
      </div>
    </GoogleOAuthProvider>
  );
}

export default Login;
