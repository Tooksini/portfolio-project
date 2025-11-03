import React from "react";
import '../styles/Navbar.css';

const Navbar = ({ toggleTheme }) => {
  const [isMobile, setIsMobile] = React.useState(false);

  return (
    <nav id="navbar" className="navbar">
      <h2 className="logo">Sachin's Portfolio</h2>

      <ul className={isMobile ? "nav-links-mobile" : "nav-links"}>
        <li><a href="#about" onClick={() => setIsMobile(false)}>About</a></li>
        <li><a href="#projects" onClick={() => setIsMobile(false)}>Projects</a></li>
        <li><a href="#contact" onClick={() => setIsMobile(false)}>Contact</a></li>
      </ul>

      <div className="navbar-actions">
        <label className="theme-switch">
          <input
            type="checkbox"
            onChange={toggleTheme}
          />
          <span className="slider"></span>
        </label>

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
