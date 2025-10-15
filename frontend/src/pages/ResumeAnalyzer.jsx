import React, { useState } from "react";
import { analyze } from "../api";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function ResumeAnalyzer(){
  const [file,setFile] = useState(null);
  const [loading,setLoading] = useState(false);
  const [result,setResult] = useState("");
  const [role,setRole] = useState("");

  const upload = async ()=>{
    if(!file){ alert("Select file"); return; }
    setLoading(true); setResult(""); setRole("");
    const fd = new FormData(); fd.append("file", file);
    try {
      const res = await analyze(fd);
      setRole(res.data.role_type);
      setResult(res.data.analysis);
    } catch(e){
      alert("Analysis failed");
    } finally { setLoading(false); }
  }

  return (
    <div>
      <p className="subtitle">Upload resume (PDF or DOCX) for AI analysis</p>
      <input className="file-input" type="file" accept=".pdf,.doc,.docx" onChange={e=>setFile(e.target.files[0])} />
      <button className="upload-btn" onClick={upload} disabled={loading}>{loading ? "Analyzing..." : "Upload & Analyze"}</button>

      {role && <div className="type-box"><strong>Detected:</strong> {role}</div>}

      {result && <div className="result-box markdown"><ReactMarkdown remarkPlugins={[remarkGfm]}>{result}</ReactMarkdown></div>}
    </div>
  )
}