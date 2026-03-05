# 导入必要的模块
from flask import Flask, jsonify, request  # Flask: 框架核心；jsonify: 返回 JSON；request: 处理请求数据

# 创建 Flask 应用实例
app = Flask(__name__)  # __name__ 用于确定应用路径，通常是当前模块名

# 示例数据：内存中的任务列表（实际中可使用数据库）
tasks = [
    {'id': 1, 'title': '买菜', 'done': False},  # 任务结构：id（唯一标识）、title（标题）、done（是否完成）
    {'id': 2, 'title': '学习 Flask', 'done': True}
]

# 定义路由：GET 获取所有任务
@app.route('/tasks', methods=['GET'])  # 路径 /tasks，只允许 GET 方法
def get_tasks():
    return jsonify({'tasks': tasks})  # 返回 JSON 格式的任务列表，HTTP 状态码默认 200

# 定义路由：GET 获取单个任务（根据 ID）
@app.route('/tasks/<int:task_id>', methods=['GET'])  # <int:task_id>：路径参数，task_id 为整数
def get_task(task_id):
    # 在列表中查找匹配 ID 的任务（使用 next() 和生成器表达式）
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({'error': '任务未找到'}), 404  # 返回错误信息和 404 状态码
    return jsonify({'task': task})  # 返回单个任务的 JSON

# 定义路由：POST 创建新任务
@app.route('/tasks', methods=['POST'])  # 只允许 POST 方法
def create_task():
    # 检查请求是否为 JSON 且包含 'title' 字段
    if not request.json or 'title' not in request.json:
        return jsonify({'error': '请求无效'}), 400  # 返回 400 Bad Request
    # 创建新任务：ID 自增，done 默认 False
    new_task = {
        'id': len(tasks) + 1,  # 计算新 ID
        'title': request.json['title'],  # 从请求 JSON 中获取 title
        'done': False
    }
    tasks.append(new_task)  # 添加到列表
    return jsonify({'task': new_task}), 201  # 返回新任务 JSON 和 201 Created 状态码

# 定义路由：PUT 更新任务（根据 ID）
@app.route('/tasks/<int:task_id>', methods=['PUT'])  # 只允许 PUT 方法
def update_task(task_id):
    # 查找任务
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({'error': '任务未找到'}), 404
    if not request.json:
        return jsonify({'error': '请求无效'}), 400
    # 更新字段：使用 get() 方法，如果未提供则保持原值
    task['title'] = request.json.get('title', task['title'])
    task['done'] = request.json.get('done', task['done'])
    return jsonify({'task': task})  # 返回更新后的任务

# 定义路由：DELETE 删除任务（根据 ID）
@app.route('/tasks/<int:task_id>', methods=['DELETE'])  # 只允许 DELETE 方法
def delete_task(task_id):
    global tasks  # 使用 global 声明修改全局变量
    # 过滤掉匹配 ID 的任务
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({'result': True})  # 返回成功结果，默认 200

# 运行应用：仅在直接执行脚本时运行（调试模式）
if __name__ == '__main__':
    app.run(debug=True)  # debug=True：启用调试，生产环境应关闭