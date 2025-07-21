import { Layout } from 'antd';
import React, { useState } from 'react';

import Footer from './Footer';
import Header from './Header';
import Sidebar from './Sidebar';

const { Content } = Layout;

interface MainLayoutProps {
  children: React.ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const [collapsed, setCollapsed] = useState(false);
  const [mobile, setMobile] = useState(window.innerWidth <= 768);

  // Handle window resize
  React.useEffect(() => {
    const handleResize = () => {
      const isMobile = window.innerWidth <= 768;
      setMobile(isMobile);
      if (isMobile) {
        setCollapsed(true);
      }
    };

    window.addEventListener('resize', handleResize);
    handleResize(); // Initial check

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <Layout hasSider className="min-h-screen">
      <Sidebar collapsed={collapsed} mobile={mobile} onCollapse={setCollapsed} />
      <Layout
        className={`transition-all duration-300 ${collapsed && !mobile ? 'ml-[80px]' : 'ml-0 md:ml-[200px]'}`}
      >
        <Header mobile={mobile} onMenuToggle={() => setCollapsed(!collapsed)} />
        <Content
          className={`
            ${mobile ? 'm-3' : 'm-6'} 
            p-4 md:p-6 lg:p-8 
            min-h-[280px] 
            bg-white 
            rounded-lg 
            shadow-sm
          `}
        >
          {children}
        </Content>
        <Footer />
      </Layout>
    </Layout>
  );
};

export default MainLayout;
