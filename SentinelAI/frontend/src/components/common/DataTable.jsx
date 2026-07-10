import Card from "./Card.jsx";

export default function DataTable({ title, columns, rows }) {
  return (
    <Card title={title}>
      <div className="overflow-x-auto">
        <table className="w-full min-w-[680px] text-left text-sm">
          <thead>
            <tr className="border-b border-slate-200 text-xs uppercase text-slate-500 dark:border-slate-800 dark:text-slate-400">
              {columns.map((column) => (
                <th key={column} className="px-3 py-3 font-semibold">
                  {column}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row[0]} className="border-b border-slate-100 last:border-0 dark:border-slate-800/70">
                {row.map((cell, index) => (
                  <td key={`${row[0]}-${cell}`} className="px-3 py-3 text-slate-700 dark:text-slate-300">
                    {index === 2 ? (
                      <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-700 dark:bg-slate-800 dark:text-slate-200">
                        {cell}
                      </span>
                    ) : (
                      cell
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}
