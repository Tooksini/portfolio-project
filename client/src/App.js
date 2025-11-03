import React, { useState, useEffect } from "react";
import Navbar from "./components/Navbar";
import About from "./components/About";
import Projects from "./components/Projects";
import Contact from "./components/Contact";
import Footer from "./components/Footer";
import "./index.css";

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Toggle dark mode globally
  const toggleTheme = () => setIsDarkMode(!isDarkMode);

  // Apply class to body
  useEffect(() => {
    if (isDarkMode) {
      document.body.classList.add("dark-mode");
    } else {
      document.body.classList.remove("dark-mode");
    }
  }, [isDarkMode]);

  return (
    <div className={`App ${isDarkMode ? "dark-mode" : "light-mode"}`}>
      <Navbar toggleTheme={toggleTheme} />
      <About />
      <Projects />
      <Contact />
      <Footer />
    </div>
  );
}

export default App;
