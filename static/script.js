let cvs = document.getElementById("inputimg");

let ctx = cvs.getContext("2d");
let onClick = false;

window.onload = function () {
    onClick = false;
    ctx.lineWidth = 15;
}

cvs.addEventListener("mousedown", function (e) {
    onClick = true;
    const rect = e.target.getBoundingClientRect();
    let x = e.clientX - rect.left;
    let y = e.clientY - rect.top;
    ctx.beginPath();
    ctx.moveTo(x, y);
})

cvs.addEventListener("mousemove", function (e) {
    if (!onClick) return;
    const rect = e.target.getBoundingClientRect();
    let x = e.clientX - rect.left;
    let y = e.clientY - rect.top;
    ctx.lineTo(x, y);
    ctx.stroke();
})

cvs.addEventListener("mouseup", function (e) {
    onClick = false;
    ctx.closePath();

    recognize();
})

document.getElementById("clearbtn").addEventListener("click", function (e) {
    ctx.clearRect(0, 0, cvs.width, cvs.height);
    document.getElementById("pred").innerHTML = 0
    document.getElementById("prob").innerHTML = ""
})

function recognize() {
    cvs.toBlob(async blob => {
        
        const body = new FormData();
        body.append('img', blob, "dummy.png")
        try{
            const response = await fetch("/recognize", {
                method: "POST",
                body: body,
            })
            const resjson = await response.json()
            let digit = resjson["digit"]
            let prob = resjson["confidence"]
            
            document.getElementById("pred").innerHTML = digit
            document.getElementById("prob").innerHTML = "Probability: " + prob.toFixed(6)
        } catch (error){
            alert("error", error)
        }
    })
}