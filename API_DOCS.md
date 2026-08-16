# 物业管理APP - API文档

> 基于 OpenAPI 3.0 标准生成

## 基础信息

- Base URL: `http://localhost:8000/api/v1`
- 认证方式: JWT Bearer Token
- 内容类型: application/json

## 认证接口

### 用户注册
```
POST /api/v1/auth/register
```
**请求体:**
```json
{
  "phone": "13800138001",
  "password": "testpass123",
  "role": "owner",
  "name": "张三"
}
```
**响应:**
```json
{
  "id": 1,
  "phone": "13800138001",
  "name": "张三",
  "role": "owner",
  "status": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### 用户登录
```
POST /api/v1/auth/login
```
**请求体:**
```json
{
  "phone": "13800138001",
  "password": "testpass123"
}
```
**响应:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### 获取当前用户信息
```
GET /api/v1/auth/me
```
**响应:**
```json
{
  "id": 1,
  "phone": "13800138001",
  "name": "张三",
  "role": "owner",
  "status": true
}
```

### 用户登出
```
POST /api/v1/auth/logout
```

## 用户管理

### 获取用户列表 (管理员)
```
GET /api/v1/users/?skip=0&limit=100
```

### 获取用户详情 (管理员)
```
GET /api/v1/users/{user_id}
```

### 更新用户状态 (管理员)
```
PUT /api/v1/users/{user_id}/status
```
**请求体:**
```json
{
  "status": true
}
```

### 获取个人资料
```
GET /api/v1/users/profile
```

### 更新个人资料
```
PUT /api/v1/users/profile
```

## 房产管理

### 获取房产列表
```
GET /api/v1/properties/?skip=0&limit=100
```

### 创建房产
```
POST /api/v1/properties/
```
**请求体:**
```json
{
  "community_id": 1,
  "building_no": "1",
  "unit_no": "1",
  "floor_no": "1",
  "room_no": "101",
  "area": 100.0
}
```

### 获取房产详情
```
GET /api/v1/properties/{property_id}
```

### 更新房产
```
PUT /api/v1/properties/{property_id}
```

### 删除房产
```
DELETE /api/v1/properties/{property_id}
```

## 账单管理

### 获取账单列表
```
GET /api/v1/bills/?skip=0&limit=100&status=pending
```

### 创建账单
```
POST /api/v1/bills/
```

### 获取账单详情
```
GET /api/v1/bills/{bill_id}
```

### 批量生成账单
```
POST /api/v1/bills/batch-generate
```

## 支付管理

### 获取支付记录
```
GET /api/v1/payments/?skip=0&limit=100
```

### 创建支付订单
```
POST /api/v1/payments/create
```
**请求体:**
```json
{
  "bill_id": 1,
  "payment_method": "wechat"
}
```

### 确认支付
```
POST /api/v1/payments/{payment_id}/confirm
```

## 报修管理

### 获取报修列表
```
GET /api/v1/repairs/?skip=0&limit=100&status=pending
```

### 提交报修
```
POST /api/v1/repairs/
```
**请求体:**
```json
{
  "property_id": 1,
  "repair_type": "indoor",
  "title": "漏水维修",
  "description": "厨房水龙头漏水"
}
```

### 获取报修详情
```
GET /api/v1/repairs/{repair_id}
```

### 更新报修状态
```
PUT /api/v1/repairs/{repair_id}
```

### 评价报修
```
POST /api/v1/repairs/{repair_id}/evaluate?rating=5&comment=服务很好
```

## 访客管理

### 获取访客列表
```
GET /api/v1/visitors/?skip=0&limit=100
```

### 创建访客
```
POST /api/v1/visitors/
```
**请求体:**
```json
{
  "property_id": 1,
  "visitor_name": "李四",
  "visitor_phone": "13900139000",
  "start_time": "2024-01-01T10:00:00Z",
  "end_time": "2024-01-01T14:00:00Z"
}
```

### 获取访客详情
```
GET /api/v1/visitors/{visitor_id}
```

### 访客签到
```
POST /api/v1/visitors/{visitor_id}/check-in
```

## 投诉建议

### 获取投诉列表
```
GET /api/v1/complaints/?skip=0&limit=100
```

### 提交投诉
```
POST /api/v1/complaints/
```

### 获取投诉详情
```
GET /api/v1/complaints/{complaint_id}
```

### 更新投诉状态
```
PUT /api/v1/complaints/{complaint_id}
```

## 通知管理

### 获取通知列表
```
GET /api/v1/notifications/?skip=0&limit=100
```

### 创建通知 (管理员)
```
POST /api/v1/notifications/
```

### 标记已读
```
POST /api/v1/notifications/mark-all-read
```

## 工单管理

### 获取工单列表
```
GET /api/v1/work-orders/work-orders/?skip=0&limit=100
```

### 创建工单
```
POST /api/v1/work-orders/work-orders/
```

### 更新工单
```
PUT /api/v1/work-orders/work-orders/{order_id}
```

## 巡检任务

### 获取巡检任务列表
```
GET /api/v1/work-orders/inspection-tasks/?skip=0&limit=100
```

### 创建巡检任务 (管理员)
```
POST /api/v1/work-orders/inspection-tasks/
```

## 管理员接口

### 获取统计数据
```
GET /api/v1/admins/stats/
```
**响应:**
```json
{
  "total_users": 150,
  "total_properties": 300,
  "pending_repairs": 12,
  "overdue_bills": 5,
  "monthly_revenue": 45000.00
}
```

### 获取用户列表
```
GET /api/v1/admins/users/?skip=0&limit=100
```

### 获取房产列表
```
GET /api/v1/admins/properties/?skip=0&limit=100
```

### 获取小区列表
```
GET /api/v1/admins/communities/?skip=0&limit=100
```

## 错误响应

### 400 Bad Request
```json
{
  "detail": "手机号已注册"
}
```

### 401 Unauthorized
```json
{
  "detail": "Unauthorized"
}
```

### 403 Forbidden
```json
{
  "detail": "Not allowed"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

## 数据模型

### User
```json
{
  "id": 1,
  "phone": "13800138001",
  "name": "张三",
  "role": "owner",
  "status": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Property
```json
{
  "id": 1,
  "community_id": 1,
  "owner_id": 1,
  "building_no": "1",
  "unit_no": "1",
  "floor_no": "1",
  "room_no": "101",
  "area": 100.0
}
```

### Bill
```json
{
  "id": 1,
  "property_id": 1,
  "bill_type": "property_fee",
  "amount": 500.00,
  "due_date": "2024-02-01T00:00:00Z",
  "status": "pending",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Repair
```json
{
  "id": 1,
  "property_id": 1,
  "repair_type": "indoor",
  "title": "漏水维修",
  "description": "厨房水龙头漏水",
  "status": "pending",
  "rating": 0,
  "created_at": "2024-01-01T00:00:00Z"
}
```
