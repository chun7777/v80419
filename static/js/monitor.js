
setInterval(function() {
    $.get("/monitor", function(data) {
        data.forEach(function(stock) {
            var cell = $("td.price[data-stock='" + stock.stock + "']");
            var oldPrice = parseFloat(cell.text());
            var newPrice = parseFloat(stock.price);
            var row = $("#row-" + stock.stock);
            var support = parseFloat(row.find(".support").text());
            var resistance = parseFloat(row.find(".resistance").text());
            var message = "";

            // 動態策略提示
            if (!isNaN(newPrice)) {
                if (Math.abs(newPrice - support) < 0.3) {
                    message = "接近支撐，留意轉強";
                    row.removeClass().addClass("highlight-green");
                } else if (Math.abs(newPrice - resistance) < 0.3) {
                    message = "接近壓力，提防回落";
                    row.removeClass().addClass("highlight-red");
                } else {
                    row.removeClass();
                }
            }

            cell.text(stock.price);
            row.find(".message").text(message);
        });
    });
}, 30000);  // 每30秒更新
