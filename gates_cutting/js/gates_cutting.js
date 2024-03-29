// Стандартні розміри листів металу
    var standardSizes = [
        { area: 2500*1250, size: '2500x1250' },
        { area: 2000*1000, size: '2000x1000' }
        // Додайте інші стандартні розміри, якщо потрібно
    ];
    var arrayLen = standardSizes.length

function calculateQtySheetsByArea() {
    // Парсимо данні з інпутів в body
    var gateWidth = parseInt(document.getElementById("width").value);
    var gateHeight = parseInt(document.getElementById("height").value);
    var totalArea = gateWidth * gateHeight;
    
    var sheetsQty = Array(arrayLen).fill(0);
    var sheetsVariants = [];

    var alive = true;
    while (alive){
        var kitArea = 0;
        var tempLineEntry = {waste: 0, sheets: {}};
        for (var i = 0; i < arrayLen-1; i++){
            kitArea += sheetsQty[i] * standardSizes[i].area;
        }
        var requiredArea = totalArea - kitArea
        if (requiredArea > 0){
            sheetsQty[arrayLen-1] = Math.ceil(requiredArea / standardSizes[arrayLen-1].area);
        } else {
            sheetsQty[arrayLen-1] = 0;
        }
        kitArea += sheetsQty[arrayLen-1] * standardSizes[arrayLen-1].area;

        var wasteArea = kitArea - totalArea;
        var wasteAreaPercentage = wasteArea * 100 / totalArea;
        if (wasteArea > totalArea){
            alive = false;
            break;
        }

        tempLineEntry.waste = Math.round(wasteAreaPercentage*10)/10;
        for (var i=0; i < arrayLen; i++){
            tempLineEntry.sheets[standardSizes[i].size] = sheetsQty[i];
        }
        sheetsVariants.push(tempLineEntry);

        var plusOne = false;
        if (arrayLen == 1 || sheetsQty.slice(1).reduce((acc, curr) => acc + curr, 0) == 0){
            alive = false;
        } else if (arrayLen > 2){
            for (var i = 0; i < arrayLen-2; i++){
                if (sheetsQty.slice(i+2).reduce((acc, curr) => acc + curr, 0) == 0){
                    sheetsQty[i+1] = 0;
                    sheetsQty[i]++;
                    plusOne = false;
                    break;
                } else {
                    plusOne = true;
                }
            }
        } else {
            plusOne = true;
        }

        if (plusOne){
            sheetsQty[arrayLen-2]++
        }

    }

    sheetsVariants.sort(function(a, b) {return a.waste - b.waste;});
    showResults(sheetsVariants);
}

function showResults(variants) {
    var table = document.getElementById("resultTable");
    var thead = table.getElementsByTagName("thead")[0];
    var tbody = table.getElementsByTagName("tbody")[0];
    // Очищення вмісту таблиці
    thead.innerHTML = "";
    tbody.innerHTML = "";

    var theadRow = thead.insertRow();
    theadRow.insertCell().innerHTML = "Втрати %";
    for (i = 0; i < arrayLen; i ++){
        theadRow.insertCell().innerHTML = "Кількість листів " + standardSizes[i].size;
    }
    
    for (var i = 0; i < variants.length; i++){
        var valueRow = tbody.insertRow();
        valueRow.insertCell().innerHTML = variants[i].waste;
    for (var j = 0; j < arrayLen; j++) {
        valueRow.insertCell().innerHTML = variants[i].sheets[standardSizes[j].size];
    }
    }

    document.getElementById("res").style.visibility = "visible"
}