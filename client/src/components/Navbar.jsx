import React, { useState } from "react";
import '../styles/Navbar.css';

const Navbar = ({ toggleTheme }) => {
  const [isMobile, setIsMobile] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(true);

  // Handle toggle internally
  const handleToggle = () => {
    setIsDarkMode(!isDarkMode);
    toggleTheme(); // call parent function if needed
  };

  return (
    <nav id="navbar" className="navbar">
      <h2 className="logo">Sachin's Portfolio</h2>

      {/* Navigation links */}
      <ul className={isMobile ? "nav-links-mobile" : "nav-links"}>
        <li><a href="#about" onClick={() => setIsMobile(false)}>About</a></li>
        <li><a href="#projects" onClick={() => setIsMobile(false)}>Projects</a></li>
        <li><a href="#contact" onClick={() => setIsMobile(false)}>Contact</a></li>
      </ul>

      {/* Navbar actions */}
      <div className="navbar-actions">
        {/* Theme toggle switch */}
        <label className="theme-switch">
          <input
            type="checkbox"
            checked={isDarkMode}
            onChange={handleToggle}
          />
          <span className="slider"></span>
        </label>

        {/* Mobile menu button */}
        <button
          className="mobile-menu-icon"
          onClick={() => setIsMobile(!isMobile)}
        >
          {isMobile ? "✖" : "☰"}
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
