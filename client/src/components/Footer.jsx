import React, { useState, useEffect } from "react";
import "../styles/Footer.css";

const Footer = () => {
  const [showButton, setShowButton] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      // Only toggle when threshold is crossed
      if (window.scrollY > 400) setShowButton(true);
      else setShowButton(false);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <footer id="footer" className="footer-section">
      <p>Sachin Cuff © 2025</p>

      <div className="social-links-footer">
        <a href="https://github.com/Tooksini" target="_blank" rel="noopener noreferrer">
          GitHub
        </a>
        <a href="https://linkedin.com/in/sachincuff/" target="_blank" rel="noopener noreferrer">
          LinkedIn
        </a>
        <a href="mailto:cuffsachin@gmail.com">Email</a>
      </div>

      <button
        onClick={scrollToTop}
        className={`back-to-top ${showButton ? "show" : ""}`}
      >
        ↑ Back To Top
      </button>
    </footer>
  );
};

export default Footer;
