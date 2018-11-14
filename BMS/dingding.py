from dingtalk_sdk_gmdzy2010.authority_request import AccessTokenRequest
from BMS import settings
from em.models import Employees
from django.contrib.auth.models import Group,User
import datetime

###获取access_token，之后的所有接口调用都需要这个token，其有效期为2小时，超时后刷新即可
params = {"appkey": settings.DINGTALK_APPKEY, "appsecret": settings.DINGTALK_SECRET}
request = AccessTokenRequest(params=params)
request.get_json_response()
access_token = request.get_access_token()


from dingtalk_sdk_gmdzy2010.department_request import  DeptsRequest, SubDeptIdsRequest
from dingtalk_sdk_gmdzy2010.user_request import DeptUsersSimpleRequest
from dingtalk_sdk_gmdzy2010.message_request import CreateGroupChatRequest,SendGroupChatRequest


def recruit_dept_ids(init_ids=None, total_ids=None, access_token=None):
    if init_ids:
        sub_level_ids = []
        for id in init_ids:
            params = {"access_token": access_token, "id": id}
            get_new_ids = SubDeptIdsRequest(params=params)
            get_new_ids.get_json_response()
            new_ids = get_new_ids.get_sub_dept_ids()
            sub_level_ids.extend(new_ids)
            if not new_ids:
                continue
        total_ids.extend(sub_level_ids)
        return recruit_dept_ids(init_ids=sub_level_ids, total_ids=total_ids,
                                access_token=access_token)
    else:
        return total_ids


def get_sub_dept_users(dept_ids=None):
    if dept_ids:
        dept_users = []
        for id in dept_ids:
            params = {"access_token": access_token, "department_id": id}
            get_users = DeptUsersSimpleRequest(params=params)
            get_users.get_json_response()
            users = get_users.get_dept_users_brief()
            dept_users.extend(users)
        return dept_users


# get_level_2_depts_params = {
#     "access_token": access_token,
#     "id": 1,
#     "fetch_child": False,
# }
# get_level_2_depts = DeptsRequest(params=get_level_2_depts_params)
# get_level_2_depts.get_json_response()
#
# # 以下get_depts方法在0.2.4版本才有
# level_2_depts = get_level_2_depts.get_depts(dept_name="科技服务事业部")
# sub_dept_ids = recruit_dept_ids(init_ids=[level_2_depts["id"]],
#                                 total_ids=[level_2_depts["id"]],
#                                 access_token=access_token)
# sub_dept_users = get_sub_dept_users(dept_ids=sub_dept_ids)
# n=0
# un=0
# mn=0
# for user in sub_dept_users:
#     users_django = User.objects.filter(last_name__exact=user['name'][0],first_name__exact=user['name'][1:])
#     if users_django:
#         if len(users_django) == 1:
#             user_django = users_django[0]
#             employees = Employees.objects.filter(user=user_django)
#             if employees:
#                 employees.dingtalk_id = user['userid']
#                 employees.dingtalk_name = user['name']
#                 employees.is_on_job = user_django.is_staff
#                 employees.submit_date = datetime.datetime.now()
#                 mn = mn + 1
#             else:
#                 Employees.objects.create(user=user_django,dingtalk_id=user['userid'],dingtalk_name=user['name'],
#                                      submit_date=datetime.datetime.now(),is_on_job=user_django.is_staff)
#                 n = n +1
#     else:
#         un = un + 1
# print("总共%s个员工，添加成功的%s个员工，不成功的%s个员工，修改成功的%s个员工"%(len(sub_dept_users),n,un,mn))
# #讨论组
# params = {"access_token": access_token}
# # data = {
# #                 "name": "test",
# #                 "owner":"03561038053843",
# #                 "useridlist":["03561038053843","09525308101247799",],
# #
# #             }
#
# # chat = CreateGroupChatRequest(params=params,json=data)
# # chat.request_method = "post"
# # chat.get_json_response()
# # response = chat.json_response
# # chat_id = chat.get_chat_id()
# # print("马圣+黄云群聊ID:"+chat_id)
#
# #马圣+黄云群聊ID:chat62dbddc59ef51ae0f4a47168bdd2a65b
# ##讨论组发消息
# # chat_id="chat62dbddc59ef51ae0f4a47168bdd2a65b"
# #
# # data = {
# #                 "chatid": chat_id,
# #                 "msg": {
# #                     "msgtype": "text",
# #                     "text": {
# #                         "content": "【测试通知】测试消息2"
# #                     }
# #                 }
# #             }
# #
# # chatMessage = SendGroupChatRequest(params=params,json=data)
# # chatMessage.request_method = "post"
# # chatMessage.get_json_response()
# # response = chatMessage.json_response
# # print(response)



