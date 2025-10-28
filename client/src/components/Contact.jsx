import React, { useState } from "react";
import axios from "axios";
import "../styles/Contact.css";

export default function Contact() {
  const [formData, setFormData] = useState({ name: "", email: "", message: "" });
  const [status, setStatus] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus("Sending...");

    try {
      const response = await axios.post("http://127.0.0.1:5000/api/contact", formData, {
        headers: { "Content-Type": "application/json" },
      });
      setStatus(response.data.message);
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
            You can reach me at{" "}
            <a href="mailto:cuffsachin@gmail.com">cuffsachin@gmail.com</a> or use the form below.
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
}
