import React, { useState } from "react";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import "./styles.css";

export default function App() {
  const [route, setRoute] = useState(localStorage.getItem("route") || "login");
  const setRouteAndStore = (r) => {
    localStorage.setItem("route", r);
    setRoute(r);
  };

  const isDashboard = route === "dashboard";

  return (
    <div id="fullpg" className={isDashboard ? "full-page" : "container"}>
      {!isDashboard && (
        <div className="card">
          {route === "login" && <Login onRouteChange={setRouteAndStore} />}
          {route === "register" && (
            <Register onRouteChange={setRouteAndStore} />
          )}
        </div>
      )}

      {isDashboard && <Dashboard onLogout={() => setRouteAndStore("login")} />}
    </div>
  );
}
