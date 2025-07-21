import './App.css';
import { ConfigProvider } from 'antd';

import DashboardLayout from './components/DashboardLayout';

function App() {
  return (
    <ConfigProvider>
      <DashboardLayout>
        <div className="p-4">
          <h1 className="text-2xl font-bold mb-4">Welcome to Dashboard</h1>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white p-4 rounded-lg shadow">
              <h2 className="text-lg font-semibold">Overview</h2>
              <p>Dashboard content goes here</p>
            </div>
            <div className="bg-white p-4 rounded-lg shadow">
              <h2 className="text-lg font-semibold">Statistics</h2>
              <p>Some statistics or charts</p>
            </div>
            <div className="bg-white p-4 rounded-lg shadow">
              <h2 className="text-lg font-semibold">Quick Actions</h2>
              <p>Quick action buttons</p>
            </div>
          </div>
        </div>
      </DashboardLayout>
    </ConfigProvider>
  );
}

export default App;
