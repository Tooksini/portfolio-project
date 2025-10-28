import React, { useState } from "react";
import Navbar from "./components/Navbar";
import About from "./components/About";
import Projects from "./components/Projects";
import Contact from "./components/Contact";
import Footer from "./components/Footer";

import "./styles/index.css";

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const toggleTheme = () => setIsDarkMode(prev => !prev);

  return (
    <div className={isDarkMode ? "App dark-mode" : "App light-mode"}>
      {/* Passing toggleTheme to Navbar to add a button */}
      <Navbar toggleTheme={toggleTheme} />
      <About />
      <Projects />
      <Contact />
      <Footer />
    </div>
  );
}

export default App;
