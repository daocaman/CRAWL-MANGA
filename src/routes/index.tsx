import { Spin } from 'antd';
import { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import MainLayout from '../components/Layout/MainLayout';

// Lazy load pages
const Dashboard = lazy(() => import('../pages/Dashboard'));

// Loading component
const Loading = () => (
  <div className="flex justify-center items-center h-screen">
    <Spin size="large" />
  </div>
);

const AppRoutes = () => {
  return (
    <Router>
      <Suspense fallback={<Loading />}>
        <Routes>
          {/* Protected Routes */}
          <Route
            path="/dashboard"
            element={
              <MainLayout>
                <Dashboard />
              </MainLayout>
            }
          />

          {/* Redirect to dashboard by default */}
          <Route path="/" element={<Navigate to="/dashboard" replace />} />

          {/* 404 Not Found */}
          <Route path="*" element={<div>Not Found</div>} />
        </Routes>
      </Suspense>
    </Router>
  );
};

export default AppRoutes;
