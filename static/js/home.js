console.log("Hii everyone");

const typeOption = document.querySelectorAll("#typeOption");
for(let i=0; i<typeOption.length; i++){
	typeOption[i].addEventListener("click", function(){
		document.getElementById("tagLable").innerHTML = typeOption[i].innerHTML;
		document.getElementById("typeSelected").value = typeOption[i].innerHTML;
	});
}