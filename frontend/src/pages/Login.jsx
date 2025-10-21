import React, { useState } from "react";
import { login } from "../api";

export default function Login({ onRouteChange }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");

  const submit = async () => {
    setErr("");
    try {
      const res = await login({ email, password });
      const token = res.data.access_token;
      const role = res.data.role;
      localStorage.setItem("token", token);
      localStorage.setItem("role", role);
      onRouteChange("dashboard");
    } catch (e) {
      setErr("Invalid credentials or server error.");
    }
  };

  return (
    <div>
      <div className="header">
        <div className="title">Resume AI Analyzer — Login</div>
      </div>

      <p className="subtitle">Sign in as Candidate or HR</p>

      <input
        className="file-input"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        className="file-input"
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button className="upload-btn" onClick={submit}>
        Sign in
      </button>

      {err && <div className="error-msg">{err}</div>}

      <p style={{ marginTop: 12 }}>
        New?{" "}
        <a href="#" onClick={() => onRouteChange("register")}>
          Register here
        </a>
      </p>
    </div>
  );
}
