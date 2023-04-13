function fetch_data(){
    var s_date = $('#start_date').val()
    var e_date = $('#end_date').val()
    if (e_date < s_date){
        alert('End date can not be previous then the start date');
        return;
    }
    var data={
        start_date:s_date,
        end_date:e_date,
        csrfmiddlewaretoken: window.CSRF_TOKEN
    }
    $.ajax({
        url: "/fetch_data/",
        data:data,
        method:'POST',
        dataType:'JSON',
        success: function(result){
        console.log(result)
           $('#table_data').html(result['data'])
        },
        error: function(){
            alert("in error")
        },
    });
}