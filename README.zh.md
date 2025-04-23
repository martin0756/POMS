




## 平台简介

基于RBAC模型的权限控制的一整套基础开发平台，前后端分离，后端采用django + django-rest-framework，前端采用基于 vue3 + CompositionAPI + typescript + vite + element plus


* 🧑‍🤝‍🧑前端采用 Vue3+TS+pinia+fastcrud
* 👭后端采用 Python 语言 Django 框架以及强大的 [Django REST Framework](https://pypi.org/project/djangorestframework)。
* 👫权限认证使用[Django REST Framework SimpleJWT](https://pypi.org/project/djangorestframework-simplejwt)，支持多终端认证系统。



## 前端♝

```bash
cd web
npm install yarn
yarn install --registry=https://registry.npmmirror.com
yarn run build
```



## 后端💈

~~~bash
cd backend
mv ./conf/env.example.py ./conf/env.py
在 env.py 中配置数据库信息
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py init
python3 manage.py init_area
python3 manage.py runserver 0.0.0.0:8000
~~~












