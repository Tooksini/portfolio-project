import React, { useEffect, useState } from "react";
import axios from "axios";
import '../styles/Projects.css';

const Projects = () => {
    const [projects, setProjects] = useState([]);
    const [loading, setLoading] = useState(true);
    const [errorMsg, setErrorMsg] = useState("");

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/projects")
            .then((res) => {
                setProjects(res.data.projects);
                setLoading(false);
            })
            .catch((err) => {
                setErrorMsg("Failed to fetch projects");
                setLoading(false);
            });
    }, []);

    if (loading) return <p className="loading">Loading projects...</p>;
    if (errorMsg) return <p className="error">{errorMsg}</p>;

    return (
        <section id="projects" className="section projects-section">
            {/* Section heading */}
            <h2>My Projects</h2>

            {/* Grid container for project cards */}
            <div className="projects-grid">
                {projects.map((project) => {
                    // Convert tech_stack to array if it's a string (from database JSON)
                    const techArray = Array.isArray(project.tech_stack)
                        ? project.tech_stack 
                        : JSON.parse(project.tech_stack);

                    return (
                        <div key={project.id} className="project-card">
                            {/* Optional background shape for visual flair */}
                            <div className="project-bg"></div>

                            {/* Main content of each project card */}
                            <div className="project-content">
                                {/* Project title */}
                                <h3>{project.title}</h3>

                                {/* Project description */}
                                <p>{project.description}</p>

                                {/* Tech stack badges */}
                                <div className="tech-stack">
                                    {techArray.map((tech, i) => (
                                        <span key={i} className="tech-badge">{tech}</span>
                                    ))}
                                </div>

                                {/* Link to GitHub */}
                                <a
                                    href={project.github_link}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="project-link"
                                >
                                    View Project
                                </a>
                            </div>
                        </div>
                    );
                })}
            </div>
        </section>
    );
};

export default Projects;
