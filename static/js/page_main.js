function menu_click(){
    document.getElementById("block_main_1").classList.toggle("menu_close");
    document.getElementById("block_main_2").classList.toggle("menu_show");
    var elem = document.getElementById("settings_button");
    if (elem.textContent == "Настройки") {
        elem.textContent = "Главная";
        
    }
    else {
        elem.textContent = "Настройки";
    }
    }
    

function updateDynamicContent() {
    $.ajax({
        url: '/_',  // Flask route URL
        method: 'get',
        dataType: 'json',
        success: function(data) {
            // Update the content with the fetched data
            $('#pressure_from_sensor').text(data.data_pressure);
            $('#tenzo').text(data.data_tenzo);
            $('#max_pressure').text(data.max_pressure);
        },
        error: function() {
            console.error('Error fetching data.');
        }
    });
}

function сorrect_null() {
    $.ajax({
        url: '/correct_null',  // Flask route URL
        method: 'get',
        dataType: 'json',
        success: function(data) {
            $('#pressure_from_sensor').text(data.data_pressure);
            $('#tenzo').text(data.data_tenzo);
            $('#max_pressure').text(data.max_pressure);
        },
        error: function() {
            console.error('Error fetching data.');
        }
    });
}

function make_document() {
    $.ajax({
        url: '/make_document',  // Flask route URL
        method: 'get',
        dataType: 'json',
        success: function(data) {
            $('#pressure_from_sensor').text(data.data_pressure);
            $('#tenzo').text(data.data_tenzo);
            $('#max_pressure').text(data.max_pressure);
        },
        error: function() {
            console.error('Error fetching data.');
        }
    });
}
// Call the update function initially and set an interval to update regularly
setInterval(updateDynamicContent, 100);