const 文字欄 = document.querySelector(".文字欄");
const 清單 = document.querySelector(".清單");
const 按鈕 = document.querySelector(".按鈕");

function 新任務() {
    if (文字欄.value === "") {
        return;
    }
    const 任務 = document.createElement("li");
    任務.innerHTML = `
        <input type="checkbox" class="打勾方塊">
        <label>${文字欄.value}</label>
        <button class="垃圾桶">🗑️</button>
    `

    const 垃圾桶 = 任務.querySelector(".垃圾桶");
    const 打勾方塊 = 任務.querySelector(".打勾方塊");

    垃圾桶.addEventListener("click", function() {
        任務.remove();
    });

    打勾方塊.addEventListener("change", function() {
        if (打勾方塊.checked){
            任務.style.textDecoration = "line-through";
            任務.style.color = "#999";
            清單.append(任務);
        } else {
            任務.style.textDecoration = "none";
            任務.style.color = "";
            清單.prepend(任務);
        }
    });

    清單.append(任務);
    文字欄.value = "";
}

按鈕.addEventListener("click", 新任務);

文字欄.addEventListener("keyup", function(e) {
    if (e.key === "Enter") {
        新任務();
    }
});
