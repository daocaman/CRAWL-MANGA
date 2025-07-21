import { Layout } from 'antd';
import React from 'react';

const { Footer: AntFooter } = Layout;

const Footer: React.FC = () => {
  return (
    <AntFooter
      className="text-center"
      style={{
        background: '#f0f2f5',
        padding: '16px',
      }}
    >
      © {new Date().getFullYear()} Your Company Name. All Rights Reserved.
    </AntFooter>
  );
};

export default Footer;
