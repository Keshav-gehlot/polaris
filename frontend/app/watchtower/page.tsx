"use client";
import {useEffect,useState} from "react";
const API=process.env.NEXT_PUBLIC_API_URL;
export default function WatchtowerPage(){const[state,setState]=useState("Loading...");const[records,setRecords]=useState<any[]>([]);useEffect(()=>{fetch((API||"")+"/api/v1/watchtower/events").then(r=>r.json()).then(d=>{setRecords(d.records||[]);setState("Live")}).catch(()=>setState("Unavailable"))},[]);return <main className="shell"><span className="eyebrow">WATCHTOWER</span><h1>Live Events</h1><p>{state}</p><div className="module-grid">{records.map(r=><article className="module-card" key={r.source}><div className="module-top"><span>{r.source}</span><span className="status live">{r.status}</span></div><p>Retrieved: {r.retrieved_at}</p>{r.note&&<p>{r.note}</p>}</article>)}</div></main>}
