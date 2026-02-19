import { useState } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import { GoogleOAuthProvider } from '@react-oauth/google';
import { AuthProvider } from './contexts/AuthContext';
import ErrorBoundary from './components/ErrorBoundary';
import SplashScreen from "./components/SplashScreen";
import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import DiagnosticHub from "./components/DiagnosticHub";
import AnalysisResult from "./pages/AnalysisResult";
import DiagnosticCenter from "./pages/DiagnosticCenter";
import Technology from "./pages/Technology";
import "./App.css";

const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID || "YOUR_GOOGLE_CLIENT_ID";

function HomePage() {
  const navigate = useNavigate();

  const handleNavigateToAnalysis = () => {
    navigate('/analysis');
  };

  const handleNavigateToDC = () => {
    navigate('/diagnostic-center');
  };

  return (
    <>
      <Hero />
      <DiagnosticHub onNavigate={handleNavigateToAnalysis} onNavigateDC={handleNavigateToDC} />
    </>
  );
}

function App() {
  const [showSplash, setShowSplash] = useState(true);

  if (showSplash) {
    return <SplashScreen onFinish={() => setShowSplash(false)} />;
  }

  return (
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      <AuthProvider>
        <ErrorBoundary>
          <Router>
            <div className="app">
              <Navbar />
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/analysis" element={<AnalysisResult />} />
                <Route path="/diagnostic-center" element={<DiagnosticCenter />} />
                <Route path="/technology" element={<Technology />} />
              </Routes>
            </div>
          </Router>
        </ErrorBoundary>
      </AuthProvider>
    </GoogleOAuthProvider>
  );
}

export default App;