import { DashboardOutlined, UserOutlined, SettingOutlined } from '@ant-design/icons';
import { Layout, Menu } from 'antd';
import React from 'react';
import { Link } from 'react-router-dom';

const { Sider } = Layout;

interface SidebarProps {
  collapsed: boolean;
  mobile: boolean;
  onCollapse: (collapsed: boolean) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ collapsed, onCollapse }) => {
  const menuItems = [
    {
      key: '1',
      icon: <DashboardOutlined />,
      label: <Link to="/dashboard">Dashboard</Link>,
    },
    {
      key: '2',
      icon: <UserOutlined />,
      label: <Link to="/profile">Profile</Link>,
    },
    {
      key: '3',
      icon: <SettingOutlined />,
      label: <Link to="/settings">Settings</Link>,
    },
  ];

  // Desktop Sidebar
  const desktopSidebar = (
    <Sider
      collapsible
      collapsed={collapsed}
      onCollapse={onCollapse}
      width={200}
      className="hidden md:block fixed left-0 top-0 bottom-0 z-50 overflow-auto h-screen !!bg-white"
      style={{
        width: collapsed ? '80px' : '200px',
        transition: 'width 0.2s ease',
      }}
    >
      <div className="logo p-4 text-center text-white">{collapsed ? 'Logo' : 'Dashboard'}</div>
      <Menu mode="inline" defaultSelectedKeys={['1']} items={menuItems} className="bg-gray-800" />
    </Sider>
  );

  return (
    <>
      {desktopSidebar}
      {/* {mobileSidebar} */}
    </>
  );
};

export default Sidebar;
