import React, { useState } from "react";
import axios from "axios";
import "../styles/Contact.css";

const Contact = () => {
  const [formData, setFormData] = useState({ name: "", email: "", message: "" });
  const [status, setStatus] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus("Sending...");

    try {
      //Automatically switch between local and Render API URLs
      const API_URL =
        process.env.NODE_ENV === "production"
          ? "https://portfolio-project-pdp5.onrender.com/api/contact"
          : "http://127.0.0.1:5001/api/contact";

      const response = await axios.post(API_URL, formData, {
        headers: { "Content-Type": "application/json" },
      });

      setStatus(response.data.message || "Message sent successfully!");
      setFormData({ name: "", email: "", message: "" });
    } catch (error) {
      console.error("Error sending message:", error);
      setStatus("Failed to send message. Please try again.");
    }
  };

  return (
    <section id="contact" className="section contact-section">
      <div className="contact-content">
        <div className="contact-text">
          <h3>Seen Enough? Contact Me</h3>
          <p>
            You can reach me at my{" "}
            <a href="mailto:cuffsachin@gmail.com">email</a> or test out my contact form below.
          </p>
        </div>

        <div className="contact-form">
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              name="name"
              placeholder="Name"
              value={formData.name}
              onChange={handleChange}
              required
            />
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleChange}
              required
            />
            <textarea
              name="message"
              placeholder="Message"
              value={formData.message}
              onChange={handleChange}
              required
            />
            <button type="submit">Send</button>
          </form>
          <p className="form-status">{status}</p>
        </div>
      </div>
    </section>
  );
};

export default Contact;
