import {
  PieChart,
  Pie,
  Cell,
  Tooltip
} from "recharts";

export default function RiskChart({
  highRisk,
  lowRisk
}) {
  const data = [
    {
      name: "High Risk",
      value: highRisk
    },
    {
      name: "Low Risk",
      value: lowRisk
    }
  ];

  return (
    <PieChart
      width={400}
      height={300}
    >
      <Pie
        data={data}
        dataKey="value"
        outerRadius={100}
      >
        <Cell />
        <Cell />
      </Pie>

      <Tooltip />
    </PieChart>
  );
}