import React from 'react';

export default function ResultsTable({ data }: { data: any[] }) {
    if (!data || data.length === 0) return null;

    const columns = Object.keys(data[0]);

    return (
        <div className="mt-4 w-full overflow-x-auto rounded-xl border border-gray-700 shadow-sm">
            <table className="w-full text-sm text-left text-gray-300">
                <thead className="text-xs text-gray-400 uppercase bg-gray-800 font-semibold border-b border-gray-700">
                    <tr>
                        {columns.map((col) => (
                            <th key={col} className="px-6 py-3">{col}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {data.map((row, idx) => (
                        <tr key={idx} className="bg-gray-900 border-b border-gray-800 hover:bg-gray-800 transition-colors">
                            {columns.map((col) => (
                                <td key={col} className="px-6 py-4">{row[col]}</td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
