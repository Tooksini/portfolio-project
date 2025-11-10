import React, { useState } from "react";
import "../styles/Navbar.css";

const Navbar = ({ toggleTheme }) => {
  const [menuOpen, setMenuOpen] = useState(false);

  const handleMenuToggle = () => {
    setMenuOpen(!menuOpen);
  };

  const handleLinkClick = () => {
    setMenuOpen(false);
  };

  return (
    <nav id="navbar" className="navbar">
      <h2 className="logo">Sachin's Portfolio</h2>

      {/* Desktop Navigation */}
      <ul className="nav-links">
        <li><a href="#about">About</a></li>
        <li><a href="#projects">Projects</a></li>
        <li><a href="#contact">Contact</a></li>
      </ul>

      <div className="navbar-actions">
        <label className="theme-switch">
          <input type="checkbox" onChange={toggleTheme} />
          <span className="slider"></span>
        </label>

        <button className="mobile-menu-icon" onClick={handleMenuToggle}>
          {menuOpen ? "✕" : "☰"}
        </button>
      </div>

      <div className={`side-panel ${menuOpen ? "open" : ""}`}>
        <a href="#about" onClick={handleLinkClick}>About</a>
        <a href="#projects" onClick={handleLinkClick}>Projects</a>
        <a href="#contact" onClick={handleLinkClick}>Contact</a>

        <button className="close-menu-icon" onClick={handleMenuToggle}>
          ✕
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
