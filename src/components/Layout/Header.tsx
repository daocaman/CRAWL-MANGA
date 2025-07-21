import { UserOutlined, LogoutOutlined, SettingOutlined } from '@ant-design/icons';
import { Layout, Avatar, Dropdown, type MenuProps } from 'antd';
import React from 'react';
import { useNavigate } from 'react-router-dom';

const { Header: AntHeader } = Layout;

interface HeaderProps {
  mobile?: boolean;
  onMenuToggle?: () => void;
}

const Header: React.FC<HeaderProps> = () => {
  const navigate = useNavigate();

  const handleMenuClick: MenuProps['onClick'] = ({ key }) => {
    switch (key) {
      case 'logout':
        navigate('/login');
        break;
      case 'profile':
        navigate('/profile');
        break;
      case 'settings':
        navigate('/settings');
        break;
    }
  };

  const menuItems: MenuProps['items'] = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: 'Profile',
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: 'Settings',
    },
    { type: 'divider' },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: 'Logout',
      danger: true,
    },
  ];

  return (
    <AntHeader
      className="site-layout-background flex items-center justify-end px-4"
      style={{ padding: 0 }}
    >
      <Dropdown menu={{ items: menuItems, onClick: handleMenuClick }} placement="bottomRight">
        <Avatar icon={<UserOutlined />} className="cursor-pointer" size="large" />
      </Dropdown>
    </AntHeader>
  );
};

export default Header;
