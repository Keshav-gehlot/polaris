"use client";
import {useEffect,useState} from "react";
const API=process.env.NEXT_PUBLIC_API_URL;
export default function CataloguePage(){const[data,setData]=useState<any>(null);useEffect(()=>{fetch((API||"")+"/api/v1/catalogue/schema").then(r=>r.json()).then(setData)},[]);return <main className="shell"><span className="eyebrow">CATALOGUE</span><h1>Evidence Catalogue</h1><p>Every record keeps source and retrieval metadata.</p>{data&&<pre>{JSON.stringify(data,null,2)}</pre>}</main>}
