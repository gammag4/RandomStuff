
var hex = "0123456789abcdef"

function intToHex(i) {
	let res = "";
	while (i > 0) {
		res = hex[i % 16] + res;
		i = Math.floor(i / 16);
	}
	return res
}

function createPage(i) {
	let image = document.createElement("img");
	document.getElementById("book").appendChild(image);
	image.src = `https://files.passeidireto.com/e1b16a52-a8bb-4f0e-8300-faedd2d53a8e/bg${intToHex(i)}.png`;
}

document.getElementsByTagName("body")[0].innerHTML = "<p id=\"book\"></p>"

var start = 1;
var end = 327;

for (let i = start; i <= end; i++) {
	createPage(i);
}
