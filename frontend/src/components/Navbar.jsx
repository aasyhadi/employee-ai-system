export default function Navbar() {
  return (
    <div
      style={{
        background: "#fff",
        borderRadius: "12px",
        padding: "15px 25px",
        display: "flex",
        justifyContent:
          "space-between",
        alignItems: "center",
        boxShadow:
          "0 2px 10px rgba(0,0,0,.08)"
      }}
    >
      <h2>Employee AI System</h2>

      <button
        onClick={() => {
          localStorage.clear();
          window.location.href = "/";
        }}
      >
        Logout
      </button>
    </div>
  );
}