# Временный файл для тестирования фрагментов кода - УДАЛИТЬ!!!

# a = {'csrfmiddlewaretoken': ['CAzCGTlUaGkHWPzAk0eU8FYNVQ74VJrUnrgNZ1Mv8jMMOrGkalDRtIvkdkRBKS1Z'], 'author': [
#     '1'], 'tittle': ['36'], 'text': ['36 dfgsdg'], 'type': ['ARTICLE'], 'category': ['2', '4']}
# print(a['category'])
# b = <QueryDict: {'csrfmiddlewaretoken': ['CAzCGTlUaGkHWPzAk0eU8FYNVQ74VJrUnrgNZ1Mv8jMMOrGkalDRtIvkdkRBKS1Z'], 'author': ['1'], 'tittle': ['36'], 'text': ['36 dfgsdg'], 'type': ['ARTICLE'], 'category': ['2', '4']}>

# email_query = [{'subscribers__email': '1@qwe.com'}, {'subscribers__email': '3@qwe.com'},
#                {'subscribers__email': '2@qwe.com'}, {'subscribers__email': '3@qwe.com'}, {'subscribers__email': '2@qwe.com'}]
# email_list = []
# [email_list.append(i['subscribers__email']) for i in email_query]
# print(email_list)

class Post():
    tittle = "72"
    text = "72 sfkalfs"


post1 = Post()
print(post1.tittle)
post1.user = "Aurhor1"
print(post1.user)
post1.user = "Aurhor2"
print(post1.user)
