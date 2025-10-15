import React, { useState } from "react";
import axios from "axios";
import { register } from "../api";

export default function Register({ onRouteChange }){
  const [name,setName]=useState("");
  const [email,setEmail]=useState("");
  const [password,setPassword]=useState("");
  const [role,setRole]=useState("candidate");
  const [err,setErr]=useState("");

  const submit = async ()=>{
    setErr("");
    try {
      await register({ name, email, password, role });
      alert("Registered — please login");
      onRouteChange("login");
    } catch(e){
      setErr("Registration failed. Try different email.");
    }
  }

  return (
    <div>
      <div className="header"><div className="title">Resume AI — Register</div></div>
      <p className="subtitle">Create account</p>
      <input className="file-input" placeholder="Full name" value={name} onChange={e=>setName(e.target.value)} />
      <input className="file-input" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
      <input className="file-input" type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
      <select className="file-input" value={role} onChange={e=>setRole(e.target.value)}>
        <option value="candidate">Candidate</option>
        <option value="hr">HR</option>
      </select>
      <button className="upload-btn" onClick={submit}>Register</button>
      {err && <div className="error-msg">{err}</div>}
      <p style={{marginTop:12}}>Have account? <a href="#" onClick={()=>onRouteChange("login")}>Login</a></p>
    </div>
  )
}