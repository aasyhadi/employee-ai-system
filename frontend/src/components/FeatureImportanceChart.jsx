import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

export default function FeatureImportanceChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />

        <XAxis dataKey="feature" />

        <YAxis />

        <Tooltip />

        <Bar dataKey="importance" />
      </BarChart>
    </ResponsiveContainer>
  );
}