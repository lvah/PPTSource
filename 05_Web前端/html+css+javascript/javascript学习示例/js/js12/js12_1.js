//自定义函数
function jiSuan(num1,num2,operator){ //特别强调：参数名前不要带var
	var res=0;
	if(operator=="+"){
		res=num1+num2;
	}else if(operator=="-"){
		res=num1-num2;
	}else if(operator=="*"){
		res=num1*num2;
	}else if(operator=="/"){
		res=num1/num2;
	}else if(operator=="%"){
		res=num1%num2;
	}
	return res;//返回值
}