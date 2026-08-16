#!/bin/bash
# 物业管理APP全面功能检查脚本

echo "=========================================="
echo "物业管理APP - 全面功能检查"
echo "=========================================="
echo ""
echo "检查时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

BASE_URL="http://localhost:8000"
PASS=0
FAIL=0

# 登录获取Token
echo "=== 1. 用户认证 ==="
TOKEN=$(curl -s -X POST "$BASE_URL/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"phone":"13800138002","password":"adminpass123"}' | \
  python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null)

if [ -n "$TOKEN" ]; then
    echo "✅ 登录成功"
    PASS=$((PASS+1))
else
    echo "❌ 登录失败"
    FAIL=$((FAIL+1))
fi
echo ""

# 用户信息
echo "=== 2. 用户信息 ==="
curl -s "$BASE_URL/api/v1/users/profile" \
  -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys,json
d=json.load(sys.stdin)
if d.get('name'):
    print(f'✅ 用户: {d.get(\"name\")} ({d.get(\"phone\")}) [{d.get(\"role\")})')
    exit(0)
else:
    print(f'❌ 获取用户信息失败')
    exit(1)
" && PASS=$((PASS+1)) || FAIL=$((FAIL+1))
echo ""

# 创建小区
echo "=== 3. 创建小区 ==="
curl -s -X POST "$BASE_URL/api/v1/admins/communities/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"阳光花园","address":"北京市朝阳区","contact_phone":"010-12345678"}' | python3 -c "
import sys,json
d=json.load(sys.stdin)
if d.get('id'):
    print(f'✅ 小区: {d.get(\"name\")} (ID: {d.get(\"id\")})')
    exit(0)
else:
    print(f'❌ 创建小区失败')
    exit(1)
" && PASS=$((PASS+1)) || FAIL=$((FAIL+1))
echo ""

# 创建房产
echo "=== 4. 创建房产 ==="
curl -s -X POST "$BASE_URL/api/v1/admins/properties/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"community_id":1,"owner_id":1,"building_no":"1号楼","unit_no":"1单元","floor_no":"1","room_no":"101","area":100.5}' | python3 -c "
import sys,json
d=json.load(sys.stdin)
if d.get('id'):
    print(f'✅ 房产: {d.get(\"building_no\")}-{d.get(\"room_no\")} (ID: {d.get(\"id\")})')
    exit(0)
else:
    print(f'❌ 创建房产失败')
    exit(1)
" && PASS=$((PASS+1)) || FAIL=$((FAIL+1))
echo ""

# 创建账单
echo "=== 5. 创建账单 ==="
curl -s -X POST "$BASE_URL/api/v1/bills/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"property_id":1,"bill_type":"property_fee","amount":500.00,"period":"2026-08","due_date":"2026-09-15","description":"物业费"}' | python3 -c "
import sys,json
d=json.load(sys.stdin)
if d.get('id'):
    print(f'✅ 账单: ¥{d.get(\"amount\")} ({d.get(\"bill_type\")})')
    exit(0)
else:
    print(f'❌ 创建账单失败')
    exit(1)
" && PASS=$((PASS+1)) || FAIL=$((FAIL+1))
echo ""

# 批量生成账单
echo "=== 6. 批量生成账单 ==="
curl -s -X POST "$BASE_URL/api/v1/bills/batch-generate" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"month":"2026-08","bill_type":"property_fee","amount":500.00}' | python3 -c "
import sys,json
d=json.load(sys.stdin)
if isinstance(d, list) and len(d) > 0:
    print(f'✅ 批量生成: {len(d)}条账单')
    exit(0)
else:
    print(f'❌ 批量生成失败')
    exit(1)
" && PASS=$((PASS+1)) || FAIL=$((FAIL+1))
echo ""

# 统计数据
echo "=== 7. 统计数据 ==="
curl -s "$BASE_URL/api/v1/admins/stats/" \
  -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys,json
d=json.load(sys.stdin)
if d.get('total_users'):
    print(f'✅ 统计: 用户{d.get(\"total_users\")}, 房产{d.get(\"total_properties\")}, 小区{d.get(\"total_communities\")}')
    exit(0)
else:
    print(f'❌ 统计失败')
    exit(1)
