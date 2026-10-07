export default function Home() {
  return (
    <main style={{ minHeight: "100vh", padding: "48px", maxWidth: 1200, margin: "0 auto" }}>
      <section>
        <p style={{ opacity: 0.65, marginBottom: 8 }}>POLARIS</p>
        <h1 style={{ fontSize: "clamp(2.5rem, 7vw, 5rem)", margin: 0 }}>
          OSINT Workbench
        </h1>
        <p style={{ maxWidth: 680, fontSize: 18, lineHeight: 1.6, opacity: 0.75 }}>
          Source-backed intelligence research, investigation cases, and evidence-driven
          workflows in one workspace.
        </p>
      </section>

      <section style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 16, marginTop: 48 }}>
        {["Watchtower", "NetScan", "Crypto", "Catalogue", "Username Research", "Cases"].map((sector) => (
          <article
            key={sector}
            style={{
              border: "1px solid #202838",
              borderRadius: 16,
              padding: 24,
              background: "#0e131d",
            }}
          >
            <h2 style={{ marginTop: 0 }}>{sector}</h2>
            <p style={{ opacity: 0.6 }}>Module foundation</p>
          </article>
        ))}
      </section>
    </main>
  );
}