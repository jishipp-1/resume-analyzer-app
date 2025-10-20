import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "https://resume-analyzer-app-majh.onrender.com";

const client = axios.create({
  baseURL: API_BASE,
  headers: { "Content-Type": "application/json" },
});

export const register = (payload) => client.post("/register", payload);
export const login = (payload) => client.post("/login", payload);
export const analyze = (formData) =>
  axios.post(`${API_BASE}/analyze`, formData, { headers: { "Content-Type": "multipart/form-data" } });

export const compareJD = (formData) =>
  axios.post(`${API_BASE}/compare_resume_jd`, formData, { headers: { "Content-Type": "multipart/form-data" } });