" && PASS=$((PASS+1)) || FAIL=$((FAIL+1))
echo ""

# 业主登录
echo "=== 8. 业主登录 ==="
OWNER_TOKEN=$(curl -s -X POST "$BASE_URL/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"phone":"13800138001","password":"testpass123"}' | \
  python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null)

if [ -n "$OWNER_TOKEN" ]; then
    echo "✅ 业主登录成功"
    PASS=$((PASS+1))
else
    echo "❌ 业主登录失败"
    FAIL=$((FAIL+1))
fi
echo ""

# 创建报修
echo "=== 9. 创建报修 ==="
curl -s -X POST "$BASE_URL/api/v1/repairs/" \
  -H "Authorization: Bearer $OWNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"property_id":1,"repair_type":"indoor","title":"卫生间漏水","description":"天花板漏水","contact_phone":"13800138001"}' | python3 -c "
import sys,json
d=json.load(sys.stdin)
if d.get('id'):
    print(f'✅ 报修: {d.get(\"title\")} (ID: {d.get(\"id\")})')
    exit(0)
else:
    print(f'❌ 创建报修失败')
    exit(1)
" && PASS=$((PASS+1)) || FAIL=$((FAIL+1))
echo ""

# 创建访客
echo "=== 10. 创建访客 ==="
curl -s -X POST "$BASE_URL/api/v1/visitors/" \
  -H "Authorization: Bearer $OWNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"property_id":1,"visitor_name":"张三","visitor_phone":"13900139001","start_time":"2026-08-16T10:00:00","end_time":"2026-08-16T12:00:00","visit_purpose":"拜访业主"}' | python3 -c "
import sys,json
d=json.load(sys.stdin)
if d.get('id'):
    print(f'✅ 访客: {d.get(\"visitor_name\")} (ID: {d.get(\"id\")})')
    exit(0)
else:
    print(f'❌ 创建访客失败')
    exit(1)
" && PASS=$((PASS+1)) || FAIL=$((FAIL+1))
echo ""

# 创建投诉
echo "=== 11. 创建投诉 ==="
curl -s -X POST "$BASE_URL/api/v1/complaints/" \
  -H "Authorization: Bearer $OWNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"property_id":1,"complaint_type":"noise","title":"楼上噪音","description":"深夜噪音","contact_phone":"13800138001"}' | python3 -c "
import sys,json
d=json.load(sys.stdin)
if d.get('id'):
    print(f'✅ 投诉: {d.get(\"title\")} (ID: {d.get(\"id\")})')
    exit(0)
else:
    print(f'❌ 创建投诉失败')
    exit(1)
" && PASS=$((PASS+1)) || FAIL=$((FAIL+1))
echo ""

# 创建通知
echo "=== 12. 创建通知 ==="
curl -s -X POST "$BASE_URL/api/v1/notifications/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"notification_type":"announcement","title":"停水通知","content":"周末停水","target_user_id":1,"priority":"high"}' | python3 -c "
import sys,json
d=json.load(sys.stdin)
if d.get('id'):
    print(f'✅ 通知: {d.get(\"title\")} (ID: {d.get(\"id\")})')
    exit(0)
else:
    print(f'❌ 创建通知失败')
    exit(1)
" && PASS=$((PASS+1)) || FAIL=$((FAIL+1))
echo ""

# 创建工单
echo "=== 13. 创建工单 ==="
curl -s -X POST "$BASE_URL/api/v1/work-orders/work-orders/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"property_id":1,"order_type":"repair","title":"电梯维修","description":"电梯故障","priority":"urgent"}' | python3 -c "
import sys,json
d=json.load(sys.stdin)
if d.get('id'):
    print(f'✅ 工单: {d.get(\"title\")} (ID: {d.get(\"id\")})')
    exit(0)
else:
    print(f'❌ 创建工单失败')
    exit(1)
" && PASS=$((PASS+1)) || FAIL=$((FAIL+1))
echo ""

# 总结
echo "=========================================="
echo "检查完成！"
echo "=========================================="
echo ""
echo "通过: $PASS/13"
echo "失败: $FAIL/13"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "✅ 所有功能正常！"
else
    echo "⚠️ 有部分功能异常，请检查日志"
fi
echo ""
