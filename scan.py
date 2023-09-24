import os
import re
import chardet

def scan_folder_for_chinese(folder_path):
    if os.path.isdir(folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                scan_folder_for_chinese(item_path)
            elif os.path.isfile(item_path):
                printChinese(item_path)
    elif os.path.isfile(folder_path):
        printChinese(item_path)

def printChinese(file_path):
    extention = file_path.split('.')[-1].upper()
    allow = extention in allowed_types
    # print(f"The file '{file_path}' is allowed?.'{extention in allowed_types}'")
    if not allow:
        return
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        # print(encoding)
    with open(file_path, 'r', encoding=encoding) as file:
        content = file.read()
        chinese_text = re.findall(r'[\u4e00-\u9fff]+', content)
        # print(chinese_text)
        if chinese_text:
            # print(content)
            for text in chinese_text:
                print(text)

def scan_files(folder_path, keywords, replacements):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                extention = file_path.split('.')[-1].upper()
                allow = extention in allowed_types
                # print(f"The file '{file_path}' is allowed?.'{extention in allowed_types}'")
                if not allow:
                    return
                process_file(file_path, keywords, replacements)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if "i18n" in dir_path:
                continue
            scan_files(dir_path, keywords, replacements)

def process_file(file_path, keywords, replacements):
    print(file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        # line = line.replace(" ","")
        for keyword, replacement in zip(keywords, replacements):
            if keyword in line:
                # line = line.replace(keywords[i], replacements[i])
                print(f"old line=>{line}")
                # pattern = rf':\s*".+"'
                pattern = rf'.:\s*"{keyword}"'
                match = re.search (pattern, line)
                if match != None:
                    # lines[i] = line.replace(f'label:"{keyword}"', f'label:this.$t("{replacement}")')
                    lines[i] = re.sub(pattern, f': this.$t("{replacement}")', line)
                    print("replace one=>"+ lines[i])
                # regex_pattern = r'([^=\s]+)=\s"{keyword}"'
                regex_pattern = rf'([^=\s]+)=(\"[{keyword}"]+\")'
                match = re.search (regex_pattern, line)
                if match:
                    replacement = re.sub(regex_pattern, r':\1='+ f'"$t(\'{replacement}\')"', match.group(0))
                    line = re.sub(regex_pattern, replacement, line)
                    print("replace two=>"+ line)
                regex_pattern = rf'>({keyword})<'
                match = re.search (regex_pattern, line)
                if match:
                    # replacement = re.sub(regex_pattern, r':\1='+ f'"$t(\'{replacement}\')"', match.group(0))
                    lines[i] = re.sub(regex_pattern, f'>{{{{$t("{replacement}")}}}}<', line)
                    print("replace three=>"+ lines[i])
        # modified_lines.append(line)

    # with open(file_path, 'w', encoding='utf-8') as file:
    #     file.writelines(lines)
# 指定要扫描的文件夹路径
allowed_types = ['VUE','TS','JS']
# 中文关键字数组和替换值数组
replacements=['failed', 'success', 'operationFailed', 'operationSuccess', 'login', 'logout', 'functionMenu', 'admin', 'dishManagement', 'tableManagement', 'kitchenManagement', 'waiter', 'waiterView', 'ongoingOrders', 'tableView', 'chef', 'chefView', 'orderAssignmentView', 'reportManagement', 'allHistoricalOrders', 'historicalOrders', 'table', 'userManagement', 'user', 'get', 'failure', 'back', 'addDish', 'tableNumber', 'dish', 'quantity', 'portion', 'note', 'pleaseCheckEntries', 'unknownError', 'oldPassword', 'newPassword', 'update', 'newPasswordLength', 'characters', 'newPasswordsMismatch', 'inputsMismatch', 'invalidInput', 'orderAssignmentKitchenView', 'hideOffline', 'kitchenStation', 'complete', 'online', 'blocked', 'offline', 'failedToRetrieveKitchenData', 'enterDish', 'filterByTag', 'yuan', 'delete', 'deleteConfirmation', 'yes', 'no', 'editDish', 'uploadImage', 'dishName', 'dishDescription', 'addDishTag', 'averagePreparationTime', 'minutes', 'price', 'backToDishList', 'uploadComplete', 'dishNameRequired', 'duplicateTag', 'historicalOrdersOf', 'refreshList', 'ongoing', 'completed', 'orderNumber', 'creator', 'orderStatus', 'creationTime', 'completionTime', 'failedToLoadTableInfo', 'createNewKitchenStation', 'edit', 'mayUseHere', 'attribute', 'kitchenStationNumber', 'required', 'description', 'create', 'editKitchenStation', 'kitchenStationNumberRequired', 'incorrectUsernameOrPassword', 'createNewDish', 'readyForPickup', 'unassigned', 'inProgress', 'served', 'markAsCooked', 'refreshTableView', 'viewCompletedDishes', 'totalPrice', 'backToOngoingOrders', 'backToHistoricalOrders', 'assignDishToKitchenStation', 'assignToKitchenStation', 'endOrder', 'paid', 'pendingAssignment', 'assignmentFailed', 'status', 'unitPrice', 'assignKitchenStation', 'operation', 'updateTime', 'modifyNote', 'legacyCodeUsed', 'periodicRefresh', 'usedToUpdateDynamicStatus', 'backToTableView', 'endOrderForTable', 'noDishesAvailableForAssignment', 'refreshOrder', 'newOrder', 'deleteOrder', 'finish', 'confirmDeleteOrder', 'viewHistoricalOrders', 'createNewTable', 'editTable', 'confirm', 'confirmDeleteTable', 'tableNumberRequired', 'createNewUser', 'all', 'searchUser', 'role', 'resetPassword', 'username', 'password', 'selectRole', 'permissionRole', 'selectARole', 'confirmDeleteUser', 'usernameAndRoleRequired', 'kitchen', 'kitchenOrderingSystem', 'changePassword', 'of', 'createDish']
keywords=['操作失败', '操作成功', '操作失败', '操作成功', '登录', '登出', '功能菜单', '管理员', '菜品管理', '餐桌管理', '厨房管理', '服务员', '服务员视图', '进行中订单', '餐桌视图', '厨师', '厨师视图', '点菜分配视图', '报表管理', '全部历史订单', '历史订单', '餐桌', '用户管理', '用户', '获取', '失败', '返回', '加菜', '桌号', '菜品', '数量', '份', '备注', '请检查填写的条目', '未知错误', '原密码', '新密码', '更新', '新密长度至少为', '个字符', '两次输入新密码不一致', '两次输入不一致', '不合法的输入', '点菜分配厨位视图', '不显示离线', '厨位', '完成', '在线', '阻挡', '离线', '获取厨位数据失败', '录入菜品', '按标签过滤', '元', '删除', '删除确认', '是', '否', '编辑菜品', '上传图片', '菜名', '菜品描述', '添加菜品标签', '平均制作工时', '分钟', '价格', '返回菜品列表', '上传完毕', '菜名不得为空', '重复标签', '的历史订单', '刷新列表', '进行中', '已完成', '订单号', '创建人', '订单状态', '创建时间', '完成时间', '载入餐桌信息失败', '新建厨位', '编辑', '这里可能使用', '属性', '厨位号', '必填', '描述', '创建', '编辑厨位', '厨位号不能为空', '用户名或密码不对', '新建菜品', '完成待取', '未分配', '制作中', '已上菜', '划菜', '定时刷新桌面视图', '用于查看已经完成的菜品', '总价', '返回进行中订单列表', '返回历史订单列表', '分配菜品到厨位', '分配到厨位', '结束订单', '已买单', '待分配', '分配失败', '状态', '单价', '分配厨位', '操作', '更新时间', '修改备注', '旧代码采用', '定时刷新', '用于更新不断变化的状态', '返回餐桌视图', '结束本桌订单', '无可分配菜品', '刷新订单', '新订单', '删除订单', '完结', '确认删除订单', '查看历史订单', '新建餐桌', '编辑餐桌', '确认', '确认删除该餐桌吗', '桌号不能为空', '新建用户', '所有', '搜用户', '角色', '重置密码', '用户名', '密码', '选择角色', '权限角色', '您需要先选中一个角色哦', '确认删除该用户吗', '用户名和角色不能为空', '小厨', '厨房点菜一体化系统', '修改密码', '的', '创建菜品']
# keywords = ['管理员', '服务员', '加菜','订单状态','新建餐桌','创建人', '创建时间', '完成时间']
# replacements = ['admin', 'waiter', 'addDish', 'orderStatus', 'createNewTable', 'creator', 'creationTime', 'completionTime']
folder_path = 'H:\kitchen\kitchen-web\src'
scan_files(folder_path, keywords, replacements)
# 调用函数进行扫描
# scan_folder_for_chinese(folder_path)