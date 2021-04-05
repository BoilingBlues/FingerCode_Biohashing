package errcode

var (
	ErrorUserLoginFail          = NewError(20000001, "登录失败")
	ErrorUserRegistFail         = NewError(20000002, "注册失败")
	ErrorUserUpdateFail         = NewError(20000003, "更新失败")
	ErrorUserAuthenticationFail = NewError(20000004, "认证失败")
	ErrorUserAdminFail          = NewError(20000005, "鉴权失败")

	ErrorLogListFail = NewError(30000001, "获取失败")
)
