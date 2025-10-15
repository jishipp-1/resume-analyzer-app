import React, { useState } from "react";
import ResumeAnalyzer from "./ResumeAnalyzer";
import JDOptimizer from "./JDOptimizer";

export default function Dashboard({ onLogout }) {
  const [tab, setTab] = useState("analyze");
  const role = localStorage.getItem("role") || "candidate";

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    onLogout();
  };

  return (
    <div>
      <div className="header">
        <div className="title">Dashboard — {role.toUpperCase()}</div>
        <div>
          <button className="tab-btn" onClick={logout}>
            Logout
          </button>
        </div>
      </div>

      <div id="innercontent">
        <div
          id="maincontent"
          style={{ display: "flex", gap: 8, marginBottom: 50 }}
        >
          <button
            className={`tab-btn ${tab === "analyze" ? "active" : ""}`}
            onClick={() => setTab("analyze")}
          >
            Resume Analyzer
          </button>
          <button
            className={`tab-btn ${tab === "jd" ? "active" : ""}`}
            onClick={() => setTab("jd")}
          >
            Resume vs JD
          </button>
        </div>

        {tab === "analyze" && <ResumeAnalyzer />}
        {tab === "jd" && <JDOptimizer />}
      </div>
    </div>
  );
}
