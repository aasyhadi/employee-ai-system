import { useState } from "react";
import api from "../services/api";
import MainLayout from "../layouts/MainLayout";

export default function ModelTraining() {
  const [file, setFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");
  const [trainingMessage, setTrainingMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const uploadDataset = async (e) => {
    e.preventDefault();

    if (!file) {
      setUploadMessage("Pilih file CSV terlebih dahulu");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setUploadMessage("Uploading...");

      const response = await api.post(
        "/model/upload-dataset",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setUploadMessage(response.data.message);
    } catch (error) {
      console.error(error);
      setUploadMessage("Upload gagal");
    }
  };

  const retrainModel = async () => {
    try {
      setLoading(true);
      setTrainingMessage("Training model sedang berjalan...");

      const response = await api.post("/model/retrain");

      setTrainingMessage(response.data.message);
    } catch (error) {
      console.error(error);
      setTrainingMessage("Training gagal");
    } finally {
      setLoading(false);
    }
  };

  return (
    <MainLayout>
      <h1>Model Training</h1>

      <div
        style={{
          background: "#fff",
          padding: "20px",
          borderRadius: "12px",
          boxShadow: "0 2px 8px rgba(0,0,0,.1)",
          maxWidth: "600px",
        }}
      >
        <h2>Upload Dataset CSV</h2>

        <form onSubmit={uploadDataset}>
          <input
            type="file"
            accept=".csv"
            onChange={(e) => setFile(e.target.files[0])}
          />

          <br />
          <br />

          <button type="submit">
            Upload Dataset
          </button>
        </form>

        {uploadMessage && (
          <p>{uploadMessage}</p>
        )}

        <hr />

        <h2>Retrain Model</h2>

        <button
          onClick={retrainModel}
          disabled={loading}
        >
          {loading ? "Training..." : "Retrain Model"}
        </button>

        {trainingMessage && (
          <p>{trainingMessage}</p>
        )}
      </div>
    </MainLayout>
  );
}