export default function Sidebar() {
  return (
    <div
      style={{
        width: "250px",
        background: "#0B4F97",
        color: "white",
        minHeight: "100vh",
        padding: "20px"
      }}
    >
      <h2>Employee AI</h2>

      <hr />

      <p>
        <a
          href="/dashboard"
          style={{
            color: "white",
            textDecoration: "none"
          }}
        >
          Dashboard
        </a>
      </p>

      <p>
        <a
          href="/prediction"
          style={{
            color: "white",
            textDecoration: "none"
          }}
        >
          Prediction
        </a>
      </p>

      <p>
        <a
          href="/history"
          style={{
            color: "white",
            textDecoration: "none"
          }}
        >
          History
        </a>
      </p>

      <p>
        <a
          href="/model-training"
          style={{
            color: "white",
            textDecoration: "none"
          }}
        >
          Model Training
        </a>
      </p>

      <hr />

      <button
        onClick={() => {
          localStorage.removeItem("token");
          window.location.href = "/";
        }}
      >
        Logout
      </button>
    </div>
  );
}