# 物业管理 APP 移动端开发计划

## 技术栈
- Flutter 3.x
- Dart 3.x
- Riverpod 状态管理
- Dio HTTP 客户端
- GoRouter 路由管理
- flutter_secure_storage 安全存储

## 项目结构

```
frontend-mobile/
├── lib/
│   ├── main.dart                    # 应用入口
│   ├── app.dart                     # 应用配置
│   ├── core/
│   │   ├── constants/              # 常量定义
│   │   ├── theme/                  # 主题配置
│   │   └── utils/                  # 工具函数
│   ├── data/
│   │   ├── models/                 # 数据模型
│   │   │   ├── user.dart
│   │   │   ├── property.dart
│   │   │   ├── bill.dart
│   │   │   ├── repair.dart
│   │   │   └── visitor.dart
│   │   ├── services/               # API 服务
│   │   │   └── api_service.dart
│   │   └── repositories/           # 数据仓库
│   ├── domain/
│   │   ├── entities/               # 领域实体
│   │   └── usecases/               # 业务逻辑
│   ├── presentation/
│   │   ├── providers/              # Riverpod 状态管理
│   │   │   ├── auth_provider.dart
│   │   │   ├── property_provider.dart
│   │   │   ├── bill_provider.dart
│   │   │   └── repair_provider.dart
│   │   ├── pages/
│   │   │   ├── owner/              # 业主端页面
│   │   │   │   ├── home_page.dart
│   │   │   │   ├── bills_page.dart
│   │   │   │   ├── repairs_page.dart
│   │   │   │   ├── visitors_page.dart
│   │   │   │   ├── complaints_page.dart
│   │   │   │   └── profile_page.dart
│   │   │   └── staff/              # 工作人员端页面
│   │   │       ├── home_page.dart
│   │   │       ├── work_orders_page.dart
│   │   │       ├── inspection_page.dart
│   │   │       └── staff_profile_page.dart
│   │   ├── widgets/                # 通用组件
│   │   └── navigation/             # 导航
│   └── routes/
│       └── app_router.dart
├── test/
│   ├── unit/
│   ├── widget/
│   └── integration/
└── pubspec.yaml
```

## 已创建文件

### 核心文件
- ✅ `lib/main.dart` - 应用入口
- ✅ `lib/core/constants/constants.dart` - 常量定义
- ✅ `lib/core/theme/app_theme.dart` - 主题配置

### 数据模型
- ✅ `lib/data/models/user.dart`
- ✅ `lib/data/models/property.dart`
- ✅ `lib/data/models/bill.dart`
- ✅ `lib/data/models/repair.dart`
- ✅ `lib/data/models/visitor.dart`

### API 服务
- ✅ `lib/data/services/api_service.dart`

### 状态管理
- ✅ `lib/presentation/providers/auth_provider.dart`

### 页面
- ✅ `lib/presentation/pages/auth/login_page.dart`
- ✅ `lib/presentation/pages/owner/home_page.dart`
- ✅ `lib/presentation/pages/staff/home_page.dart`

### 路由
- ✅ `lib/routes/app_router.dart`

### 配置文件
- ✅ `pubspec.yaml`
- ✅ `README.md`

## 待开发功能

### 业主端
- [ ] 启动页/引导页
- [ ] 注册页面
- [ ] 费用缴纳页面（含模拟支付）
- [ ] 报事报修页面（含图片上传）
- [ ] 访客管理页面
- [ ] 智慧门禁页面
- [ ] 车位管理页面
- [ ] 投诉建议页面
- [ ] 消息中心
- [ ] 个人中心
- [ ] 房屋信息管理

### 工作人员端
- [ ] 工单管理页面
- [ ] 通知发布页面
- [ ] 访客审核页面
- [ ] 巡检管理页面
- [ ] 收费台账页面
- [ ] 人员管理页面
- [ ] 数据看板页面

### 通用功能
- [ ] 图片上传功能
- [ ] 二维码扫描功能
- [ ] 通知推送集成
- [ ] 离线缓存机制

## API 端点映射

| 功能 | 方法 | 端点 |
|------|------|------|
| 登录 | POST | /api/v1/auth/login |
| 注册 | POST | /api/v1/auth/register |
| 获取用户 | GET | /api/v1/auth/me |
| 登出 | POST | /api/v1/auth/logout |
| 房产列表 | GET | /api/v1/properties/ |
| 账单列表 | GET | /api/v1/bills/ |
| 批量生成账单 | POST | /api/v1/bills/batch-generate |
| 创建支付 | POST | /api/v1/payments/create |
| 确认支付 | POST | /api/v1/payments/{id}/confirm |
| 提交报修 | POST | /api/v1/repairs/ |
| 报修列表 | GET | /api/v1/repairs/ |
| 创建访客 | POST | /api/v1/visitors/ |
| 访客列表 | GET | /api/v1/visitors/ |
| 提交投诉 | POST | /api/v1/complaints/ |
| 通知列表 | GET | /api/v1/notifications/ |

## 测试计划

### 单元测试
- [ ] API 服务测试
- [ ] 数据模型测试
- [ ] 状态管理测试
- [ ] 工具函数测试

### Widget 测试
- [ ] 登录页面测试
- [ ] 首页组件测试
- [ ] 表单组件测试

### 集成测试
- [ ] 登录流程测试
- [ ] 导航流程测试
- [ ] API 联调测试

## 构建命令

```bash
# 获取依赖
flutter pub get

# 运行测试
flutter test

# 构建 APK
flutter build apk --release

# 构建 iOS
flutter build ios --release

# 运行应用
flutter run
```
