# 物业管理 APP 移动端

基于 Flutter 3.x 开发的业主端和工作人员端 APP。

## 项目结构

```
frontend-mobile/
├── lib/
│   ├── main.dart                 # 应用入口
│   ├── app.dart                  # 应用配置
│   ├── core/
│   │   ├── constants/           # 常量定义
│   │   ├── theme/               # 主题配置
│   │   └── utils/               # 工具函数
│   ├── data/
│   │   ├── models/              # 数据模型
│   │   ├── services/            # API 服务
│   │   └── repositories/        # 数据仓库
│   ├── domain/
│   │   ├── entities/            # 领域实体
│   │   └── usecases/            # 业务逻辑
│   ├── presentation/
│   │   ├── providers/           # Riverpod 状态管理
│   │   ├── pages/               # 页面
│   │   │   ├── owner/           # 业主端页面
│   │   │   └── staff/           # 工作人员端页面
│   │   └── widgets/             # 通用组件
│   └── routes/                  # 路由配置
├── test/
│   └── ...                      # 测试文件
└── pubspec.yaml                 # 依赖配置
```

## 技术栈

- Flutter 3.x
- Dart 3.x
- Riverpod 状态管理
- Dio HTTP 客户端
- flutter_secure_storage 安全存储
- qr_flutter 二维码生成
- image_picker 图片选择
- flutter_local_notifications 本地通知

## 依赖配置

```yaml
dependencies:
  flutter:
    sdk: flutter
  flutter_riverpod: ^2.4.0
  dio: ^5.3.0
  flutter_secure_storage: ^9.0.0
  qr_flutter: ^4.1.0
  image_picker: ^1.0.0
  flutter_local_notifications: ^16.0.0
  intl: ^0.18.0
  go_router: ^12.0.0
  
dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0
```

## API 端点

| 模块 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 认证 | POST | /api/v1/auth/register | 注册 |
| 认证 | POST | /api/v1/auth/login | 登录 |
| 认证 | GET | /api/v1/auth/me | 获取当前用户 |
| 认证 | POST | /api/v1/auth/logout | 登出 |
| 房产 | GET | /api/v1/properties/ | 房产列表 |
| 房产 | POST | /api/v1/properties/ | 创建房产 |
| 账单 | GET | /api/v1/bills/ | 账单列表 |
| 账单 | POST | /api/v1/bills/batch-generate | 批量生成 |
| 支付 | POST | /api/v1/payments/create | 创建支付 |
| 支付 | POST | /api/v1/payments/{id}/confirm | 确认支付 |
| 报修 | POST | /api/v1/repairs/ | 提交报修 |
| 报修 | GET | /api/v1/repairs/ | 报修列表 |
| 访客 | POST | /api/v1/visitors/ | 创建访客 |
| 投诉 | POST | /api/v1/complaints/ | 提交投诉 |
| 通知 | GET | /api/v1/notifications/ | 通知列表 |

## 业主端功能

- 登录/注册
- 首页（公告、快捷入口）
- 费用缴纳
- 报事报修
- 访客通行
- 智慧门禁
- 车位管理
- 投诉建议
- 消息中心
- 个人中心
- 房屋信息管理

## 工作人员端功能

- 登录/注册
- 首页（今日工单、待办）
- 工单管理
- 通知发布
- 访客审核
- 巡检管理
- 收费台账
- 人员管理
- 数据看板

## 开发指南

```bash
# 获取依赖
flutter pub get

# 运行应用
flutter run

# 运行测试
flutter test

# 构建 APK
flutter build apk --release

# 构建 iOS
flutter build ios --release
```

## 状态管理

使用 Riverpod 进行状态管理：

```dart
// 示例：认证状态
@riverpod
class AuthNotifier extends _$AuthNotifier {
  @override
  FutureOr<AuthState> build() async {
    // 初始化逻辑
    return AuthState.initial();
  }

  Future<void> login(String phone, String password) async {
    // 登录逻辑
  }

  void logout() {
    state = const AsyncData(AuthState.logout());
  }
}
```

## 注意事项

1. 所有 API 请求需要携带 JWT Token
2. 敏感数据使用 flutter_secure_storage 存储
3. 图片上传需要压缩处理
4. 离线数据使用 Hive 缓存
5. 通知推送集成 Firebase Cloud Messaging
