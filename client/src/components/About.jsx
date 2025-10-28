import React from 'react';
import profileImg from "../assets/IMG_9630 2.png";
import '../styles/About.css';

const About = () => {
    return (
        <section id="about" className="section about-section">
            <div className="about-content">
                <img src={profileImg} alt="Sachin Cuff" className="profile-img" />

                <div className="about-text">
                    <h2>Sachin Cuff</h2>
                    <p>
                        Hello, I am a software developer with traces of full-stack skills in React, Python, and MySQL.
                        My career goal is to build scalable, impactful, and user-friendly applications.
                    </p>

                    <h3>Technical Skills</h3>
                    <ul className="skills">
                        <li>JavaScript / React / jQuery</li>
                        <li>Python / Flask</li>
                        <li>Java / Spring / Spring Boot</li>
                        <li>HTML / CSS / Bootstrap</li>
                        <li>MySQL / Databases</li>
                    </ul>
                </div>
            </div>
        </section>
    );
};

export default About;
