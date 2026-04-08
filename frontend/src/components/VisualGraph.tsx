import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, LineChart, Line } from 'recharts';

export default function VisualGraph({ data }: { data: any[] }) {
    if (!data || data.length === 0) return null;

    // Determine if it's trending topics (topic & views), or date trends (date & views)
    const isDateTrend = data[0].hasOwnProperty('date');

    if (isDateTrend) {
        return (
            <div className="w-full h-64 mt-4 bg-gray-800 p-4 rounded-xl shadow-inner border border-gray-700">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                        <XAxis dataKey="date" stroke="#9CA3AF" />
                        <YAxis stroke="#9CA3AF" />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#1F2937', color: '#fff', border: 'none', borderRadius: '8px' }}
                            itemStyle={{ color: '#60A5FA' }}
                        />
                        <Line type="monotone" dataKey="views" stroke="#3B82F6" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 8 }} />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        );
    }

    // Fallback to Bar chart for categorical data (e.g., topic vs views)
    return (
        <div className="w-full h-64 mt-4 bg-gray-800 p-4 rounded-xl shadow-inner border border-gray-700">
            <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" horizontal={false} />
                    <XAxis type="number" stroke="#9CA3AF" />
                    <YAxis dataKey={data[0].topic ? "topic" : "id"} type="category" stroke="#9CA3AF" width={80} />
                    <Tooltip
                        contentStyle={{ backgroundColor: '#1F2937', color: '#fff', border: 'none', borderRadius: '8px' }}
                        cursor={{ fill: 'transparent' }}
                    />
                    <Bar dataKey="views" fill="#3B82F6" radius={[0, 4, 4, 0]} barSize={20} />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}
