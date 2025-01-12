'use client'

import { useEffect, useState } from 'react'
import { Table, Card, Statistic, Row, Col } from 'antd'
import { ShopOutlined, CheckCircleOutlined, SyncOutlined } from '@ant-design/icons'
import useWebSocket from '@/hooks/useWebSocket'
import { OrderType } from '../types/order'

export default function DashboardPage() {
    const [orders, setOrders] = useState<OrderType[]>([])
    const socket = useWebSocket('ws://localhost:8000/api/v1/orders/ws')

    useEffect(() => {
        // Fetch initial orders
        fetch('http://localhost:8000/api/v1/orders')
            .then(res => res.json())
            .then(data => setOrders(data))
    }, [])

    useEffect(() => {
        if (!socket) return

        socket.onmessage = (event) => {
            const message = JSON.parse(event.data)

            switch (message.type) {
                case 'new_order':
                    setOrders(prev => [...prev, message.data])
                    break
                case 'order_updated':
                    setOrders(prev => prev.map(order =>
                        order.id === message.data.id ? message.data : order
                    ))
                    break
            }
        }
    }, [socket])

    const columns = [
        {
            title: 'Order ID',
            dataIndex: 'id',
            key: 'id',
            width: 100,
        },
        {
            title: 'Dish',
            dataIndex: 'dish_name',
            key: 'dish_name',
        },
        {
            title: 'Quantity',
            dataIndex: 'quantity',
            key: 'quantity',
            width: 100,
        },
        {
            title: 'Status',
            dataIndex: 'status',
            key: 'status',
            width: 150
        },
        {
            title: 'Created At',
            dataIndex: 'created_at',
            key: 'created_at',
            render: (date: string) => new Date(date).toLocaleString(),
        },
    ]

    const stats = {
        total: orders.length,
        pending: orders.filter(o => o.status === 'pending').length,
        preparing: orders.filter(o => o.status === 'preparing').length,
        completed: orders.filter(o => o.status === 'completed').length,
    }

    return (
        <div className="p-8">
            <h1 className="text-2xl font-bold mb-8">Order Dashboard</h1>

            <Row gutter={16} className="mb-8">
                <Col span={6}>
                    <Card>
                        <Statistic
                            title="Total Orders"
                            value={stats.total}
                            prefix={<ShopOutlined />}
                        />
                    </Card>
                </Col>
                <Col span={6}>
                    <Card>
                        <Statistic
                            title="Pending"
                            value={stats.pending}
                            prefix={<SyncOutlined spin />}
                        />
                    </Card>
                </Col>
                <Col span={6}>
                    <Card>
                        <Statistic
                            title="Preparing"
                            value={stats.preparing}
                            prefix={<SyncOutlined />}
                        />
                    </Card>
                </Col>
                <Col span={6}>
                    <Card>
                        <Statistic
                            title="Completed"
                            value={stats.completed}
                            prefix={<CheckCircleOutlined />}
                        />
                    </Card>
                </Col>
            </Row>

            <Card>
                <Table
                    columns={columns}
                    dataSource={orders}
                    rowKey="id"
                    pagination={false}
                    virtual={true}
                />
            </Card>
        </div>
    )
}