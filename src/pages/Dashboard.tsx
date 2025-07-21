import { UserOutlined, ShoppingCartOutlined, DollarOutlined } from '@ant-design/icons';
import { Card, Row, Col, Statistic, Space } from 'antd';
import React from 'react';

const Dashboard: React.FC = () => {
  return (
    <div className="min-h-[80%]">
      <h1 className="text-2xl font-bold mb-4 ]">Dashboard Overview</h1>
      <Row
        gutter={[
          { xs: 8, sm: 16, md: 24 },
          { xs: 8, sm: 16, md: 24 },
        ]}
      >
        <Col xs={24} sm={12} md={8}>
          <Card
            hoverable
            className="w-full"
            cover={
              <div className="p-4 text-center bg-blue-50">
                <UserOutlined className="text-4xl text-blue-500 mb-2" />
              </div>
            }
          >
            <Statistic title="Total Users" value={1128} valueStyle={{ color: '#1890ff' }} />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={8}>
          <Card
            hoverable
            className="w-full"
            cover={
              <div className="p-4 text-center bg-green-50">
                <ShoppingCartOutlined className="text-4xl text-green-500 mb-2" />
              </div>
            }
          >
            <Statistic title="Total Orders" value={256} valueStyle={{ color: '#52c41a' }} />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={8}>
          <Card
            hoverable
            className="w-full"
            cover={
              <div className="p-4 text-center bg-gold-50">
                <DollarOutlined className="text-4xl text-gold-500 mb-2" />
              </div>
            }
          >
            <Statistic
              title="Revenue"
              value={89450}
              precision={2}
              valueStyle={{ color: '#faad14' }}
              prefix="$"
            />
          </Card>
        </Col>
      </Row>

      {/* Quick Actions Section */}
      <div className="mt-6">
        <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
        <Space direction="horizontal" size="middle" className="w-full">
          <Card
            hoverable
            className="w-full md:w-auto"
            styles={{
              body: {
                padding: '12px 20px',
              },
            }}
          >
            Create New Order
          </Card>
          <Card
            hoverable
            className="w-full md:w-auto"
            styles={{
              body: {
                padding: '12px 20px',
              },
            }}
          >
            Generate Report
          </Card>
          <Card
            hoverable
            className="w-full md:w-auto"
            styles={{
              body: {
                padding: '12px 20px',
              },
            }}
          >
            Manage Inventory
          </Card>
        </Space>
      </div>
    </div>
  );
};

export default Dashboard;
