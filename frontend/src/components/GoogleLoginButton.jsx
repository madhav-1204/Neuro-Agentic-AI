import { useState } from "react";
import { GoogleLogin } from "@react-oauth/google";
import { useAuth } from "../contexts/AuthContext";

const GoogleLoginButton = () => {
  const { login } = useAuth();
  const [error, setError] = useState(null);

  const handleSuccess = async (credentialResponse) => {
    setError(null);
    const result = await login(credentialResponse.credential);
    if (!result.success) {
      setError(result.error || "Login failed. Please try again.");
    }
  };

  const handleError = () => {
    setError("Google sign-in was cancelled or failed. Please try again.");
  };

  return (
    <div className="google-login-wrapper">
      <GoogleLogin
        onSuccess={handleSuccess}
        onError={handleError}
        useOneTap
        theme="filled_blue"
        size="large"
        text="signin_with"
        shape="rectangular"
      />
      {error && (
        <div className="auth-error-toast">
          <span>⚠️ {error}</span>
          <button onClick={() => setError(null)} className="auth-error-dismiss">✕</button>
        </div>
      )}
    </div>
  );
};

export default GoogleLoginButton;
