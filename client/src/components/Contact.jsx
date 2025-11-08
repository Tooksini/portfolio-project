import React, { useState } from "react";
import "../styles/Contact.css";

const Contact = () => {
  const [formData, setFormData] = useState({ name: "", email: "", message: "" });
  const [alert, setAlert] = useState({ type: "", message: "" });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await res.json();

      if (data.status === "success") {
        setAlert({ type: "success", message: "Message sent successfully ✅" });
        setFormData({ name: "", email: "", message: "" });
      } else {
        setAlert({ type: "error", message: "Failed to send message ❌" });
      }
    } catch (error) {
      setAlert({ type: "error", message: "Network error. Try again!" });
    }

    setTimeout(() => setAlert({ type: "", message: "" }), 4000);
  };

  return (
    <section id="contact" className="contact-section">
      <div className="contact-card">
        <h2>Contact Me</h2>

        <form onSubmit={handleSubmit} className="contact-form">
          <div className="input-box">
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
            />
            <label>Name</label>
          </div>

          <div className="input-box">
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
            <label>Email</label>
          </div>

          <div className="input-box">
            <textarea
              name="message"
              rows="4"
              value={formData.message}
              onChange={handleChange}
              required
            />
            <label>Message</label>
          </div>

          <button type="submit">Send Message</button>
        </form>

        {alert.message && (
          <div className={`alert ${alert.type}`}>
            {alert.message}
          </div>
        )}
      </div>
    </section>
  );
};

export default Contact;
