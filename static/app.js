var i = 1
var b = 0
let answers = []
let buttons = []
while (b == 0){
	var a = document.getElementById("answer" + i);
	console.log(a)
	var q = document.getElementById("button" + i);
	if (a == null){
		break;
	}
	buttons.push(q)
	answers.push(a)
	buttons[i - 1].addEventListener("click", alertMe);
	console.log(answers)
	function alertMe(){
		answers[i - 1].style.visibility = "visible";
	}
	console.log("answer" + i)
	i++;
}