"""backend URL Configuration
   # 后端URL配置

The `urlpatterns` list routes URLs to views. For more information please see:
# urlpatterns列表将URL路由到视图函数。更多信息请参考：
    https://docs.djangoproject.com/en/3.2/topics/http/urls/

Examples:
# 示例：
Function views
# 函数视图
    1. Add an import:  from my_app import views
    # 1. 添加导入：from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
    # 2. 添加URL到urlpatterns：path('', views.home, name='home')
Class-based views
# 类视图
    1. Add an import:  from other_app.views import Home
    # 1. 添加导入：from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    # 2. 添加URL到urlpatterns：path('', Home.as_view(), name='home')
Including another URLconf
# 包含其他URL配置
    1. Import the include() function: from django.urls import include, path
    # 1. 导入include()函数：from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    # 2. 添加URL到urlpatterns：path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from application import dispatch
from application import settings
from dvadmin.system.views.dictionary import InitDictionaryViewSet
from dvadmin.system.views.login import (
    LoginView,
    CaptchaView,
    ApiLogin,
    LogoutView,
    LoginTokenView
)
from dvadmin.system.views.system_config import InitSettingsViewSet
from dvadmin.utils.swagger import CustomOpenAPISchemaGenerator

# =========== 初始化系统配置 =================
dispatch.init_system_config()
# 初始化系统配置
dispatch.init_dictionary()
# 初始化字典数据
# =========== 初始化系统配置 =================

schema_view = get_schema_view(
# 创建一个Swagger模式视图，用于生成API文档
    openapi.Info(
    # 定义API的基本元信息
        title="Snippets API",
        # API的标题名称
        default_version="v1",
        # API的默认版本号
        description="Test description",
        # API的简要描述
        terms_of_service="https://www.google.com/policies/terms/",
        # API的服务条款URL
        contact=openapi.Contact(email="contact@snippets.local"),
        # API的联系信息
        license=openapi.License(name="BSD License"),
        # API的许可证信息
    ),
    public=True,
    # 设置为True表示无需身份验证即可访问API文档
    permission_classes=(permissions.AllowAny,),
    # 允许任何用户访问API文档，无需权限验证
    generator_class=CustomOpenAPISchemaGenerator,
    # 使用自定义的模式生成器，用于定制API文档的生成逻辑
)
# 前端页面映射
from django.http import Http404, HttpResponse
from django.shortcuts import render
import mimetypes
import os


def web_view(request):
# 定义视图函数
    return render(request, 'web/index.html')
    # 用于渲染前端应用的主页面


def serve_web_files(request, filename):
# 定义视图函数，用于提供前端静态资源
    filepath = os.path.join(settings.BASE_DIR, 'templates', 'web', filename)
    # 构建文件路径，指向模板目录下的web文件夹
    if not os.path.exists(filepath):
    # 检查文件是否存在
        raise Http404("File does not exist")

    mime_type, _ = mimetypes.guess_type(filepath)
    # 根据文件扩展名，确定 MIME 类型

    with open(filepath, 'rb') as f:
    # 以二进制模式打开文件并返回响应
        response = HttpResponse(f.read(), content_type=mime_type)
        return response


urlpatterns = (
# 定义URL路由规则
        [
            re_path(
                r"^swagger(?P<format>\.json|\.yaml)$",
                schema_view.without_ui(cache_timeout=0),
                name="schema-json",
            ),
            # Swagger JSON/YAML格式文档的URL
            path(
                "",
                schema_view.with_ui("swagger", cache_timeout=0),
                name="schema-swagger-ui",
            ),
            # Swagger UI界面的URL
            path(
                r"redoc/",
                schema_view.with_ui("redoc", cache_timeout=0),
                name="schema-redoc",
            ),
            # ReDoc界面的URL
            path("api/system/", include("dvadmin.system.urls")),
            # 系统模块API的URL
            path("api/login/", LoginView.as_view(), name="token_obtain_pair"),
            # 登录接口
            path("api/logout/", LogoutView.as_view(), name="token_obtain_pair"),
            # 登出接口
            path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
            # 刷新令牌接口
            re_path(
                r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")
            ),
            # DRF自带的认证URL
            path("api/captcha/", CaptchaView.as_view()),
            # 验证码接口
            path("api/init/dictionary/", InitDictionaryViewSet.as_view()),
            # 初始化字典数据接口
            path("api/init/settings/", InitSettingsViewSet.as_view()),
            # 初始化系统设置接口
            path("apiLogin/", ApiLogin.as_view()),
            # API登录接口
            path("api/token/", LoginTokenView.as_view()),
            # 仅用于开发环境的令牌获取接口，上线需关闭
            path('web/', web_view, name='web_view'),
            # 前端页面映射
            path('web/<path:filename>', serve_web_files, name='serve_web_files'),
            # 前端页面映射
        ]
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        # 添加媒体文件的URL映射
        + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
        # 添加静态文件的URL映射
        + [re_path(ele.get('re_path'), include(ele.get('include'))) for ele in settings.PLUGINS_URL_PATTERNS]
        # 添加插件的URL映射
)
