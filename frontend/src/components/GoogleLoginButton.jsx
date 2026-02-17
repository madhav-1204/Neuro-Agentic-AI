import { GoogleLogin } from "@react-oauth/google";
import { useAuth } from "../contexts/AuthContext";

const GoogleLoginButton = () => {
  const { login } = useAuth();

  const handleSuccess = async (credentialResponse) => {
    const result = await login(credentialResponse.credential);
    if (result.success) {
      console.log("Login successful!");
    } else {
      console.error("Login failed:", result.error);
    }
  };

  const handleError = () => {
    console.error("Google Login Failed");
  };

  return (
    <GoogleLogin
      onSuccess={handleSuccess}
      onError={handleError}
      useOneTap
      theme="filled_blue"
      size="large"
      text="signin_with"
      shape="rectangular"
    />
  );
};

export default GoogleLoginButton;
