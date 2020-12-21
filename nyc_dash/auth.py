
def get_user(request):
	
	login_value = request.get_Arguement('login')
	password_value = request.get_Arguement('password')
	if login_value=='nyc' and password_value='iheartnyc':
		Return 1
	Else: 
		Return None
		


