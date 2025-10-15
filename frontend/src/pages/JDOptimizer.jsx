import React, { useState } from "react";
import { compareJD } from "../api";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function JDOptimizer(){
  const [resumeFile,setResumeFile] = useState(null);
  const [jdText,setJdText] = useState("");
  const [loading,setLoading] = useState(false);
  const [result,setResult] = useState("");

  const submit = async ()=>{
    if(!resumeFile){ alert("Upload resume"); return; }
    if(!jdText.trim()){ alert("Paste JD"); return; }
    setLoading(true); setResult("");
    const fd = new FormData();
    fd.append("resume", resumeFile);
    fd.append("jd_text", jdText);
    try {
      const res = await compareJD(fd);
      setResult(res.data.comparison_result);
    } catch(e){
      alert("Comparison failed");
    } finally { setLoading(false); }
  }

  return (
    <div>
      <p className="subtitle">Upload resume + paste JD (text) to check match</p>
      <input className="file-input" type="file" accept=".pdf,.doc,.docx" onChange={e=>setResumeFile(e.target.files[0])} />
      <textarea className="jd-textarea" placeholder="Paste job description here..." value={jdText} onChange={e=>setJdText(e.target.value)} />
      <button className="upload-btn" onClick={submit} disabled={loading}>{loading? "Comparing..." : "Compare Resume with JD"}</button>

      {loading && <div className="spinner" />}

      {result && <div className="result-box markdown"><ReactMarkdown remarkPlugins={[remarkGfm]}>{result}</ReactMarkdown></div>}
    </div>
  )
}