import Link from "next/link";

const modules = [
  ["watchtower","Watchtower","live","Geographic and disaster-event intelligence."],
  ["netscan","NetScan","partial","RDAP, DNS and certificate intelligence."],
  ["crypto","Crypto","partial","Bitcoin/EVM investigation provider boundary."],
  ["catalogue","Catalogue","partial","Evidence and source records."],
  ["username","Username Research","partial","Provider-based username research."],
  ["camera","Camera","planned","Image and camera intelligence."],
  ["hawk","Hawk","planned","Advanced investigative intelligence."],
  ["skywave","Skywave","planned","Wireless/radio intelligence."],
  ["fisherman","Fisherman","planned","Collection and ingestion."],
  ["cases","Cases","live","Investigation case board foundation."]
];

export default function Home() {
  return <main className="shell"><header className="hero"><span className="eyebrow">POLARIS</span><h1>OSINT Workbench</h1><p>Source-backed intelligence research, investigation cases, and evidence-driven workflows.</p></header><section className="module-grid">{modules.map(([id,name,status,description])=><Link className="module-card" href={["camera","hawk","skywave","fisherman"].includes(id)?"/planned/"+id:"/"+id} key={id}><div className="module-top"><span>{name}</span><span className={"status "+status}>{status}</span></div><p>{description}</p></Link>)}</section></main>;
}
