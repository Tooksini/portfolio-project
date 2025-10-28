import React from "react";
import '../styles/Footer.css';

const Footer = () =>{
    const scrollToTop = () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    };
    
    return(
        <footer id ="footer" className="footer-section">
            <p> Sachin Cuff @2025</p>

            <div className="social-links-footer">
                <a href="https://github.com/Tooksini" target="_blank" rel="noopener noreferrer">GitHub </a>
                <a href="https://linkedin.com/in/sachincuff/" target="_blank" rel="noopener noreferrer">LinkedIn </a>
                <a href="mailto:cuffsachin@gmail.com">email </a>
            </div>

            <button onClick={scrollToTop}>Back To Top</button>
        </footer>
    );
};

export default Footer;