import React, { useRef, useState } from 'react';
import '@ant-design/v5-patch-for-react-19';
import { 
  Button, 
  Flex, 
  Form, 
  Input, 
  Checkbox, 
  DatePicker, 
  Select, 
  Row, 
  Col,
  Alert 
} from 'antd';
import { openSerialSimple } from './components/SerialSimple';


export default function App() {
  const [connected, setConnected] = useState(false);
  const [logs, setLogs] = useState([]);
  const disconnectRef = useRef(null);

  const onFinish = values => {
    const id = 
    const uid = "ABC";
    const player_name = values.playerName;
    const dob = `${values.dob.$y}-${values.dob.$M+1}-${values.dob.$D}`;
    const email = values.email;
    const whatsapp = values.whatsapp;
    const membership_type = value.membershipType

  };
  const onFinishFailed = errorInfo => {
    console.error('Form submission failed:', errorInfo);
  };

  const handleData = (data, err) => {
    if (err) {
      console.error('Serial error', err);
      setLogs((l) => [...l, `ERROR: ${err.message ?? err}`]);
      return;
    }
    if (!data) return;

    // data is a decoded text chunk (string) from SerialSimple
    const s = data.trim();
    console.log('Serial incoming:', s);
    if(s.length === 8) {
      setLogs((l) => [...l, data.trim()]);
    }
 };

  const handleConnect = async () => {
    try {
      const session = await openSerialSimple(9600, handleData);
      // openSerialSimple returns { disconnect }
      disconnectRef.current = session.disconnect;
      setConnected(true);
      setLogs((l) => [...l, 'Connected']);
    } catch (e) {
      console.error('connect failed', e);
      setLogs((l) => [...l, `Connect failed: ${e.message ?? e}`]);
    }
  };

  const handleDisconnect = async () => {
    try {
      if (disconnectRef.current) await disconnectRef.current();
    } catch (e) {
      console.error('disconnect failed', e);
      setLogs((l) => [...l, `Disconnect error: ${e.message ?? e}`]);
    } finally {
      disconnectRef.current = null;
      setConnected(false);
      setLogs((l) => [...l, 'Disconnected']);
    }
  };

  return (
    <div style={{ padding: 20, fontFamily: 'system-ui, sans-serif' }}>
      <h2>Sport Hub Registration</h2>
      <Form
        name="basic"
        labelCol={{ span: 8 }}
        wrapperCol={{ span: 16 }}
        style={{ maxWidth: 600 }}
        initialValues={{ remember: true }}
        onFinish={onFinish}
        onFinishFailed={onFinishFailed}
        autoComplete="off"
      >
        <Form.Item
          label="Player Name"
          name="playerName"
          rules={[{ required: true, message: 'Please input your player name!' }]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="DOB"
          name="dob"
          rules={[{ required: true, message: 'Please input date of birth!' }]}
        >
          <DatePicker />
        </Form.Item>

        <Form.Item
          label="Email"
          name="email"
          rules={[{ required: true, message: 'Please input your email!' }]}
        >
          <Input />
        </Form.Item>

        {/* <Form.Item label="Connect to card" style={{ marginBottom: 12 }}>
          <button onClick={handleConnect} disabled={connected} style={{ marginRight: 8 }}>
            Connect
          </button>
          <button onClick={handleDisconnect} disabled={!connected}>
            Disconnect
          </button>
          <p>Card detected: {logs[logs.length - 1]}</p>
        </Form.Item> */}

        <Form.Item
          label="Whatsapp"
          name="whatsapp"
          rules={[{ required: true, message: 'whatsapp number...' }]}
        >
          <Input />
        </Form.Item>

        <Form.Item name="membershipType" label="Membership Type" rules={[{ required: true }]}>
          <Select
            placeholder="Membership Type..."
            allowClear
          >
            <Option value="daily">Daily</Option>
            <Option value="employee">Employee</Option>
          </Select>
        </Form.Item>


        <Form.Item label={null}>
          <Button type="primary" htmlType="submit">
            Submit
          </Button>
        </Form.Item>
      </Form>

    </div>
  );
}
