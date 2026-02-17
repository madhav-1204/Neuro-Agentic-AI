import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import { GoogleOAuthProvider } from '@react-oauth/google';
import { AuthProvider } from './contexts/AuthContext';
import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import DiagnosticHub from "./components/DiagnosticHub";
import AnalysisResult from "./pages/AnalysisResult";
import "./App.css";

const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID || "YOUR_GOOGLE_CLIENT_ID";

function HomePage() {
  const navigate = useNavigate();

  const handleNavigateToAnalysis = () => {
    navigate('/analysis');
  };

  return (
    <>
      <Hero />
      <DiagnosticHub onNavigate={handleNavigateToAnalysis} />
    </>
  );
}

function App() {
  return (
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      <AuthProvider>
        <Router>
          <div className="app">
            <Navbar />
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/analysis" element={<AnalysisResult />} />
            </Routes>
          </div>
        </Router>
      </AuthProvider>
    </GoogleOAuthProvider>
  );
}

export default App;