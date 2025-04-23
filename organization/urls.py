from django.urls import path

from .views import OrganizationList, OrganizationDetail, EmployeeDetail, EmployeeListByOrganization, \
    EmployeeListByOrganizationAndUserType, Login, Logout, Profile, EmployeesView, EmployeeActiveInActive, EmployeeView

urlpatterns = [
    path('organizations/', OrganizationList.as_view(), name='organization-create'),
    path('organization/<int:pk>', OrganizationDetail.as_view(), name='organization-create'),
    path('employees/', EmployeesView.as_view(), name='employee-create'),
    # path('employee/<int:pk>', EmployeeDetail.as_view(), name='employee-create'),
    path('employee/active-inactive/<uuid:pk>', EmployeeActiveInActive.as_view(), name='employee-create'),
    path('employee/<uuid:pk>', EmployeeView.as_view(), name='employee-create'),
    path('employees/<int:organization>/<str:user_type>', EmployeeListByOrganizationAndUserType.as_view(), name='employee-create'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('profile/', Profile.as_view(), name='profile'),
    path('organization/employees/', EmployeeListByOrganization.as_view(), name='org-employees'),

]