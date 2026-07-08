import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

export default function MainLayout({
  children
}) {
  return (
    <div
      style={{
        display: "flex",
        background: "#f5f7fa",
        minHeight: "100vh"
      }}
    >
      <Sidebar />

      <div
        style={{
          flex: 1,
          padding: "20px"
        }}
      >
        <Navbar />

        {children}
      </div>
    </div>
  );
}