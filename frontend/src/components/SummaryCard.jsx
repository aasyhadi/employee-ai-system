export default function SummaryCard({
  title,
  value
}) {
  return (
    <div
      style={{
        background: "#fff",
        borderRadius: "12px",
        padding: "20px",
        boxShadow:
          "0 2px 10px rgba(0,0,0,.08)",
        minHeight: "120px"
      }}
    >
      <p
        style={{
          color: "#666",
          fontSize: "14px"
        }}
      >
        {title}
      </p>

      <h1
        style={{
          marginTop: "10px",
          color: "#0B4F97"
        }}
      >
        {value}
      </h1>
    </div>
  );
}