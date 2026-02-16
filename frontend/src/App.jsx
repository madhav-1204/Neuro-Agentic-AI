import { useState } from "react";
import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import DiagnosticHub from "./components/DiagnosticHub";
import "./App.css";

function App() {
  return (
    <div className="app">
      <Navbar />
      <Hero />
      <DiagnosticHub onResult={setResult} result={result} />
    </div>
  );
}

export default App;