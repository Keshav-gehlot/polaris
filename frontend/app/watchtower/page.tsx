"use client";

import { useEffect, useMemo, useRef, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL || "";

type EventItem = {
  id?: string;
  title: string;
  description?: string | null;
  category?: string | null;
  source: string;
  source_url?: string | null;
  retrieved_at: string;
  time?: number | string | null;
  magnitude?: number | null;
  status?: string | null;
  location?: { longitude: number; latitude: number } | null;
};

type ApiResponse = {
  searched: boolean;
  events: EventItem[];
  sources: Array<{
    source: string;
    retrieved_at: string;
    status: string;
    data?: { url?: string; count?: number };
    note?: string | null;
  }>;
};

function project(longitude: number, latitude: number, width: number, height: number) {
  return { x: ((longitude + 180) / 360) * width, y: ((90 - latitude) / 180) * height };
}

function EventMap({ events }: { events: EventItem[] }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    const width = Math.max(320, rect.width);
    const height = Math.max(220, rect.height);
    canvas.width = width * dpr;
    canvas.height = height * dpr;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    ctx.scale(dpr, dpr);
    ctx.fillStyle = "#0E2233";
    ctx.fillRect(0, 0, width, height);
    ctx.strokeStyle = "rgba(221,231,229,.18)";
    ctx.lineWidth = 1;

    for (let lon = -180; lon <= 180; lon += 30) {
      const x = ((lon + 180) / 360) * width;
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, height); ctx.stroke();
    }
    for (let lat = -90; lat <= 90; lat += 30) {
      const y = ((90 - lat) / 180) * height;
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(width, y); ctx.stroke();
    }

    for (const event of events) {
      if (!event.location) continue;
      const point = project(event.location.longitude, event.location.latitude, width, height);
      ctx.beginPath();
      ctx.arc(point.x, point.y, 4, 0, Math.PI * 2);
      ctx.fillStyle = "#D9962B";
      ctx.fill();
      ctx.strokeStyle = "#DDE7E5";
      ctx.stroke();
    }
  }, [events]);

  return <div className="watch-map"><canvas ref={canvasRef} aria-label="World map showing Watchtower event locations" /><span className="map-note">Equirectangular view · point geometries only</span></div>;
}

export default function WatchtowerPage() {
  const [source, setSource] = useState<"all" | "usgs" | "eonet">("all");
  const [data, setData] = useState<ApiResponse | null>(null);
  const [state, setState] = useState("Loading live sources...");
  const [error, setError] = useState("");
  const [refresh, setRefresh] = useState(0);

  useEffect(() => {
    const controller = new AbortController();
    setState("Loading live sources...");
    setError("");
    fetch(`${API}/api/v1/watchtower/events?source=${source}&limit=100`, { signal: controller.signal })
      .then(async response => {
        const body = await response.json();
        if (!response.ok) throw new Error(body.detail || "Watchtower request failed");
        return body as ApiResponse;
      })
      .then(body => {
        setData(body);
        const failed = body.sources.filter(item => item.status === "error");
        setState(failed.length ? "Partial source failure" : "Live");
        if (failed.length) setError(failed.map(item => `${item.source}: ${item.note || "request failed"}`).join(" · "));
      })
      .catch(err => {
        if (err.name !== "AbortError") { setState("Unavailable"); setError(err.message || "Unable to reach the Polaris API"); }
      });
    return () => controller.abort();
  }, [source, refresh]);

  const events = data?.events || [];
  const pointEvents = useMemo(() => events.filter(item => item.location), [events]);

  return (
    <main className="shell">
      <div className="module-heading">
        <div>
          <span className="eyebrow">WATCHTOWER</span>
          <h1>Live Event Intelligence</h1>
          <p>USGS earthquakes and NASA EONET hazards, with source provenance and retrieval time.</p>
        </div>
        <button className="secondary-button" onClick={() => setRefresh(value => value + 1)}>Refresh</button>
      </div>

      <div className="toolbar">
        <label>Source
          <select value={source} onChange={event => setSource(event.target.value as typeof source)}>
            <option value="all">USGS + NASA EONET</option>
            <option value="usgs">USGS earthquakes</option>
            <option value="eonet">NASA EONET hazards</option>
          </select>
        </label>
        <span className="status live">{state}</span>
        <span className="muted">{events.length} events · {pointEvents.length} mapped points</span>
      </div>

      {error && <div className="error-banner">{error}</div>}
      {data && <EventMap events={pointEvents} />}

      <section className="source-strip">
        {(data?.sources || []).map(item => (
          <article className="source-card" key={item.source}>
            <strong>{item.source}</strong>
            <span className={item.status === "ok" ? "source-ok" : "source-error"}>{item.status}</span>
            <small>Retrieved {new Date(item.retrieved_at).toLocaleString()}</small>
            {item.data?.url && <a href={item.data.url} target="_blank" rel="noreferrer">Open source</a>}
            {item.note && <small>{item.note}</small>}
          </article>
        ))}
      </section>

      <section className="event-list">
        {events.map((event, index) => (
          <article className="event-card" key={event.id || `${event.source}-${index}`}>
            <div className="event-top">
              <span className="event-category">{event.category || "event"}</span>
              {typeof event.magnitude === "number" && <strong>M {event.magnitude.toFixed(1)}</strong>}
            </div>
            <h2>{event.title}</h2>
            {event.description && <p>{event.description}</p>}
            <div className="event-meta">
              <span>{event.source}</span>
              {event.time && <span>{new Date(event.time).toLocaleString()}</span>}
              <span>Retrieved {new Date(event.retrieved_at).toLocaleString()}</span>
            </div>
            {event.source_url && <a href={event.source_url} target="_blank" rel="noreferrer">View original record</a>}
          </article>
        ))}
        {data && events.length === 0 && <div className="empty-state">No events returned by the selected source. This is not the same as “not searched”.</div>}
      </section>
    </main>
  );
}
