#!/bin/bash
# Railway部署功能测试脚本
# 测试所有API功能

BASE_URL="${1:-http://localhost:8000}"
TOKEN=""
ADMIN_TOKEN=""
OWNER_TOKEN=""

echo "=========================================="
echo "Railway部署功能测试"
echo "=========================================="
echo ""
echo "测试环境: $BASE_URL"
echo ""

# 登录管理员
echo "=== 1. 管理员登录 ==="
ADMIN_TOKEN=$(curl -s -X POST "$BASE_URL/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"phone":"13800138002","password":"adminpass123"}' | \
  python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null)

if [ -z "$ADMIN_TOKEN" ]; then
  echo "❌ 管理员登录失败"
  exit 1
fi
echo "✅ 管理员登录成功"
echo ""

# 登录业主
echo "=== 2. 业主登录 ==="
OWNER_TOKEN=$(curl -s -X POST "$BASE_URL/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"phone":"13800138001","password":"testpass123"}' | \
  python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null)

if [ -z "$OWNER_TOKEN" ]; then
  echo "❌ 业主登录失败"
  exit 1
fi
echo "✅ 业主登录成功"
echo ""

# 测试用户信息
echo "=== 3. 测试用户信息 ==="
curl -s "$BASE_URL/api/v1/users/profile" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"✅ 用户: {d.get('name')} ({d.get('phone')}) [{d.get('role')})\")" 2>/dev/null
echo ""

# 测试创建小区
echo "=== 4. 测试创建小区 ==="
curl -s -X POST "$BASE_URL/api/v1/admins/communities/" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"阳光花园","address":"北京市朝阳区阳光路1号","contact_phone":"010-12345678"}' | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"✅ 小区: {d.get('name')} (ID: {d.get('id')})\")" 2>/dev/null || echo "❌ 创建小区失败"
echo ""

# 测试创建房产
echo "=== 5. 测试创建房产 ==="
curl -s -X POST "$BASE_URL/api/v1/admins/properties/" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"community_id":1,"owner_id":1,"building_no":"1号楼","unit_no":"1单元","floor_no":"1","room_no":"101","area":100.5}' | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"✅ 房产: {d.get('building_no')}-{d.get('room_no')} (ID: {d.get('id')})\")" 2>/dev/null || echo "❌ 创建房产失败"
echo ""

# 测试创建账单
echo "=== 6. 测试创建账单 ==="
curl -s -X POST "$BASE_URL/api/v1/bills/" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"property_id":1,"bill_type":"property_fee","amount":500.00,"period":"2026-08","due_date":"2026-09-15","description":"2026年8月物业费"}' | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"✅ 账单: ¥{d.get('amount')} ({d.get('bill_type')})\")" 2>/dev/null || echo "❌ 创建账单失败"
echo ""

# 测试批量生成账单
echo "=== 7. 测试批量生成账单 ==="
curl -s -X POST "$BASE_URL/api/v1/bills/batch-generate" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"month":"2026-08","bill_type":"property_fee","amount":500.00}' | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"✅ 批量生成账单: {len(d) if isinstance(d, list) else d}\")" 2>/dev/null || echo "❌ 批量生成失败"
echo ""

# 测试统计
echo "=== 8. 测试统计数据 ==="
curl -s "$BASE_URL/api/v1/admins/stats/" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"✅ 统计: 用户{d.get('total_users')}, 房产{d.get('total_properties')}, 小区{d.get('total_communities')}\")" 2>/dev/null || echo "❌ 统计失败"
echo ""

# 测试业主创建报修
echo "=== 9. 测试业主创建报修 ==="
curl -s -X POST "$BASE_URL/api/v1/repairs/" \
  -H "Authorization: Bearer $OWNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"property_id":1,"repair_type":"indoor","title":"卫生间漏水","description":"卫生间天花板漏水","contact_phone":"13800138001"}' | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"✅ 报修: {d.get('title')} (ID: {d.get('id')})\")" 2>/dev/null || echo "❌ 创建报修失败"
echo ""

# 测试业主创建访客
echo "=== 10. 测试业主创建访客 ==="
curl -s -X POST "$BASE_URL/api/v1/visitors/" \
  -H "Authorization: Bearer $OWNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"property_id":1,"visitor_name":"张三","visitor_phone":"13900139001","start_time":"2026-08-16T10:00:00","end_time":"2026-08-16T12:00:00","visit_purpose":"拜访业主"}' | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"✅ 访客: {d.get('visitor_name')} (ID: {d.get('id')})\")" 2>/dev/null || echo "❌ 创建访客失败"
echo ""

# 测试业主创建投诉
echo "=== 11. 测试业主创建投诉 ==="
curl -s -X POST "$BASE_URL/api/v1/complaints/" \
  -H "Authorization: Bearer $OWNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"property_id":1,"complaint_type":"noise","title":"楼上噪音太大","description":"楼上经常深夜噪音","contact_phone":"13800138001"}' | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"✅ 投诉: {d.get('title')} (ID: {d.get('id')})\")" 2>/dev/null || echo "❌ 创建投诉失败"
echo ""

# 测试业主创建通知
echo "=== 12. 测试业主创建通知 ==="
curl -s -X POST "$BASE_URL/api/v1/notifications/" \
  -H "Authorization: Bearer $OWNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"notification_type":"system","title":"系统测试","content":"测试通知","target_user_id":1}' | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"✅ 通知: {d.get('title')} (ID: {d.get('id')})\")" 2>/dev/null || echo "❌ 创建通知失败"
echo ""

# 测试工单
echo "=== 13. 测试创建工单 ==="
curl -s -X POST "$BASE_URL/api/v1/work-orders/" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"property_id":1,"work_order_type":"repair","title":"电梯维修","description":"电梯故障","priority":"urgent"}' | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"✅ 工单: {d.get('title')} (ID: {d.get('id')})\")" 2>/dev/null || echo "❌ 创建工单失败"
echo ""

echo "=========================================="
echo "测试完成！"
echo "=========================================="
